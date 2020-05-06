import requests
from flask import Blueprint, jsonify, Response, request

view = Blueprint('view', __name__, url_prefix='')


@view.route('/', methods=['GET'])
def home():
    x = jsonify("hello")
    return x

# http://dummy.restapiexample.com/api/v1/employees

def process_request(request, path):
    target = 'dummy.restapiexample.com'
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
    resp = requests.get(url, headers=headers)
    return process_response(resp)

@view.route('/<path:path>', methods=['POST'])
def post_dummy(path):
    url, headers = process_request(request, path)
    x = request.get_data()
    # Example:
    # https://medium.com/customorchestrator/simple-reverse-proxy-server-using-flask-936087ce0afb
    #resp = requests.get(url, headers=headers)
    return process_response(resp)
