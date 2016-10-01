from flask import Flask
from config import config
from flask.ext.bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask.ext.moment import Moment


db = SQLAlchemy()
bootstrap = Bootstrap()      #create instance as a global var
moment = Moment()

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'     #bprint and route showing login page

def create_app(config_name):                            #creating app in function
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    bootstrap.init_app(app)     #connecting extention with app ie bring features to app
    moment.init_app(app)

    from .auth import auth as auth_blueprints
    app.register_blueprint(auth_blueprints, url_prefix='/auth')     #prefix-ing all routes defined in bprint as /auth

    from .talks import talks as talks_blueprint
    app.register_blueprint(talks_blueprint)         #bring/import the routes from bprint to app

    return app


