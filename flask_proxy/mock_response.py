import json

from flask import Response


class MockResponse:
    def __init__(self, endpoint=None, status_code=200, method='GET', body=None, headers=None):
        self.endpoint = endpoint
        self.status_code = status_code
        self.method = method
        self.body = body or {}
        self.headers = headers or {}

    def to_flask_response(self):
        return Response(
            json.dumps(self.body),
            self.status_code,
            self.headers
        )
