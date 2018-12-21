import os
from flask import Flask, request, current_app
from pqueue.redis_client import Redis
from pqueue.task import TaskGenerator, Task
from pqueue.task_dispatcher import TaskDispatcher
from pqueue.task_processor import TaskProcessor

from config import config


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLACK_CONFIG', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    app.redis_connection = Redis()
    app.task_generator = TaskGenerator()

    app.TaskDispatcher = TaskDispatcher
    app.TaskProcessor = TaskProcessor




    # Register pomelo routes
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app
