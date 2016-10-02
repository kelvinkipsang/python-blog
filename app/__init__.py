from flask import Flask
from config import config
from flask.ext.bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask.ext.moment import Moment
from flask.ext.pagedown import PageDown


db = SQLAlchemy()
bootstrap = Bootstrap()      #create instance as a global var
moment = Moment()
pagedown = PageDown()

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'     #bprint and route showing login page

def create_app(config_name):                            #creating app in function
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    bootstrap.init_app(app)     #connecting extention with app ie bring features to app
    moment.init_app(app)
    pagedown.init_app(app)

    from api_1_0 import api as api_blueprints
    app.register_blueprint(api_blueprints, url_prefix='/api/1.0')

    from .auth import auth as auth_blueprints
    app.register_blueprint(auth_blueprints, url_prefix='/auth')     #prefix-ing all routes defined in bprint as /auth

    from .talks import talks as talks_blueprint
    app.register_blueprint(talks_blueprint)         #bring/import the routes from bprint to app

    return app


