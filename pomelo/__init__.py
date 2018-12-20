import os
from flask import Flask

from config import config


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLACK_CONFIG', 'development')
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Register pomelo routes
    from .pomelo import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
