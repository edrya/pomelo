import os
import json
import time
import logging

from pqueue.redis_client import Redis
from pqueue.task import TaskGenerator

redis_client = Redis()


class TaskDispatcher:
    """Dispatches and coordinates tasks for processing using Redis with queues.

    dispatcher.log -  logs all events to the dispatcher.log

    """
    TIMEOUT = 100

    def __init__(self, connection=None, name='pomelo:queue:task'):

        self.connection = connection
        self.name = name
        self.tasks = None

    def run(self, tasks):

        self.tasks = tasks

        if tasks:
            tasks = [self.prepare(task) for task in self.tasks]

            while tasks:
                if self.dispatch(tasks):
                    continue
                else:
                    break

    def dispatch(self, tasks):

        try:
            for t in tasks:
                if not t['tasks']:
                    self.enqueue(t)
                    tasks.remove(t)
                else:
                    if self.enqueue_ready(t):
                        self.enqueue(t)
                        tasks.remove(t)

        except KeyboardInterrupt:
            print('Program interrupted by user. Shutting down...'
                  'deleting all the keys of the currently selected DB')
            logger.info('Program interrupted by user. Shutting down...'
                        'deleting all the keys of the currently selected DB')

            return False

        return True

    def enqueue(self, body):
        self.connection.rpush(self.name, json.dumps(body))
        return True

    @staticmethod
    def prepare(task_obj):
        """This prepare task for enqueuing.

        :returns encoded value using json.dumps
        """
        tid = task_obj.id
        depends_on = task_obj.tasks

        return {'id': tid, 'tasks': [t.id for t in depends_on]}

    def enqueue_ready(self, task):

        depends_on = task['tasks']
        values = []

        for tid in depends_on:
            if self.connection.get_value(tid):
                values.append(redis_client.get_value(tid))

        if len(values) == len(depends_on):
            return True
        else:
            return False


def main():
    redis_client.flush_db()
    tasks = TaskGenerator.generate_tasks()
    logger.info(f'Started dispatcher with {len(tasks)} tasks')
    TaskDispatcher(connection=redis_client).run(tasks)


if __name__ == '__main__':
    logging.basicConfig(filename='dispatcher.log', filemode='w', level=logging.INFO, format='%(asctime)s - %(message)s',
                        datefmt='%H:%M:%S')
    logger = logging.getLogger(__name__)

    main()
