from pqueue.redis_client import Redis
import time


class Task(object):

    def __init__(self, id=None, tasks=None):
        """
        :param id: integer which is used to identify the output of the task in redis
        :param tasks: list of Task, this Task depends on or None
        """

        assert isinstance(id, int)

        if tasks is None:
            # no subtasks
            tasks = []

        self.id = id
        self.tasks = tasks # these are the subtasks

    def run(self):
        """ This performs some calculation using the subtasks (if any), then store the output in Redis.
        """
        print("Running task {0}".format(self.id))
        print(time.sleep(5))

        # Run calculation
        if len(self.tasks) == 0:
            # No subtask, output = id
            value = self.id
        else:
            """ Add up output of the subtasks
            """
            value = 0

            for task in self.tasks:
                task_output = Redis.get_value(task.id)
                assert not task_output is None, "Missing task output for subtask {0}".format(task.id)
                value += int(task_output)

        # Save output in redis
        print("Setting value = {0} for task {0}".format(value, self.id))
        Redis.set_value(self.id, value)


class TaskGenerator(object):
    @classmethod
    def generate_tasks(self):
        """ This returns a list of tasks
        """
        tasks_level_1 = [Task(1), Task(2), Task(3), Task(4)]
        tasks_level_2 = [Task(5, tasks=tasks_level_1[0:2]), Task(6, tasks=tasks_level_1)]
        tasks_level_3 = [Task(7, tasks=tasks_level_1 + tasks_level_2)]
        tasks_level_4 = [Task(8, tasks=tasks_level_1 + tasks_level_2 + tasks_level_3)]

        return tasks_level_1 + tasks_level_2 + tasks_level_3 + tasks_level_4
