from flask import Blueprint
from flask_restplus import Api
from flask import current_app as app
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
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
    app.logger.error(f'default error handler {str(error)}  {getattr(error, "code", -1)}')
    return {'message': str(error)}, getattr(error, 'code', 400)


@api.errorhandler(JWTExtendedException)
@api.errorhandler(TokenNotFound)
def handle_security_exception(error):
    '''Security exceptions handler'''
    return {'message': error.message}, 401


@api.errorhandler(ExpiredSignatureError)
def handle_expire_exception(error):
    app.logger.error('Signature expired')
    return {'message': 'Signature expired'}, 401


@api.errorhandler(InvalidSignatureError)
def handle_invalid_exception(error):
    app.logger.error(f'{str(error)} ')
    return {'message': 'Signature invalid'}, 401


