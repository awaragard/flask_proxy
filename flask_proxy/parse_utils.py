import ast
import json
import os
import re
from datetime import datetime, timedelta
from traceback import TracebackException

from dateutil import parser

date_format = '%Y_%m_%d-%H.%M.%S'


def parse_type(value, as_type):
    try:
        if as_type == bool:
            return parse_bool(value)
        elif as_type == list:
            return parse_list(value)
        elif as_type == dict:
            return parse_dict(value)
        elif as_type == timedelta:
            return parse_time_delta(value)
        elif as_type == datetime:
            return parse_datetime(value)
        else:
            return as_type(value)
    except:
        raise TypeError("Error parsing '{0}' as type '{1}'".format(value, as_type))


def parse_datetime(date):
    if isinstance(date, datetime):
        return date
    if not isinstance(date, str):
        return TypeError("Cannot parse date '{0}' from type: {1}".
                         format(str(datetime), str(type(datetime))))
    return parser.parse(date)


def parse_bool(value):
    if not value:
        return False
    if isinstance(value, bool):
        return value
    if value in ["1", "0", 1, 0]:
        return str(value) == "1"
    elif value.lower() in ["true", "false"]:
        return value == "true"
    raise TypeError("Cannot cast: " + str(value) + " to boolean")


def parse_list(value):
    if isinstance(value, set):
        return list(value)
    else:
        return parse_collection(value, list)


def parse_dict(value):
    return parse_collection(value, dict)


def parse_collection(value, as_type):
    if value is None:
        return as_type()
    elif isinstance(value, as_type):
        return value
    else:
        try:
            value = value.decode()
        except:
            pass
        try:
            return json.loads(value)
        except:
            pass
        try:
            return ast.literal_eval(value)
        except:
            pass
    return as_type(value)


def parse_time_delta(value):
    if isinstance(value, timedelta):
        return value
    if value is not None:
        value = str(value)
        intervals = re.split('[(days, ):]+', value)
        if len(intervals) >= 3:
            d = float(intervals[0]) if len(intervals) == 4 else 0.0
            s = float(intervals[-1])
            m = float(intervals[-2])
            h = float(intervals[-3])
            value = timedelta(hours=h, minutes=m, seconds=s, days=d)
    return value


def correct_path(path):
    path = re.split('[/\\\\]+', path)
    return os.sep.join(path)


def timestamp(date=None):
    if date and not isinstance(date, datetime):
        return date
    return (date or datetime.now()).strftime(date_format)


def displaytime(date=None):
    if date and not isinstance(date, datetime):
        return date
    return (date or datetime.now()).strftime('%Y/%m/%d %H:%M:%S')


def decode(text, lower=False):
    if not text:
        return
    try:
        text = text.decode()
    except:
        pass

    text = str(text).strip()
    return text.lower() if lower else text


def as_list(obj):
    if not obj:
        return []
    if isinstance(obj, list):
        return obj
    elif isinstance(obj, set):
        return list(obj)
    return [obj]


def get_header(headers, key):
    dec = {decode(k, True): decode(v, True) for k, v in headers.items()}
    return dec.get(key)


def parse_body(request):
    file = request.files.get('file')
    if file and file.filename:
        data = decode(file.read())
        file.close()
    else:
        data = decode(request.data)
    if not data:
        raise AssertionError("No data was found in the request")
    return data


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
