import json
import logging
import os
import re
import signal

from confluent_kafka import Producer, Consumer, KafkaException, KafkaError
from gridfs import GridFSBucket, NoFile
from pydantic import ValidationError
from pymongo import MongoClient
from jsonschema import validate

from .helpers.schema import schema
from .ti_object_models.exceptions import (FieldRequired, FieldEmpty,
                                          ConnectionRequired, ValidationException, JsonSerialize)
from .ti_object_models.request import Request
from .ti_object_models.response_external import Response, ResponseExternal
from .ti_object_models.handshake import Handshake
from .configuration import Configuration
from .ti_object_models.file_specific_fields import FileSpecificFields
from .ti_object_models.network_artifact_specific_fields import NetworkArtifactSpecificFields


class Analyzer:
    """
    Describes instance of analyzer connected to RT Protect TI instance
    """
    is_running = False

    def __init__(self, configuration: Configuration):
        """
        Describes instance of analyzer connected to RT Protect TI instance
        :param configuration: Analyzer configuration
        """

        if not configuration:
            raise FieldRequired('configuration')

        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

        self.conf: Configuration = configuration
        self.topic_name = self.conf.topic_name
        self.callback = self.conf.callback

        config = {'KafkaBootstrapServers': configuration.kafka_bootstrap_servers,
                  'MongoConnectionString': configuration.mongo_connection_string}
        config.update(os.environ)

        kafka_bootstrap_servers = config['KafkaBootstrapServers']
        if not kafka_bootstrap_servers:
            raise FieldEmpty("kafka_bootstrap_servers")

        if self.conf.connection_to_storage_required:
            mongo_connection_string = config['MongoConnectionString']
            if not mongo_connection_string:
                raise FieldEmpty("mongo_connection_string")
            self.gridFS = GridFSBucket(MongoClient(self.conf.mongo_connection_string)['file_storage'])

        self.throw_if_configuration_invalid(configuration)

        self.consumer = Consumer({
            'bootstrap.servers': self.conf.kafka_bootstrap_servers,
            'group.id': 'analyzer',
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': False,
            'message.max.bytes': 1024 * 1024 * 500
        })

        self.producer = Producer({
            'bootstrap.servers': self.conf.kafka_bootstrap_servers,
            'message.max.bytes': 1024 * 1024 * 500
        })

    def signal_handler(self, signum, frame):
        """
        Internal handler to stop analyzer runner
        """
        self.stop()
        logging.info("Analyzer runner stopped")

    def run(self):
        """
        Runs current instance of analyzer. This method has infinite loop,
        use method "stop" to break.
        When receiving a request from the server to analyze an artifact,
        the CallbackAction function from the configuration will be called
        """

        if self.is_running:
            raise ValidationException("Analyzer is already running")

        self.is_running = True

        self.consumer.subscribe([self.topic_name])
        logging.info(f"Subscribed to {self.topic_name}")

        hand_shake = Handshake(AnalyzerName=self.conf.analyzer_name,
                               ArtifactTypes=[e.value for e in self.conf.artifact_types],
                               TopicName=self.topic_name,
                               MaxAnalyzeTimeInMinutes=self.conf.max_analyze_time_in_minutes,
                               FileInStorageRequired=self.conf.file_in_storage_required,
                               AutoEnrichmentEnabled=self.conf.auto_enrichment_enabled,
                               HtmlTemplate=self.conf.html_template,
                               Arguments=self.conf.arguments,
                               DisplayName=self.conf.display_name,
                               ReportLifetimeInDays=self.conf.report_lifetime_in_days)

        if self.conf.image_configuration:
            hand_shake.Image = self.conf.image_configuration.image
            hand_shake.ImageContentType = self.conf.image_configuration.image_content_type

        hs_json = hand_shake.model_dump_json()

        logging.info(f"Producing handshake. Object: {hs_json}")

        self.producer.produce('analyze_worker', key='handshake', value=hs_json)
        self.producer.flush()

        logging.info(f"Produced handshake. Analyzer name: {hand_shake.AnalyzerName}")

        while self.is_running:
            message = self.consumer.poll(timeout=1.0)

            if message is None:
                continue

            if message.error():
                if message.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    raise KafkaException(message.error())

            value = message.value()
            logging.info(f"Message value: {value}")
            try:
                request_source = Request.model_validate_json(value)
            except ValidationError as err:
                logging.error(f"Exception while request validating json. Exception: {err}")
                raise err

            if request_source is None:
                logging.critical(f"Unable to parse analyzer request. Request: {value}")
                self.consumer.commit(message=message, asynchronous=False)
                continue

            logging.info(f"Request consumed. Request: {request_source.model_dump_json()}")
            analyzer_report = ResponseExternal(FileSpecificFields=None, NetworkArtifactSpecificFields=None)
            try:
                request = Request(AnalyzerName=request_source.AnalyzerName,
                                  Artifact=request_source.Artifact,
                                  ArtifactType=request_source.ArtifactType,
                                  QueueTime=request_source.QueueTime,
                                  Args=request_source.Args)
                self.callback(request, analyzer_report)
            except Exception as err:
                logging.error(f"Exception while handling request. Exception: {err}")
                analyzer_report = ResponseExternal(Error=str(err),
                                                   FileSpecificFields=None,
                                                   NetworkArtifactSpecificFields=None)

            self.validate_analyzer_response(analyzer_report, request_source.ArtifactType)
            analyzer_report.AnalyzerName = request_source.AnalyzerName
            analyzer_report.AnalyzerReportId = request_source.AnalyzerReportId
            analyzer_report.Artifact = request_source.Artifact
            analyzer_report.ArtifactType = request_source.ArtifactType

            report_json = analyzer_report.model_dump_json()
            logging.info(f"report_json: {report_json}")
            report_instance = json.loads(report_json)
            logging.info(f"report_instance: {report_instance}")

            validate(instance=report_instance, schema=schema)

            self.producer.produce('analyze_worker', key='report', value=report_json)
            self.producer.flush()

            logging.info("Request produced")
            self.consumer.commit(message=message, asynchronous=False)
            logging.info("Request handled")

    def get_file_stream_from_storage(self, sha256):
        """
        Returns instance of GridOut containing file data downloaded from TI file storage
        :param sha256: SHA256 of a file
        :return: Returns an instance of :class:`~gridfs.grid_file.GridOut`
        """

        logging.info(f"Downloading file {sha256} from MongoDB")
        try:
            return self.gridFS.open_download_stream_by_name(sha256)
        except (NoFile, ValueError) as err:
            logging.error(f"Exception while downloading file. Exception: {err}")
            raise err

    def throw_if_configuration_invalid(self, conf: Configuration):
        """
        Internal method for validate configuration
        :param conf: Analyzer configuration
        """

        if not conf.analyzer_name:
            raise FieldEmpty("analyzer_name")

        if not conf.display_name:
            raise FieldEmpty("display_name")

        if conf.artifact_types is None or len(conf.artifact_types) == 0:
            raise FieldEmpty("artifact_types")

        if not conf.topic_name:
            raise FieldEmpty("topic_name")

        if not conf.callback:
            raise FieldEmpty("callback")

        if conf.file_in_storage_required:
            if not conf.connection_to_storage_required or self.gridFS is None:
                raise ConnectionRequired("connection_to_storage_required")

        if conf.connection_to_storage_required and self.gridFS is None:
            raise ConnectionRequired("connection_to_storage_required")

        if conf.max_analyze_time_in_minutes < 0:
            raise ValidationException("max_analyze_time_in_minutes must be positive value")

        if conf.arguments:
            for argument in conf.arguments:
                if not argument.Name:
                    raise FieldEmpty("argument_name")

        if conf.image_configuration and conf.image_configuration.image:
            if not conf.image_configuration.image_content_type:
                raise FieldEmpty("image_content_type")
            elif not conf.image_configuration.image_content_type.lower().startswith('image'):
                raise ValidationException("image_content_type")

    @staticmethod
    def validate_analyzer_response(response: Response,
                                   artifact_type: str):
        """
        Internal method for validate response from analyzer
        :param response: Analyzer response
        :param artifact_type: Artifact type
        """

        if not response:
            raise FieldRequired("response")

        try:
            response.Report = json.dumps(response.Report) if response.Report else None
        except Exception as err:
            logging.info(f"Exception while report converting to json. Exception {err}")
            raise JsonSerialize(err)

        if artifact_type == 'file' and response.FileSpecificFields is not None:
            Analyzer.validate_file_params(response.FileSpecificFields)

        elif (artifact_type == 'ip' or 'domain' or 'url' or 'email') and response.NetworkArtifactSpecificFields:
            Analyzer.validate_network_params(response.NetworkArtifactSpecificFields)

    @staticmethod
    def validate_network_params(params: NetworkArtifactSpecificFields):
        """
        Internal method to validate network specific parameters
        """

        if params.IpNetwork:
            if not re.search(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,3}$', params.IpNetwork):
                raise ValidationException("IpNetwork")

    @staticmethod
    def validate_file_params(params: FileSpecificFields):
        """
        Internal method to validate file specific parameters
        """

        if params.SizeInBytes and params.SizeInBytes < 0:
            raise ValidationException("SizeInBytes must be positive")

        if params.Md5:
            if not re.search('^[0-9a-fA-F]{32}$', params.Md5):
                raise ValidationException("Md5")

        if params.Sha1:
            if not re.search('^[0-9a-fA-F]{40}$', params.Sha1):
                raise ValidationException("Sha1")

        if params.Sha256:
            if not re.search('^[0-9a-fA-F]{64}$', params.Sha256):
                raise ValidationException("Sha256")

        if params.Sha512:
            if not re.search('^[0-9a-fA-F]{128}$', params.Sha512):
                raise ValidationException("Sha512")

    def stop(self):
        """
        Stop work loop analyzer method and closing kafka consumer
        """

        self.is_running = False
        self.consumer.close()
