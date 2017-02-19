from model.Task import Task
import random
import config.constant as constant
import copy


class WorkFlow(object):
    def __init__(self):
        self.task_list = []
        self.make_span = None

    @property
    def task_list_length(self):
        return len(self.task_list)

    def get_task_by_id(self, _id):
        return self.task_list[_id]

    def print(self):
        for task in self.task_list:
            print(task.pre_task_id_list, task.task_id, task.suc_task_id_list)

    def create(self, task_number):
        entry_task = Task(0, [], [])
        exit_task = Task(task_number - 1, [], [])

        self.task_list.append(entry_task)

        surplus_task_num = task_number - 2
        last_layer = [entry_task.task_id]
        max_id = 0

        while surplus_task_num != 0:
            current_layer_task_num = random.randint(constant.MIN_TASK_NUM, constant.MAX_TASK_NUM)

            # 创建当层任务列表
            current_layer_task_id_list = []

            if current_layer_task_num > surplus_task_num:
                current_layer_task_num = surplus_task_num

            for i in range(0, current_layer_task_num):
                task = Task(max_id + 1, [], [])
                self.task_list.append(task)
                current_layer_task_id_list.append(task.task_id)
                max_id += 1

            # 给上层任务随机添加后继任务
            for task_id in last_layer:
                task = self.get_task_by_id(task_id)

                random_num = random.randint(0, current_layer_task_num - 1)
                task_id_temp = current_layer_task_id_list[random_num]
                task.suc_task_id_list.append(task_id_temp)

                task_temp = self.get_task_by_id(task_id_temp)
                task_temp.pre_task_id_list.append(task_id)

            # 判断当前层的任务是否都有前驱，如果没有，随机添加前驱任务
            for task_id in current_layer_task_id_list:
                task = self.get_task_by_id(task_id)
                if task.pre_task_id_list is None or len(task.pre_task_id_list) == 0:
                    random_num = random.randint(0, len(last_layer) - 1)
                    task_id_temp = last_layer[random_num]
                    task_temp = self.get_task_by_id(task_id_temp)
                    task_temp.suc_task_id_list.append(task.task_id)
                    task.pre_task_id_list.append(task_id_temp)

            surplus_task_num -= current_layer_task_num
            last_layer = current_layer_task_id_list

        for task_id in last_layer:
            task = self.get_task_by_id(task_id)
            task.suc_task_id_list.append(exit_task.task_id)
            exit_task.pre_task_id_list.append(task_id)

        self.task_list.append(exit_task)

    def init_task_order(self):
        # 第一个任务
        first_task = self.get_task_by_id(0)
        first_task_id = first_task.task_id

        # 已排好序的任务列表
        task_list_ordered = list()
        task_list_ordered.append(first_task_id)

        # 未排序的任务列表
        task_list = copy.deepcopy(self.task_list)
        task_list.remove(task_list[0])

        # 待排序的任务列表
        task_list_to_order = list()

        while len(self.task_list) != len(task_list_ordered):
            for task in task_list:
                if task.task_id not in task_list_ordered and task not in task_list_to_order:
                    pre_task_id_list = task.pre_task_id_list

                    available = True
                    for _id in pre_task_id_list:
                        if _id not in task_list_ordered:
                            available = False
                            break

                    if available:
                        task_list_to_order.append(task)

            i = random.randint(0, len(task_list_to_order) - 1)
            task_temp = task_list_to_order[i]
            task_list_ordered.append(task_temp.task_id)
            task_list_to_order.remove(task_temp)
        return task_list_ordered
