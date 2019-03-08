import requests
import json

from flask import request, Response, stream_with_context, current_app as app, jsonify
from flask_restplus import Resource, Namespace
from flask_jwt_extended import jwt_required, get_jwt_claims

api = Namespace('services', description='services')

batch_server = 'http://batch:5010/api'
datastore_server = 'http://datastore:5020/api'


def forward(url, data, stream=False):
    try:
        resp = requests.request(
            method=request.method,
            url=url,
            headers={key: value for (key, value) in request.headers if key != 'Host'},
            data=data,
            cookies=request.cookies,
            allow_redirects=False,
            stream=stream)

        app.logger.debug('forward status_code: %s  [stream=%s]', resp.status_code, stream)

        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items()
                   if name.lower() not in excluded_headers]

        if stream:
            return Response(stream_with_context(resp.iter_content()), resp.status_code, content_type=resp.headers['content-type'])
        else:
            return Response(resp.content, resp.status_code, headers)
    except requests.exceptions.ConnectionError:
        return {'message': 'service not available'}, 502


def add_credentials_and_forward(server, path, stream=False):
    claims = get_jwt_claims()
    data = json.loads(request.data) if request.data else {}
    data['identity'] = {
        'user': claims['username'],
        'roles': claims['roles']
    }

    resp = forward(url=f'{server}/{path}', data=json.dumps(data), stream=stream)
    return resp


@api.route('batch/<path:path>')
class Batch(Resource):
    @jwt_required
    def get(self, path):
        return add_credentials_and_forward(batch_server, path)

    @jwt_required
    def post(self, path):
        return add_credentials_and_forward(batch_server, path)

    @jwt_required
    def delete(self, path):
        return add_credentials_and_forward(batch_server, path)


@api.route('datastore/<path:path>')
class Datastore(Resource):
    @jwt_required
    def get(self, path):
        return add_credentials_and_forward(datastore_server, path, stream=False)


