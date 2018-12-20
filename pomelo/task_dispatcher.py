import os
import json
import time
import logging

from redis_client import Redis
from task import TaskGenerator

redis_client = Redis()


class TaskDispatcher:
    """Dispatches and coordinates tasks for processing using Redis with queues.

    dispatcher.log -  logs all events to the dispatcher.log

    """
    TIMEOUT = 10

    def __init__(self, connection=None, name='pomelo:queue:task'):

        self.connection = connection
        self.name = name
        self.tasks = None

    def run(self, tasks):
        self.tasks = tasks

        if tasks:
            self.dispatch()

    def dispatch(self):

        tasks = [self.prepare(task) for task in self.tasks]

        try:
            while tasks:
                for idx, task in enumerate(tasks):
                    if not task['tasks']:
                        self.enqueue(task)
                        tasks.pop(idx)
                    else:
                        if self.enqueue_ready(task):
                            self.enqueue(task)
                            tasks.pop(idx)

                time.sleep(1)

        except KeyboardInterrupt:
            print('Shutdown requested...deleting all the keys of the currently selected DB')
            self.connection.flush_db()

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

#
# class PomeloQueue:
#
#     def __init__(self, connection=None, name='pomelo:queue:task'):
#         self.connection = connection
#         self.name = name
#
#     def enqueue(self, body):
#         self.connection.rpush(self.name, json.dumps(body))


def main():
    logger.info(f'loading tasks to redis')
    redis_client.flush_db()

    tasks = TaskGenerator.generate_tasks()
    TaskDispatcher(connection=redis_client).run(tasks)


if __name__ == '__main__':

    logging.basicConfig(filename='dispatcher.log', level=logging.INFO, format='%(asctime)s - %(message)s',
                        datefmt='%H:%M:%S')
    logger = logging.getLogger(__name__)

    main()
