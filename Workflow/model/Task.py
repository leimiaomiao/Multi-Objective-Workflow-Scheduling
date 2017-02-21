import random
from config import constant


class Task(object):
    def __init__(self, task_id, pre_task_id_list, suc_task_id_list):
        self.task_id = task_id
        self.pre_task_id_list = pre_task_id_list
        self.suc_task_id_list = suc_task_id_list

        self.work_load = random.randint(constant.MIN_WORKLOAD_NUM, constant.MAX_WORKLOAD_NUM)
        # size of the task's output
        self.output = random.randint(constant.MIN_OUTPUT_NUM, constant.MAX_OUTPUT_NUM)

        self.excu_time = None
        self.start_time = None
        self.end_time = None
        self.span_time = None
        self.transmission_time = None
        self.energy = None

    @property
    def workload(self):
        return self.work_load

    @workload.setter
    def workload(self, value):
        self.work_load = value

    def print(self):
        print((self.task_id, self.pre_task_id_list, self.suc_task_id_list, self.work_load, self.start_time,
               self.end_time))
