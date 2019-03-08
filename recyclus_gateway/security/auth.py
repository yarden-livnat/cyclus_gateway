from datetime import datetime
from flask import current_app
from flask_jwt_extended import (JWTManager,
                                create_access_token, create_refresh_token, decode_token)

from ..db import db
from .models import User, Token
from .exceptions import TokenNotFound

jwt = JWTManager()


def epoch_utc_to_datetime(epoch_utc):
    """
    Helper function for converting epoch timestamps (as stored in JWTs) into
    python datetime objects (which are easier to use with sqlalchemy).
    """
    return datetime.fromtimestamp(epoch_utc)


@jwt.user_identity_loader
def user_identify(user):
    return user.username if type(user) != str else user


@jwt.user_claims_loader
def add_claims(user):
    return {'username': user.username, 'roles': user.roles }


@jwt.user_loader_callback_loader
def jwt_identity(identity):
    return User.query.filter_by(username=identity).first()


@jwt.token_in_blacklist_loader
def check_if_token_revoked(decoded_token):
    return is_token_revoked(decoded_token)


def get_access_token(user, fresh=False):
    token = create_access_token(identity=user, fresh=fresh)
    save_token(token, current_app.config['JWT_IDENTITY_CLAIM'])
    return token


def get_refresh_token(user):
    token = create_refresh_token(identity=user)
    save_token(token, current_app.config['JWT_IDENTITY_CLAIM'])
    return token


def is_token_revoked(decoded_token):
    jti = decoded_token['jti']
    token = Token.query.filter_by(jti=jti).first()

    return token.revoked if token is not None else True


def revoke_token(**kwargs):
    token = Token.query.filter_by(**kwargs).first()
    if token is not None:
        token.update(revoked=True)
    else:
        raise TokenNotFound(f'Could not find token with {kwargs}')


def revoke_all(identity):
    for token in get_user_active_tokens(identity):
        token.delete(commit=False)
    db.session.commit()


def get_user_active_tokens(identity):
    return Token.query.filter_by(user_identity=identity, revoked=False).all()


def save_token(encoded_token, identity_claim):
    decoded_token = decode_token(encoded_token)
    token = Token(
        jti=decoded_token['jti'],
        token_type=decoded_token['type'],
        user_identity=decoded_token[identity_claim],
        expires=epoch_utc_to_datetime(decoded_token['exp']),
        revoked=False,
    )
    token.save()


def prune():
    now = datetime.now()
    expired = Token.query.filter(TokenBlacklist.expires < now).all()
    for token in expired:
        token.delete(commit=False)
    db.session.commit()
