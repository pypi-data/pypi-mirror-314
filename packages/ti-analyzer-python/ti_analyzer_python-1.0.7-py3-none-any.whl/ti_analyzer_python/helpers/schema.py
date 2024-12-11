schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "Report": {
            "type": [
                "string",
                "null"
            ]
        },
        "Error": {
            "type": [
                "string",
                "null"
            ]
        },
        "DetectedTime": {
            "type": [
                "string",
                "null"
            ]
        },
        "Score": {
            "type": [
                "integer",
                "null"
            ],
            "minimum": -100,
            "maximum": 100
        },
        "Tags": {
            "type": [
                "array",
                "null"
            ],
            "items":
            [
                {
                    "type": ["string", "null"]
                }
            ]
        },
        "RelatedArtifacts": {
            "type": [
                "array",
                "null"
            ],
            "items":
            [
                {
                    "type": ["object", "null"],
                    "properties": {
                        "Artifact": {
                            "type": "string"
                        },
                        "RelationshipType": {
                            "type": "integer"
                        }
                    }
                }
            ]
        },
        "FileSpecificFields": {
            "type": [
                "object",
                "null"
            ],
            "properties": {
                "Names": {
                    "type": ["array", "null"],
                    "items":
                    [
                        {
                            "type": "string"
                        }
                    ]
                },
                "SizeInBytes": {
                    "type": ["integer", "null"]
                },
                "Sha256": {
                    "type": ["string", "null"]
                },
                "Sha1": {
                    "type": ["string", "null"]
                },
                "Md5": {
                    "type": ["string", "null"]
                },
                "Sha512": {
                    "type": ["string", "null"]
                },
                "Tlsh": {
                    "type": ["string", "null"]
                },
                "Ssdeep": {
                    "type": ["string", "null"]
                },
                "Imphash": {
                    "type": ["string", "null"]
                }
            }
        },
        "NetworkArtifactSpecificFields": {
            "type": [
                "object",
                "null"
            ],
            "properties": {
                "Whois": {
                    "type": ["string", "null"]
                },
                "WhoisTime": {
                    "type": ["string", "null"]
                },
                "Country": {
                    "type": ["string", "null"]
                },
                "IpNetwork": {
                    "type": ["string", "null"]
                },
                "Registrar": {
                    "type": ["string", "null"]
                }
            }
        },
        "AnalyzerName": {
            "type": "string"
        },
        "AnalyzerReportId": {
            "type": "string"
        },
        "Artifact": {
            "type": "string"
        },
        "ArtifactType": {
            "type": "string"
        }
    },
    "required": [
        "AnalyzerName",
        "AnalyzerReportId",
        "Artifact",
        "ArtifactType"
    ]
}
