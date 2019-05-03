import os
from flask import Flask
from werkzeug.contrib.fixers import ProxyFix

from .config import config_by_name
from .db import db
from .security import jwt, bcrypt
from .api import blueprint as api_blueprint
from .public import blueprint as public_blueprint


def create_app(config_name='development'):
    print('create gateway', config_name)

    app = Flask(__name__, instance_relative_config=True)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    app.config.from_object(config_by_name[config_name])
    app.config.from_pyfile('config.py', silent=True)
    app.config.from_envvar('APP_CONFIG_FILE', silent=True)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    app.register_blueprint(api_blueprint, url_prefix='/api')
    app.register_blueprint(public_blueprint)

    @app.before_first_request
    def create_tables():
        db.create_all()

    return app
