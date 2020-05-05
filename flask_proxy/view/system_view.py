import os

from flask import Blueprint, jsonify

from ust_proxy.config import Logging
from ust_proxy.error import ApiError

system_view = Blueprint('system_view', __name__, url_prefix='')
local_logs = ""



@system_view.route('/', methods=['GET'])
def home():
    Logging.get_logger("TEST").info("XXXX")
    return jsonify("hello")


@system_view.route('/logs/<filename>', methods=['GET'])
def get_local_log(filename):
    try:
        return jsonify(read_log(os.path.join(local_logs, filename)))
    except Exception as e:
        raise ApiError("Error, no logs for '"
                       + filename + "' could be found!", e, status_code=404)


def read_log(filename):
    short_name = filename.split(os.sep)[-1]
    data = ["Log data for: " + short_name, "---------------------------------"]
    with open(filename, 'r') as log:
        data.extend([l.rstrip('\n') for l in log.readlines()])
    return data
