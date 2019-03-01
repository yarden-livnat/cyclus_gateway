"""Application configuration."""
import os
from pathlib import Path
from datetime import timedelta

db_dir = Path('.').parent.resolve()


class Config(object):
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', None)
    BCRYPT_LOG_ROUNDS = 13
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_TOKEN_LOCATION = ['headers'] #'cookies']

    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

    # JWT_ACCESS_COOKIE_PATH = '/api/'
    # JWT_REFRESH_COOKIE_PATH = '/token/refresh'


class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True
    DB_NAME = 'dev.db'
    SQLALCHEMY_DATABASE_URI = f'sqlite:////data/gateway_dev.db'

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    # Only allow JWT cookies to be sent over https.
    JWT_COOKIE_SECURE = False

    # Disable CSRF protection for this example. In almost every case,
    # this is a bad idea. See examples/csrf_protection_with_cookies.py
    # for how safely store JWTs in cookies
    JWT_COOKIE_CSRF_PROTECT = False


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4

    SQLALCHEMY_DATABASE_URI = f'sqlite:////data/gateway_test.db'
    PRESERVE_CONTEXT_ON_EXCEPTION = False

    # Only allow JWT cookies to be sent over https.
    JWT_COOKIE_SECURE = False

    # Disable CSRF protection for this example. In almost every case,
    # this is a bad idea. See examples/csrf_protection_with_cookies.py
    # for how safely store JWTs in cookies
    JWT_COOKIE_CSRF_PROTECT = False


class ProductionConfig(Config):
    ENV = 'production'
    DEBUG = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_COOKIE_SECURE = False


config_by_name = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    production=ProductionConfig
)