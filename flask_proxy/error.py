from datetime import datetime
from http import HTTPStatus
from traceback import TracebackException

def displaytime(date=None):
    if date and not isinstance(date, datetime):
        return date
    return (date or datetime.now()).strftime('%Y/%m/%d %H:%M:%S')

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
        rv['timestamp'] = displaytime(self.timestamp)
        return rv

class VCRAssertionFailure(Exception):
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

