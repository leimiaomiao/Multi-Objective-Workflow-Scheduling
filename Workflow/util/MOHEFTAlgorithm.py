from model.Individual import Individual, IndividualTask
from config import constant
import copy
from util.CrowdingDistanceAlgorithm import CrowdingDistanceAlgorithm


class MOHEFTAlgorithm(object):
    def __init__(self, workflow, bw_value):
        self.name = "MOHEFT"
        self.workflow = workflow
        self.bw_value = bw_value

        self.individual = Individual(self, 0, workflow, bw_value)

        self.pareto_result = list()

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

            # 执行位置初始化为0，代表在移动设备上
            individual_task.exec_pos = 0
            individual_task_list.append(individual_task)
            index += 1

        return individual_task_list

    def process(self):
        k = constant.PARETO_RESULT_NUM

        # 记录当前的pareto列表，元素为一个individual_task的列表
        result = list()
        individual_id = 0

        for individual_task in self.individual.individual_task_list:
            task_temp_1 = copy.deepcopy(individual_task)
            task_temp_1.exec_pos = 0

            task_temp_2 = copy.deepcopy(individual_task)
            task_temp_2.exec_pos = 1

            to_select_list = list()
            if len(result) > 0:
                for individual in result:
                    individual_temp_1 = copy.deepcopy(individual)
                    individual_temp_1.individual_id = individual_id

                    individual_temp_1.individual_task_list.append(task_temp_1)

                    individual_temp_1.schedule()
                    to_select_list.append(individual_temp_1)

                    individual_id += 1
                    individual_temp_2 = copy.deepcopy(individual)
                    individual_temp_2.individual_id = individual_id

                    individual_temp_2.individual_task_list.append(task_temp_2)

                    individual_temp_2.schedule()
                    to_select_list.append(individual_temp_2)

                    individual_id += 1
            else:
                individual_temp_1 = copy.deepcopy(self.individual)
                individual_temp_1.individual_id = individual_id
                individual_temp_1.individual_task_list = [task_temp_1]
                individual_temp_1.schedule()
                to_select_list.append(individual_temp_1)

                individual_id += 1

                individual_temp_2 = copy.deepcopy(self.individual)
                individual_temp_2.individual_id = individual_id
                individual_temp_2.individual_task_list = [task_temp_2]
                individual_temp_2.schedule()
                to_select_list.append(individual_temp_2)

                individual_id += 1

            crowding_distance_algorithm = CrowdingDistanceAlgorithm()
            result = crowding_distance_algorithm.individual_select_by_crowding_distance(to_select_list, k)

        self.pareto_result = result

        # print(len(self.pareto_result))
        # for result in self.pareto_result:
        #     result.print()
        #     result.print_results()
        #     print("=============")
