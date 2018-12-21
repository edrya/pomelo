import os
from flask import Flask
from pq.redis_client import Redis
from pq.task import TaskGenerator
from pq.run_task_dispatcher import TaskDispatcher

from config import config


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLACK_CONFIG', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    app.redis_connection = Redis()
    app.task_generator = TaskGenerator

    app.task_dispatcher = TaskDispatcher(connection=app.redis_connection)


    # Register pomelo routes
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app
