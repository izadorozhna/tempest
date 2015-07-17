api_version = {
    "name": "snapshots-metadata",
    "json-schema": {
        "type": "object",
        "properties": {
        }
    }
}

api_version["json-schema"]["properties"] = {
    "api_version": {
        "type": "integer",
        "results": {
            "api_version_1": 1,
            "api_version_2": 2
        }
    }
}
