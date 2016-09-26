import os
from flask_script import Manager
from app import create_app, db

from app.models import User

app = create_app(os.getenv('FLASK_CONFIG') or 'default') #get environment configuration if set else use default configuration(DevelopmentConfig)
manager = Manager(app)

if __name__ == '__main__':
    manager.run()

@manager.command
def adduser(email, username, admin=False):      #creates new command using flsk script,using name of fnt,checks arg with no default become positional args
    """Register a new user."""
    from getpass import getpass
    password = getpass()                           #prompt to get pass
    password2 = getpass(prompt='Confirm: ')
    if password != password2:
        import sys
        sys.exit('Error: passwords do not match.')
    db.create_all()
    user = User(email=email, username=username, password=password,
                is_admin=admin)
    db.session.add(user)
    db.session.commit()
    print('User {0} was registered successfully.'.format(username))
