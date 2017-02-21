from config import constant
from model.Individual import Individual, IndividualTask
import random
import copy
from util.CrowdingDistanceAlgorithm import CrowdingDistanceAlgorithm
from util.ParetoAlgorithm import ParetoAlgorithm


class GeneticAlgorithm(object):
    # 遗传算法初始化，bw_value为当前带宽环境
    paretoAlgorithm = ParetoAlgorithm()

    def __init__(self, workflow, bw_value, delta=constant.USR_MAX_DELAY_TOLERANCE):
        # 随机初始化种群
        self.individual_list = list()
        self.workflow = workflow
        self.delta = delta

        if self.delta == 0:
            name = "MOWS_%s" % self.delta
        else:
            name = "MOWS_DTM_%s" % self.delta
        self.name = name

        i = 0
        while i < constant.INDIVIDUAL_NUM:
            individual = Individual(self, i, workflow, bw_value, delta)
            individual.schedule()
            self.individual_list.append(individual)
            i += 1

        self.max_id = len(self.individual_list) - 1

        # 初始化pareto解集
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

            random_num = random.random()
            if random_num <= 0.5:
                individual_task.exec_pos = 0
            else:
                individual_task.exec_pos = 1

            individual_task_list.append(individual_task)
            index += 1
        return individual_task_list

    def individual_crossover(self, individual1, individual2):
        individual_1, individual_2 = self.individual_task_pos_crossover(individual1, individual2)
        individual_1, individual_2 = self.individual_task_sequence_crossover(individual_1, individual_2)
        return individual_1, individual_2

    def individual_mutate(self, individual):
        individual_new = self.individual_task_pos_mutate(individual)
        individual_new = self.individual_task_sequence_mutate(individual_new)
        return individual_new

    @staticmethod
    def individual_task_pos_crossover(individual1, individual2):
        crossover_pos = random.randint(1, len(individual1.individual_task_list) - 2)
        # print(crossover_pos)

        index = crossover_pos
        individual_1 = copy.deepcopy(individual1)
        individual_2 = copy.deepcopy(individual2)

        while index < len(individual_1.individual_task_list):
            individual_task_1 = individual_1.individual_task_list[index]
            individual_task_2 = individual_2.individual_task_list[index]

            temp = individual_task_1.exec_pos
            individual_task_1.exec_pos = individual_task_2.exec_pos
            individual_task_2.exec_pos = temp

            index += 1

        return individual_1, individual_2

    @staticmethod
    def individual_task_sequence_crossover(individual1, individual2):
        crossover_pos = random.randint(1, len(individual1.individual_task_list) - 2)

        # print(crossover_pos)

        individual1_temp = copy.deepcopy(individual1)
        individual2_temp = copy.deepcopy(individual2)

        individual1_temp.individual_task_list = individual1_temp.individual_task_list[:crossover_pos]
        individual2_temp.individual_task_list = individual2_temp.individual_task_list[:crossover_pos]

        for individual_task in individual2.individual_task_list:
            exist = False
            for task in individual1_temp.individual_task_list:
                if individual_task.task.task_id == task.task.task_id:
                    exist = True

            if not exist:
                individual1_temp.individual_task_list.append(individual_task)

        for individual_task in individual1.individual_task_list:
            exist = False
            for task in individual2_temp.individual_task_list:
                if individual_task.task.task_id == task.task.task_id:
                    exist = True

            if not exist:
                individual2_temp.individual_task_list.append(individual_task)

        index = 0
        for individual_task in individual1_temp.individual_task_list:
            individual_task.exec_sequence = index
            index += 1

        index = 0
        for individual_task in individual2_temp.individual_task_list:
            individual_task.exec_sequence = index
            index += 1

        return individual1_temp, individual2_temp

    @staticmethod
    def individual_task_pos_mutate(individual):
        mutate_pos = random.randint(0, len(individual.individual_task_list) - 1)

        pm = 0.5  # 变异系数
        p = random.random()
        new_individual = copy.deepcopy(individual)
        if p <= pm:
            new_individual.individual_task_list[mutate_pos].exec_pos = 1 - new_individual.individual_task_list[
                mutate_pos].exec_pos
        return new_individual

    @staticmethod
    def individual_task_sequence_mutate(individual):
        mutate_pos = random.randint(1, len(individual.individual_task_list) - 2)

        new_individual = copy.deepcopy(individual)
        individual_task = new_individual.individual_task_list[mutate_pos]

        pre_task_list = individual_task.task.pre_task_id_list
        last_pre_task_pos = mutate_pos - 1
        index = mutate_pos - 1
        while index >= 0:
            task_temp = new_individual.individual_task_list[index]
            if task_temp.task.task_id in pre_task_list:
                last_pre_task_pos = index
                break
            index -= 1

        suc_task_list = individual_task.task.suc_task_id_list
        first_suc_task_pos = mutate_pos + 1
        index = mutate_pos + 1
        while index < len(new_individual.individual_task_list):
            task_temp = individual.individual_task_list[index]
            if task_temp.task.task_id in suc_task_list:
                first_suc_task_pos = index
                break
            index += 1

        if first_suc_task_pos - 1 > last_pre_task_pos + 1:
            random_num = random.randint(last_pre_task_pos + 1, first_suc_task_pos - 1)

            if random_num < mutate_pos:
                individual_task_from_mutate_pos_to_random_num = copy.deepcopy(new_individual.individual_task_list[
                                                                              random_num:mutate_pos])
                new_individual.individual_task_list[
                random_num + 1: mutate_pos + 1] = individual_task_from_mutate_pos_to_random_num
                new_individual.individual_task_list[random_num] = individual_task
            else:
                individual_task_from_mutate_pos_to_random_num = copy.deepcopy(new_individual.individual_task_list[
                                                                              mutate_pos + 1: random_num + 1])
                new_individual.individual_task_list[random_num] = individual_task
                new_individual.individual_task_list[
                mutate_pos:random_num] = individual_task_from_mutate_pos_to_random_num

        index = 0
        for individual_task in new_individual.individual_task_list:
            individual_task.exec_sequence = index
            index += 1

        return new_individual

    def get_new_generation(self, individual_list):
        new_generation = list()
        for i in range(0, len(individual_list), 2):
            individual1, individual2 = self.individual_crossover(individual_list[i], individual_list[i + 1])

            individual1 = self.individual_mutate(individual1)
            individual2 = self.individual_mutate(individual2)

            self.max_id += 1
            individual1.individual_id = self.max_id
            self.max_id += 1
            individual2.individual_id = self.max_id

            individual1.schedule()
            individual2.schedule()

            new_generation.append(individual1)
            new_generation.append(individual2)
        return new_generation

    def individual_select(self, individual_list, num):
        individual_left = list()

        individual_list_temp = copy.deepcopy(individual_list)

        while len(individual_left) < num:
            pareto_list = self.paretoAlgorithm.get_pareto_result(individual_list_temp)
            if len(individual_left) + len(pareto_list) <= num:
                individual_left += pareto_list

                # 从待选列表中去除已经加入的pareto结果
                for temp in pareto_list:
                    individual = None

                    for ind in individual_list_temp:
                        if ind.individual_id == temp.individual_id:
                            individual = ind
                            break
                    if individual is not None:
                        individual_list_temp.remove(individual)
            else:
                need_num = num - len(individual_left)
                crowding_distance_algorithm = CrowdingDistanceAlgorithm()
                crowding_sort_result = crowding_distance_algorithm.individual_select_by_crowding_distance(pareto_list,
                                                                                                          need_num)
                individual_left += crowding_sort_result

        return individual_left

    def process(self):
        old_generation = list()
        new_generation = self.individual_list

        pareto_result = list()

        iteration = 0
        while iteration < constant.ITERATION:
            # 适应度值评价
            print("适应度值评价")
            pareto_list = self.paretoAlgorithm.get_pareto_result(new_generation)

            # 更新Pareto最优解
            print("更新Pareto最优解")
            new_pareto_list = pareto_result + pareto_list
            pareto_result = self.paretoAlgorithm.get_pareto_result(new_pareto_list)
            print("Pareto最优解长度 %s" % len(pareto_result))

            # 选择算子
            print("选择算子")
            mix_generation = old_generation + new_generation

            if len(mix_generation) > constant.INDIVIDUAL_NUM:
                old_generation = self.individual_select(mix_generation, constant.INDIVIDUAL_NUM)

            else:
                old_generation = mix_generation

            # 交叉算子
            # 变异算子
            # 产生新的种群
            print("产生新的种群")

            new_generation = self.get_new_generation(old_generation)
            iteration += 1

        filter_result = list()

        for individual in pareto_result:
            exist = False
            for i in filter_result:
                if individual.makespan == i.makespan and individual.energy == i.energy:
                    exist = True

            if exist is False:
                filter_result.append(individual)

        crowding_distance_algorithm = CrowdingDistanceAlgorithm()
        self.pareto_result = crowding_distance_algorithm.individual_select_by_crowding_distance(filter_result,
                                                                                                constant.INDIVIDUAL_NUM)
        # for result in pareto_result:
        #     result.print()
        #     result.print_results()
        #     print("=================")

