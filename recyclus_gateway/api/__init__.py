from flask import Blueprint
from flask_restplus import Api

from jwt.exceptions import ExpiredSignatureError
from flask_jwt_extended.exceptions import JWTExtendedException
from ..security.exceptions import TokenNotFound

from .admin import api as admin_api
from .auth import api as auth_api
from .services import api as services_api

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='Recyclus API Gateway',
          version='1.0',
          description='Remote cyclus services api',
          doc='/doc/')


api.add_namespace(admin_api)
api.add_namespace(auth_api)
api.add_namespace(services_api, path='/')

@api.errorhandler
def default_error_handler(error):
    '''Default error handler'''
    return {'message': str(error)}, getattr(error, 'code', 500)


@api.errorhandler(JWTExtendedException)
@api.errorhandler(TokenNotFound)
def handle_security_exception(error):
    '''Security exceptions handler'''
    return {'message': error.message}, 400


@api.errorhandler(ExpiredSignatureError)
def handle_expire_exception(error):
    return {'message': 'Signature expired'}, 400
