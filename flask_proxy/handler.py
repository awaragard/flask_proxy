import logging

from flask import jsonify
from werkzeug.exceptions import NotFound

from flask_proxy.error import ApiError


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

    @view.view.errorhandler(Exception)
    def handle_error(error):
        return ErrorHandler.generic_error_handler(error)
