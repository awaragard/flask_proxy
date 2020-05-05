from flask import Blueprint, jsonify

from ust_proxy.config import Logging

proxy_view = Blueprint('proxy_view', __name__, url_prefix='')

logger = Logging.get_logger("proxy")


@proxy_view.route('/proxy', methods=['GET'])
def proxy_hello():
    return jsonify("proxy hello")
