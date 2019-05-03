from flask_restplus import Resource, Namespace
from flask_jwt_extended import ( get_raw_jwt,
                jwt_required, fresh_jwt_required, jwt_refresh_token_required)
from webargs.flaskparser import use_args, use_kwargs

from ..security import User, UserSchema, TokenSchema, auth

from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('auth', description='authentication services')


@api.route('/login')
class Login(Resource):
    @use_kwargs(UserSchema(only=('username', 'password')))
    def post(self, username, password):
        user = User.query.filter_by(username=username).first()
        if not user or not user.verify_password(password):
            return {'message': 'Bad username or password'}, 401

        access_token = auth.get_access_token(user, fresh=True)
        # refresh_token = auth.get_refresh_token(user)
        return { 'token': access_token }


@api.route('/logout')
class Logout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        auth.revoke_token(jti=jti)
        return {'status': 'success'}


@api.route('/token')
class Tokens(Resource):
    @jwt_required
    def get(self):
        identity = get_jwt_identity()
        all_tokens = auth.get_user_active_tokens(identity)
        return TokenSchema(many=True).dump(all_tokens)


@api.route('/token/refresh')
class Refresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        token = auth.get_access_token(current_user)
        return {'access_token': token}, 201


@api.route('/token/revoke/<token_id>')
class Revoke(Resource):
    @jwt_required
    def delete(self, token_id):
        identity = get_jwt_identity()
        auth.revoke_token(id=token_id, user_identity=identity)
        return {'message': 'revoked'}

