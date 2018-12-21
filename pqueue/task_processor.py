import multiprocessing
import json
from pqueue.redis_client import Redis
from pqueue.task import Task
import logging

import time
import os
import psutil

redis_client = Redis()

cpu_count = multiprocessing.cpu_count() - 1


class TaskProcessor:
    """Listening for tasks from redis.
    Workers will read jobs from the given queues
     in an endless loop, waiting for new work to arrive when all jobs are done.
    """

    def __init__(self, connection=None, processes=1, name='pomelo:queue:task'):

        self.connection = connection
        self.name = name
        self.tasks = None
        self.processes = processes

    def run(self):

        try:
            while True:
                worker = self.get_worker(self.execute)
                print(worker.is_alive())
                print(psutil.Process())
                worker.start()
                worker.join()
                print(worker.is_alive())

        except KeyboardInterrupt:
            print('Program interrupted by user. Terminating process...')

            logger.info('Program interrupted by user. Terminating process...')

    @staticmethod
    def get_worker(target):
        """Initialize the process with the function we wish to call/"""
        return multiprocessing.Process(target=target)

    def execute(self):
        """Invokes the task by calling the task's run() method"""
        task = self.dequeue()
        task.run()
        return task.run()

    def dequeue(self):
        """Removes task from the tail's queue and return a Task object"""

        task = redis_client.brpop(['pomelo:queue:task'])
        task = json.loads(task[1])

        depends_on = task.get('tasks')

        if depends_on:
            tasks = [Task(id=t) for t in task['tasks']]

            return Task(id=task['id'], tasks=tasks)

        return Task(id=task['id'], tasks=depends_on)


def main():
    logger.info(f'Start with 1 processor')
    TaskProcessor(connection=redis_client, name='pomelo:queue:task').run()


if __name__ == '__main__':

    logging.basicConfig(filename='processor.log', filemode='w', level=logging.INFO, format='%(asctime)s - %(message)s',
                        datefmt='%H:%M:%S')
    logger = logging.getLogger(__name__)

    main()
