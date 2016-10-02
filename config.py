import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY =os.environ.get("SECRET_KEY")    # obtaining key from environment
    TALKS_PER_PAGE = 50
    COMMENTS_PER_PAGE = 100

class DevelopmentConfig(Config):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "top secret key"   #if it isnt set in environment
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')         #setting paths to dbs

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

class ProductionConfig(Config):
    pass
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

#dictionary placing configs in an easy to use structure
config = {
    'development': DevelopmentConfig,
    'testing':TestingConfig,
    'production':ProductionConfig,

    'default': DevelopmentConfig
}

