import logging

import requests
from flask import Blueprint, jsonify, Response, request
from qconf import decode

from flask_proxy.config import ProxyConfig
from flask_proxy.error import ApiError, VCRAssertionFailure
from vcr.errors import CannotOverwriteExistingCassetteException, UnhandledHTTPRequestError

view = Blueprint('view', __name__, url_prefix='')
proxy_opts = ProxyConfig()
logger = logging.getLogger()


@view.route('/', methods=['GET'])
def home():
    return jsonify("hello")


def build_request(request, path):
    target = proxy_opts.base_url
    headers = dict(request.headers)
    headers['Host'] = target
    url = '{0}://{1}/{2}'.format(proxy_opts.protocol, target, path)
    return url, headers


def build_response(response):
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in response.raw.headers.items() if name.lower() not in excluded_headers]
    return Response(response.content, response.status_code, headers)


@view.route('/<path:path>', methods=['GET'])
def get(path):
    url, headers = build_request(request, path)
    resp = make_call(url, headers=headers, cassette='getreq.yaml')
    return build_response(resp)


@view.route('/<path:path>', methods=['POST'])
def post(path):
    try:
        url, headers = build_request(request, path)
        resp = make_call(url, method='POST', headers=headers, body=request.data, cassette='postreq.yaml')
        return build_response(resp)
    except (CannotOverwriteExistingCassetteException, UnhandledHTTPRequestError) as e:
        raise VCRAssertionFailure("VCR assertion failed", e)
    except Exception as e:
        raise ApiError("Unhandled exception occured", e, status_code=500)


def make_call(url, method='GET', body=None, headers=None, auth=None, cassette=None):
    request_params = {'url': url}

    if auth:
        request_params['auth'] = auth
    if headers:
        request_params['headers'] = headers
    if body:
        request_params['data'] = body

    if method == 'POST':
        def call():
            return requests.post(**request_params)
    elif method == 'DELETE':
        def call():
            return requests.delete(**request_params)
    else:
        def call():
            return requests.get(**request_params)

    if proxy_opts.vcr_enabled:
        with proxy_opts.vcr.use_cassette(cassette):
            return call()
    return call()
