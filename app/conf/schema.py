#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with https://jsonschema.net
#   Object options : required

json_schema = """
{
  "definitions": {}, 
  "$schema": "http://json-schema.org/draft-04/schema#", 
  "type": "object", 
  "id": "http://example.com/example.json", 
  "additionalProperties": false, 
  "required": [
    "global", 
    "imap", 
    "smtp", 
    "http", 
    "post"
  ], 
  "properties": {
    "global": {
      "type": "object", 
      "additionalProperties": false, 
      "required": [
        "lang", 
        "polling", 
        "exit_on_error"
      ], 
      "properties": {
        "lang": {
          "type": "string", 
          "title": "The Lang Schema.", 
          "description": "An explanation about the purpose of this instance.", 
          "default": ""
        }, 
        "polling": {
          "type": "integer", 
          "title": "The Polling Schema.", 
          "description": "An explanation about the purpose of this instance.", 
          "default": 0
        }, 
        "exit_on_error": {
          "type": "boolean", 
          "title": "The Exit_on_error Schema.", 
          "description": "An explanation about the purpose of this instance.", 
          "default": false
        }
      }
    }, 
    "imap": {
      "type": "object", 
      "additionalProperties": false, 
      "required": [
        "host", 
        "ssl", 
        "port", 
        "login", 
        "password"
      ], 
      "properties": {
        "host": {
          "type": "string", 
          "title": "The Host Schema.", 
          "description": "An explanation about the purpose of this instance.", 
          "default": ""
        }, 
        "ssl": {
          "type": "boolean", 
          "title": "The Ssl Schema.", 
          "description": "An explanation about the purpose of this instance.", 
          "default": false
        }, 
        "port": {
          "type": "integer", 
          "title": "The Port Schema.", 
          "description": "An explanation about the purpose of this instance.", 
          "default": 0
        }, 
        "login": {
          "type": "string", 
          "title": "The Login Schema.", 
          "description": "An explanation about the purpose of this instance.", 
          "default": ""
        }, 
        "password": {
          "type": "string", 
          "title": "The Password Schema.", 
          "description": "An explanation about the purpose of this instance.", 
          "default": ""
        }
      }
    }, 
    "smtp": {
      "type": "object", 
      "additionalProperties": false, 
      "required": [
        "host", 
        "starttls", 
        "port", 
        "login", 
        "password"
      ], 
      "properties": {
        "host": {
          "type": "string", 
          "title": "The Host Schema.", 
          "description": "An explanation about the purpose of this instance.", 
          "default": ""
        }, 
        "starttls": {
          "type": "boolean", 
          "title": "The Starttls Schema.", 
          "description": "An explanation about the purpose of this instance.", 
          "default": false
        }, 
        "port": {
          "type": "integer", 
          "title": "The Port Schema.", 
          "description": "An explanation about the purpose of this instance.", 
          "default": 0
        }, 
        "login": {
          "type": "string", 
          "title": "The Login Schema.", 
          "description": "An explanation about the purpose of this instance.", 
          "default": ""
        }, 
        "password": {
          "type": "string", 
          "title": "The Password Schema.", 
          "description": "An explanation about the purpose of this instance.", 
          "default": ""
        }
      }
    }, 
    "http": {
      "type": "object", 
      "additionalProperties": false, 
      "required": [
        "host", 
        "port"
      ], 
      "properties": {
        "host": {
          "type": "string", 
          "title": "The Host Schema.", 
          "description": "An explanation about the purpose of this instance.", 
          "default": ""
        }, 
        "port": {
          "type": "integer", 
          "title": "The Port Schema.", 
          "description": "An explanation about the purpose of this instance.", 
          "default": 0
        }
      }
    }, 
    "post": {
      "type": "object", 
      "additionalProperties": false, 
      "required": [
        "default", 
        "routing"
      ], 
      "properties": {
        "default": {
          "type": "string", 
          "title": "The Default Schema.", 
          "description": "An explanation about the purpose of this instance.", 
          "default": ""
        }, 
        "routing": {
          "type": "array", 
          "items": {
            "id": "kamchatkabear", 
            "title": "Empty Object", 
            "description": "This accepts anything, as long as it's valid JSON."
          }
        }
      }
    }
  }
}


"""