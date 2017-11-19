#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with https://jsonschema.net
#   schema: draft-04
#   Object options: required

json_schema = """
{
  "definitions": {}, 
  "$schema": "http://json-schema.org/draft-04/schema#", 
  "type": "object", 
  "id": "http://example.com/example.json", 
  "additionalProperties": false, 
  "required": [
    "general", 
    "imap", 
    "smtp", 
    "http"
  ], 
  "properties": {
    "general": {
      "type": "object", 
      "additionalProperties": false, 
      "required": [
        "polling", 
        "db_url"
      ], 
      "properties": {
        "polling": {
          "type": "integer", 
          "title": "The Polling Schema.", 
          "description": "An explanation about the purpose of this instance.", 
          "default": 0
        }, 
        "db_url": {
          "type": "string", 
          "title": "The Db_url Schema.", 
          "description": "An explanation about the purpose of this instance.", 
          "default": ""
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
        "active",
        "host", 
        "port"
      ], 
      "properties": {
        "active": {
          "type": "boolean", 
          "title": "The Active Schema.", 
          "description": "An explanation about the purpose of this instance.", 
          "default": ""
        },      
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
    "nsq": {
      "type": "object", 
      "additionalProperties": false, 
      "required": [
        "active",
        "host", 
        "port"
      ], 
      "properties": {
        "active": {
          "type": "boolean", 
          "title": "The Active Schema.", 
          "description": "An explanation about the purpose of this instance.", 
          "default": ""
        },       
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
    }    
  }
}
"""