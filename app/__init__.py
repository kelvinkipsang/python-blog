from flask import Flask
from config import config
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
bootstrap =Bootstrap()      #create instance as a global var

def create_app(config_name):                            #creating app in function
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    bootstrap.init_app(app)     #connecting extention with app ie bring features to app

    from .auth import auth as auth_blueprints
    app.register_blueprint(auth_blueprints, url_prefix='/auth')     #prefix-ing all routes defined in bprint as /auth

    from .talks import talks as talks_blueprint
    app.register_blueprint(talks_blueprint)         #bring/import the routes from bprint to app

    return app


