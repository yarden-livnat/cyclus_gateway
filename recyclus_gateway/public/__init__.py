from flask import Blueprint
from flask_restplus import Api

from .public import api as public_api

blueprint = Blueprint('', __name__)

api = Api(blueprint,
          title='Recyclus Gateway',
          version='1.0',
          description='Remote cyclus services',
          doc='/doc/')

api.add_namespace(public_api)