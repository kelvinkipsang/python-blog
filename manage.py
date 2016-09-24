import os
from app import create_app
from flask_script  import Manager

app = create_app(os.getenv('FLASK_CONFIG') or 'default') #get environment configuration if set else use default configuration(DevelopmentConfig)
manager = Manager(app)

if __name__ == '__main__':
    manager.run()