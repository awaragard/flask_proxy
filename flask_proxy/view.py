import logging

from flask import Blueprint, jsonify

view = Blueprint('view', __name__, url_prefix='')



@view.route('/', methods=['GET'])
def home():
    logging.getLogger("TEST").info("XXXX")
    return jsonify("hello")


@view.route('/proxy', methods=['GET'])
def proxy_hello():
    return jsonify("proxy hello")
