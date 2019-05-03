#!/usr/bin/env python
import os
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from recyclus_gateway import create_app, db
from recyclus_gateway.security import auth
from recyclus_gateway.security.models import User, Token


app = create_app(os.getenv('FLASK_ENV') or 'production')

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def run():
    app.run(host='0.0.0.0', port=80,
            ssl_context=('/recyclus/certificates/hostcert.crt', '/recyclus/certificates/hostcert.key'))


@manager.command
def init():
    db.create_all()
    admin = User(username='admin', password='test')
    admin.save()
    auth.get_access_token(admin)
    auth.get_refresh_token(admin)


@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('testing', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    manager.run()
