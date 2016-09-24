from flask import Flask
from config import config

def create_app(config_name):                            #creating app in function
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    from .talks import talks as talks_blueprint
    app.register_blueprint(talks_blueprint)         #bring the routes from bprint to app

    return app