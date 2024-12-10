from enum import Enum

class Methods(Enum):
    POST = 'POST'
    GET = 'GET'
    PUT = 'PUT'

class ResponseTypes(Enum):
    TEXT = 'TEXT'
    JSON = 'JSON'