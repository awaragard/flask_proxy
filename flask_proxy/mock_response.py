import json

from flask import Response


class MockResponse:
    def __init__(self, rpath=None, status_code=200, body=None, headers=None):
        self.rpath = rpath
        self.status_code = status_code
        self.body = body or {}
        self.headers = headers or {}

    def to_flask_response(self):
        return Response(
            json.dumps(self.body),
            self.status_code,
            self.headers
        )



# p1 = MockResponse('/ims/exchange/jwt', body={
#             'expires_in': 10000,
#             'access_token': "x"
#         })




#
# opts['mock_response_dict'] = {
#                                  '/ims/exchange/jwt': ""{
#         'status_code': 200,
#         'body': {
#             'expires_in': 10000,
#             'access_token': "x"
#         }
#     },
# }
