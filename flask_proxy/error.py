import logging
from datetime import datetime
from http import HTTPStatus
from traceback import TracebackException

from flask import jsonify
from werkzeug.exceptions import NotFound

class ApiError(Exception):
    status_code = 400
    __name__ = "ApiError"

    def __init__(self, message=None, error=None, status_code=None, chain=None, payload=None):
        Exception.__init__(self)
        if isinstance(error, Exception):
            self.error_msg = str(error)
            self.traceback = parse_exception(error)

            if chain:
                if isinstance(chain, list):
                    self.chain = [parse_exception(e) for e in chain]
                else:
                    self.chain = parse_exception(chain)
            try:
                self.error = type(error).__name__
            except:
                self.error = type(error)

        elif error:
            self.error = str(error)

        self.args = self.message = (message,)
        self.status_code = status_code
        self.payload = payload
        self.timestamp = datetime.now()

    def serialize(self):
        rv = dict(self.payload or ())

        if self.status_code:
            rv['status_code'] = str(self.status_code)
            rv['reply'] = HTTPStatus(self.status_code).phrase

        if self.message:
            rv['message'] = self.message

        if hasattr(self, 'chain'):
            rv['chain'] = self.chain

        if hasattr(self, 'error'):
            rv['error'] = self.error
            rv['error_message'] = self.error_msg
            rv['traceback'] = self.traceback
        rv['timestamp'] = self.timestamp.strftime('%Y/%m/%d %H:%M:%S')
        return rv


class VCRAssertionError(ApiError):
    pass


def parse_exception(exc, extra_msg=''):
    if not exc:
        return []
    exc_list = exc
    if isinstance(exc, Exception):
        tbe = TracebackException(type(exc), exc, exc.__traceback__)
        exc_list = tbe.format()
    lines = []
    for l in exc_list:
        lines.extend(l.split('\n'))
    lines.append(extra_msg)
    return list(map(
        lambda x: x.strip(), filter(lambda x: x, lines)))


class ErrorHandler:
    @classmethod
    def api_error_handler(cls, api_error):
        response = jsonify(api_error.serialize())
        response.status_code = api_error.status_code
        return response

    @classmethod
    def generic_error_handler(cls, error):
        """
        Unknown errors during API call
        Don't log/report simple 404 errors!
        """
        if isinstance(error, NotFound):
            status_code = 404
        else:
            status_code = 500
            logging.getLogger().error(error)
        api_err = ApiError(str(error), error, status_code)
        return cls.api_error_handler(api_err)


def register(view):
    @view.view.errorhandler(ApiError)
    def handle_error(error):
        return ErrorHandler.api_error_handler(error)

    @view.view.errorhandler(VCRAssertionError)
    def handle_error(error):
        return ErrorHandler.api_error_handler(error)

    @view.view.errorhandler(Exception)
    def handle_error(error):
        return ErrorHandler.generic_error_handler(error)
