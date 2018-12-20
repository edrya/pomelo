import multiprocessing
import json
from redis_client import Redis
from task import Task
import logging
import time

redis_client = Redis()

cpu_count = multiprocessing.cpu_count() - 1


class TaskProcessor:
    """Listening for tasks from redis.
    Workers will read jobs from the given queues
     in an endless loop, waiting for new work to arrive when all jobs are done.
    """

    def __init__(self, connection=None, name='pomelo:queue:task'):

        self.connection = connection
        self.name = name
        self.tasks = None

    def run(self):
        self.work()

    @staticmethod
    def work():

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

            time.sleep(100)

    @staticmethod
    def do_work():
        task = redis_client.brpop(['pomelo:queue:task', 'queue:dep:task'])

        # todo: create queue for processing
        redis_client.rpush('pomelo:queue:task:processing', task[1])

        task = json.loads(task[1])
        if task['tasks']:
            tasks = [Task(id=x) for x in task['tasks']]
            Task(id=task['id'], tasks=tasks).run()

        else:

            Task(id=task['id'], tasks=task['tasks']).run()


def main():
    logger.info(f'Start loops with {cpu_count} processors')
    TaskProcessor(connection=redis_client, name='pomelo:queue:task').run()


if __name__ == '__main__':
    logging.basicConfig(filename='processor.log', filemode='w', level=logging.INFO, format='%(asctime)s - %(message)s',
                        datefmt='%H:%M:%S')
    logger = logging.getLogger(__name__)

    main()
