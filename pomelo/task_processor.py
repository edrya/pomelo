import multiprocessing
import json
from redis_client import Redis
from task import Task
import logging
import time

redis_client = Redis()


logging.basicConfig(filename='dispatcher.log', level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)


cpu_count = multiprocessing.cpu_count() - 1


class TaskProcessor:

    @classmethod
    def run(cls):
        cls._work()

    @staticmethod
    def _work():

        """This starts the worker loop to listen queue for a new tasks.
         If task exists it executes it.

         """

        print(f'Running with {cpu_count} processes!')
        processes = []
        while True:
            for w in range(cpu_count):
                p = multiprocessing.Process(target=TaskProcessor.do_work)
                processes.append(p)
                p.start()
            for p in processes:
                p.join()

            time.sleep(1)


    @staticmethod
    def do_work():
        task = redis_client.brpop(['pomelo:queue:task', 'queue:dep:task' ])

        # todo: create queue for processing
        redis_client.rpush('pomelo:queue:task:processing', task[1])

        task = json.loads(task[1])
        if task['tasks']:
            tasks = [Task(id=x) for x in task['tasks']]
            Task(id=task['id'], tasks=tasks).run()

        else:

            Task(id=task['id'], tasks=task['tasks']).run()


if __name__ == '__main__':
    logger.info(f'Start loops with {cpu_count}')
    TaskProcessor.run()
