import urllib.parse
import re
import requests
from flask import Blueprint, jsonify, Response, request
from vcr.errors import CannotOverwriteExistingCassetteException, UnhandledHTTPRequestError

from flask_proxy.error import ApiError, VCRAssertionError

view = Blueprint('view', __name__, url_prefix='')
logger = None
proxy_server = None


# noinspection PyUnresolvedReferences
def generate_cassette_name(url, request):
    name = urllib.parse.quote_plus(proxy_server.base_url + request.full_path)
    try:
        data = request.data.decode()
        if data:
            data = urllib.parse.quote_plus(data)
            name += data[:45] + data[-20] + "-" + str(len(data))
    except:
        logger.warning("Failed to create cassette filename for {} with data - taking URL only!".format(url))
        pass
    return name


# noinspection PyUnresolvedReferences
def build_request(request):
    target = proxy_server.base_url
    for k,v in proxy_server.base_url_dict.items():
        if re.search(k, request.full_path):
            target = v
            break
    headers = dict(request.headers)
    headers['Host'] = target
    url = '{0}://{1}/{2}'.format(proxy_server.protocol, target, request.full_path)
    return url, headers


def build_response(response):
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in response.raw.headers.items() if name.lower() not in excluded_headers]
    return Response(response.content, response.status_code, headers)


@view.route('/<path:path>', methods=['GET'])
def get(path):
    try:
        url, headers = build_request(request)
        resp = make_call(url, headers=headers, cassette='get-{}.yml'
                         .format(generate_cassette_name(url, request)))
        return build_response(resp)
    except (CannotOverwriteExistingCassetteException, UnhandledHTTPRequestError) as e:
        raise VCRAssertionError("VCR assertion failed", e, status_code=417)
    except Exception as e:
        raise ApiError("Unhandled exception occured", e, status_code=500)


@view.route('/<path:path>', methods=['POST'])
def post(path):
    try:
        url, headers = build_request(request)
        resp = make_call(url, method='POST', headers=headers,
                         body=request.data, cassette='post-{}.yml'
                         .format(generate_cassette_name(url, request)))
        return build_response(resp)
    except (CannotOverwriteExistingCassetteException, UnhandledHTTPRequestError) as e:
        raise VCRAssertionError("VCR assertion failed", e)
    except Exception as e:
        raise ApiError("Unhandled exception occured", e, status_code=500)


@view.route('/ping', methods=['GET'])
def ping():
    return jsonify("alive")


# noinspection PyUnresolvedReferences
@view.route('/shutdown', methods=['GET'])
def shutdown_server():
    logger.warning("Server will shut down")
    request.environ.get('werkzeug.server.shutdown')
    return jsonify('shutting down')


# noinspection PyUnresolvedReferences
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
    if proxy_server.vcr_enabled:
        with proxy_server.vcr.use_cassette(cassette):
            return call()
    return call()
