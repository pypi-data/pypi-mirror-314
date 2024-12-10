from typing import List, Callable

from pydantic import BaseModel

from .image_configuration import ImageConfiguration
from .ti_object_models.argument import Argument
from .ti_object_models.request import Request
from .ti_object_models.response import Response
from .ti_object_models.ti_artifact_types import TiArtifactTypes


class Configuration(BaseModel):
    """
    Analyzer configuration
    :param str analyzer_name: [Required] The name of the analyzer used to identify it
    :param str display_name: [Required] The name of the analyzer used to display it
    :param List[TiArtifactTypes] artifact_types: [Required] Artifact types supported by analyzer
    :param str topic_name: [Required] Name of a topic to get a report requests. Topic name should identify analyzer
    :param Callable[[Request, Response], None] callback:
        [Required] Action that invokes to handle RT Protect TI report request
    :param str kafka_bootstrap_servers: [Required]
        Server addresses to connect with RT Protect TI Kafka instance.
        Might be replaced via KafkaBootstrapServers environment variable
    :param bool file_in_storage_required:
        Determines whether the analyzer requires the file to be present in the file storage
    :param bool connection_to_storage_required:
        Determines whether the analyzer requires the connection to the file storage
    :param str mongo_connection_string:
        Connection string to connect with RT Protect TI MongoDB instance.
        Required if file_in_storage_required flag is True.
        Might be replaced via MongoConnectionString environment variable
    :param str html_template: HTML template to visualize the analyzer report data
    :param int max_analyze_time_in_minutes: [Required] Maximum time required to analyze an artifact
    :param bool auto_enrichment_enabled:
        The request will be automatically sent without arguments when the artifact page opened
    :param List[Argument] arguments: List of arguments supported by the analyzer
    :param int report_lifetime_in_days: The analyzer report validity period in days
    :param ImageConfiguration image_configuration: Image analyzer configuration
   """
    analyzer_name: str
    display_name: str
    artifact_types: List[TiArtifactTypes]
    topic_name: str
    callback: Callable[[Request, Response], None]
    kafka_bootstrap_servers: str
    file_in_storage_required: bool = False
    connection_to_storage_required: bool = False
    mongo_connection_string: str | None = None
    html_template: str | None = None
    max_analyze_time_in_minutes: int = 0
    auto_enrichment_enabled: bool = False
    arguments: List[Argument] | None = None
    report_lifetime_in_days: int = 0
    image_configuration: ImageConfiguration | None
