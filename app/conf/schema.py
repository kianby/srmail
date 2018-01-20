#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with https://app.quicktype.io
#   name: srmail

json_schema = """
{
    "$ref": "#/definitions/Srmail",
    "definitions": {
        "Srmail": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "general": {
                    "$ref": "#/definitions/General"
                },
                "imap": {
                    "$ref": "#/definitions/IMAP"
                },
                "smtp": {
                    "$ref": "#/definitions/IMAP"
                },
                "http": {
                    "$ref": "#/definitions/HTTP"
                },
                "zmq": {
                    "$ref": "#/definitions/Zmq"
                }
            },
            "required": [
                "general",
                "http",
                "imap",
                "smtp",
                "zmq"
            ],
            "title": "srmail"
        },
        "General": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "polling": {
                    "type": "integer"
                },
                "db_url": {
                    "type": "string"
                }
            },
            "required": [
                "db_url",
                "polling"
            ],
            "title": "general"
        },
        "HTTP": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "active": {
                    "type": "boolean"
                },
                "host": {
                    "type": "string"
                },
                "port": {
                    "type": "integer"
                }
            },
            "required": [
                "active",
                "host",
                "port"
            ],
            "title": "http"
        },
        "IMAP": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "host": {
                    "type": "string"
                },
                "ssl": {
                    "oneOf": [
                        {
                            "type": "boolean"
                        },
                        {
                            "type": "null"
                        }
                    ],
                    "title": "ssl"
                },
                "port": {
                    "type": "integer"
                },
                "login": {
                    "type": "string"
                },
                "password": {
                    "type": "string"
                },
                "starttls": {
                    "oneOf": [
                        {
                            "type": "boolean"
                        },
                        {
                            "type": "null"
                        }
                    ],
                    "title": "ssl"
                }
            },
            "required": [
                "host",
                "login",
                "password",
                "port"
            ],
            "title": "imap"
        },
        "Zmq": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "active": {
                    "type": "boolean"
                },
                "host": {
                    "type": "string"
                },
                "pub_port": {
                    "type": "integer"
                },
                "sub_port": {
                    "type": "integer"
                }
            },
            "required": [
                "active",
                "host",
                "pub_port",
                "sub_port"
            ],
            "title": "zmq"
        }
    }
}
"""