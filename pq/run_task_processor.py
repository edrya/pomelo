"""
This script creates a worker that repeatedly picks up tasks from a redis queue and executes it.

It blocks the connection when there are no tasks left in the queue.



run_task_processor.py

Amir Edry
"""

import multiprocessing
import logging
import psutil
import os
import json
from redis_client import Redis
from task import Task


class TaskProcessor:
    """Creates multiple processes to execute tasks."""

    def __init__(self, connection, num_processors=1, name='pomelo:queue:task'):

        self.connection = connection
        self.task_queue = name
        self.processors = num_processors

    def run(self):
        self.create_processes()

    def create_processes(self):
        """This method creates the workers that pick up the tasks."""

        print(f'Parent process id: {os.getpid()}')
        logger.info(f'Parent process id: {os.getpid()}')

        processes = []
        for _ in range(self.processors):

            process = multiprocessing.Process(target=self.worker)
            # process.daemon = True
            process.start()
            processes.append(process)
        for p in processes:
            p.join()

    def worker(self):
        """The worker executes an infinite loop, and in each iteration it tries to retrieve a
        task from the task's queue."""

        print(f'Child process id: {os.getpid()}')
        logger.info(f'Child process id: {os.getpid()}')
        while True:
            self.execute()

    def execute(self):
        """Invokes the task by calling the task's run() method"""

        task = self.dequeue()

        task.run(self.connection)

    def dequeue(self):
        """Removes task from the tail's queue and return a Task object"""

        task = self.connection.brpop(['pomelo:queue:task'])
        task = json.loads(task[1])
        if task:
            logger.info(f"Picked up task with id {task['id']} from {self.task_queue}")

        depends_on = task.get('tasks')

        if depends_on:
            tasks = [Task(id=t) for t in task['tasks']]

            return Task(id=task['id'], tasks=tasks)

        return Task(id=task['id'], tasks=depends_on)


def main():
    redis_connection = Redis()
    cpu_count = multiprocessing.cpu_count()

    # by default the task processor will start with 1 worker
    # replace with cpu_count to use all available core

    num_worker = 4
    logger.info(f'Starting worker with {num_worker} processor')

    print(f'Starting worker with {num_worker} processor')
    TaskProcessor(redis_connection, num_processors=num_worker, name='pomelo:queue:task').run()


if __name__ == '__main__':

    logging.basicConfig(filename='processor.log', filemode='w', level=logging.INFO, format='%(asctime)s: %(message)s',
                        datefmt='%H:%M:%S')
    logger = logging.getLogger(__name__)

    main()
