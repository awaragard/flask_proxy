import requests
from flask import Blueprint, jsonify, Response, request
import vcr
from qconf import QConfig

view = Blueprint('view', __name__, url_prefix='')
options = QConfig({})

global my_vcr


def init_vcr():
    global my_vcr

    my_vcr = vcr.VCR(
        cassette_library_dir = options.get_string("cassette_dir"),
        record_mode= options.get_string("record_mode"),
        match_on=['uri', 'method', 'raw_body']
    )


@view.route('/', methods=['GET'])
def home():
    x = jsonify("hello")
    return x


# http://dummy.restapiexample.com/api/v1/employees

def process_request(request, path):
    target = options.get_string("request_base_url")
    headers = dict(request.headers)
    headers['Host'] = target
    url = 'http://{}/{}'.format(target, path)
    return url, headers


def process_response(response):
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in response.raw.headers.items() if name.lower() not in excluded_headers]
    return Response(response.content, response.status_code, headers)


@view.route('/<path:path>', methods=['GET'])
def get_dummy(path):
    url, headers = process_request(request, path)
    with my_vcr.use_cassette('synopsis2.yaml'):
        resp = requests.get(url, headers=headers)
    return process_response(resp)


@view.route('/<path:path>', methods=['POST'])
def post_dummy(path):
    url, headers = process_request(request, path)
    with my_vcr.use_cassette('synopsis.yaml'):
        resp = requests.post(url, headers=headers, json=request.get_json())
    return process_response(resp)
