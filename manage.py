#!/usr/bin/env python
import os
if os.path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

from app import create_app
from flask_script import Manager
from app import db
from app.models import User

app = create_app(os.getenv('FLASK_CONFIG') or 'default')    #get environment configuration if set else use default configuration(DevelopmentConfig)
manager = Manager(app)

@manager.command
def test():
    from subprocess import call
    call(['nosetests', '-v',
          '--with-coverage', '--cover-package=app', '--cover-branches',
          '--cover-erase', '--cover-html', '--cover-html-dir=cover'])

@manager.command
def adduser(email, username, admin=False):      #creates new command using flsk script,using name of fnt,checks arg with no default become positional args
    """Register a new user."""
    from getpass import getpass
    password = getpass()                    #prompt to get pass (from standard module getpass)
    password2 = getpass(prompt='Confirm: ')
    if password != password2:
        import sys
        sys.exit('Error: passwords do not match.')
    db.create_all()
    user = User(email=email, username=username, password=password,
                is_admin=admin)                 
    db.session.add(user)         #add to session,like a db handle
    db.session.commit()          #call that makes changes effective
    print('User {0} was registered successfully.'.format(username))


if __name__ == '__main__':
    manager.run()
