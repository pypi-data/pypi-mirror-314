import json
from decimal import Decimal
from datetime import datetime


class Encoder(json.JSONEncoder):
    
    def defaul(self, obj):
        if isinstance(obj, Decimal):
            if obj % 1 == 0:
                return int(obj)
            return float(obj)
        elif isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d")
        return str(obj)


class API:
    
    def __init__(self, event, **args):
        self.event = event
        self.extra_params = args
        
    @staticmethod
    def get_default(data, field, default):
        return data[field] if data.get(field) else default
    
    @property
    def body(self):
        raw_body = self.get_default(self.event, field="body", default={})
        return json.loads(raw_body)
    
    @property
    def headers(self):
        raw_headers = self.get_default(self.event, field="headers", default={})
        return {k.lower(): v for k, v in raw_headers.items()}
    
    @property
    def path_parameters(self):
        return self.get_default(self.event, field="pathParameters", default={})
    
    @property
    def path(self):
        return self.event["requestContext"]["resourcePath"] if self.event["requestContext"].get("resourcePath") else self.event["requestContext"]["routeKey"].split(" ")[-1]
    
    @property
    def query_string_parameters(self):
        return self.get_default(self.event, field="queryStringParameters", default={})
    
    @property
    def request(self):
        return {
            "headers": self.headers,
            "path": self.path,
            "path_parameters": self.path_parameters,
            "query_string_parameters": self.query_string_parameters,
            "body": self.body   
        }
    
    @property
    def response_headers(self):
        cors_headers = {}
        origin = self.get_default(self.headers, field="origin", default="")
        allowed = "*" in self.extra_params["cors-allowed-origin"]
        if origin is self.extra_params["cors-allowed-origin"] or allowed:
            cors_headers = {
                "Access-Control-Allow-Origin": origin,
                "Access-Control-Allow-Credentials": "true",
                "Access-Control-Allow-Methods": self.extra_params["cors-allowed-methods"],
                "Access-Control-Allow-Headers": self.extra_params["cors-allowed-headers"]
            }
        return {
            **cors_headers,
            "X-XSS-Protection": "1; mode=block",
            "X-Frame-Options": "DENY",
            "X-Content-Type-Options": "nosniff",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains"
        }
    
    @property
    def error_response(self, exception):
        if exception.__class__.__name__ != "":
            exception.args = ({"pt": "Erro", "en": "Error"}, 500)
        return {
            "statusCode": exception.args[1],
            "headers": self.response_headers,
            "body": {
                "error": {
                    "type": type(exception).__name__,
                    "description": exception.args[0]
                }
            }
        }
    
    def success_response(self, data):
        return {
            "statusCode": 200,
            "headers": self.response_headers,
            "body": json.dumps(data, cls=Encoder, ensure_ascii=False)
        }