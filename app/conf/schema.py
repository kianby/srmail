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
                "rabbitmq": {
                    "$ref": "#/definitions/Rabbitmq"
                }
            },
            "required": [
                "general",
                "http",
                "imap",
                "rabbitmq",
                "smtp"
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
                    "type": "boolean"
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
                    "type": "boolean"
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
        "Rabbitmq": {
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
                },
                "username": {
                    "type": "string"
                },
                "password": {
                    "type": "string"
                },
                "vhost": {
                    "type": "string"
                },
                "exchange": {
                    "type": "string"
                }
            },
            "required": [
                "active",
                "exchange",
                "host",
                "password",
                "port",
                "username",
                "vhost"
            ],
            "title": "rabbitmq"
        }
    }
}
"""