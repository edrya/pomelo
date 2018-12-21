import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY',
                                '5a384f5f-170d-46c8-86fc-e65cf7f15da2')


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    THREADED = False


class ProductionConfig(Config):
    DEBUG = False
    THREADED = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
