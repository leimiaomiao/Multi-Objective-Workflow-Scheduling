from config import constant
from model.Individual import Individual, IndividualTask
import random


class RandomAlgorithm(object):
    def __init__(self, workflow, bw_value):
        # 随机初始化种群
        self.individual_list = list()
        self.workflow = workflow
        self.name = "RANDOM"

        i = 0
        while i < constant.PARETO_RESULT_NUM:
            individual = Individual(self, i, workflow, bw_value)
            individual.schedule()
            self.individual_list.append(individual)
            i += 1

        self.max_id = len(self.individual_list) - 1

        # 初始化pareto解集
        self.pareto_result = self.individual_list

    def init_task_list_order_pos(self):
        # 任务排序初始化
        task_list_ordered = self.workflow.init_task_order()

        # 任务位置初始化
        individual_task_list = list()
        index = 0
        for task_id in task_list_ordered:
            task = self.workflow.get_task_by_id(task_id)
            individual_task = IndividualTask()
            individual_task.task = task
            individual_task.exec_sequence = index

            random_num = random.random()
            if random_num <= 0.5:
                individual_task.exec_pos = 0
            else:
                individual_task.exec_pos = 1

            individual_task_list.append(individual_task)
            index += 1
        return individual_task_list
