import os

class Config:
    SECRET_KEY =os.environ.get("SECRET_KEY")    # obtaining key from environment

class DevelopmentConfig(Config):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "top secret key"   #if it isnt set in environment

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    pass
#dictionary placing configs in an easy to use structure
config{
    'development': DevelopmentConfig,
    'testing':TestingConfig,
    'production':ProductionConfig,

    'default': DevelopmentConfig
}