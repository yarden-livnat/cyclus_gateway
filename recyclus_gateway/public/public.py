from flask_restplus import Resource, Namespace

api = Namespace('', description='public')


@api.route('/')
class Index(Resource):

    def get(self):
        return "Recylus main page"


@api.route('/register')
class Register(Resource):

    def get(self):
        return 'register'
