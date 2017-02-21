from config import constant
import math


class IndividualTask(object):
    task = None
    exec_pos = None
    exec_sequence = None


class Individual(object):
    makespan = 0
    energy = 0
    individual_id = 0

    def __init__(self, algorithm, individual_id, workflow, bandwidth_value, delta=constant.USR_MAX_DELAY_TOLERANCE):
        self.individual_id = individual_id
        self.workflow = workflow
        self.bandwidth_value = bandwidth_value
        self.delta = delta
        self.individual_task_list = algorithm.init_task_list_order_pos()

    def print(self):
        for individual_task in self.individual_task_list:
            print(individual_task.task.task_id, individual_task.exec_pos, individual_task.exec_sequence)

    def print_results(self):
        print(self.individual_id, self.makespan, self.energy)

    def get_individual_task_by_id(self, _id):
        for individual_task in self.individual_task_list:
            if individual_task.task.task_id == _id:
                return individual_task

    # 整个工作流完工时间
    def calc_makespan(self, bandwidth_value):
        last_task = self.individual_task_list[len(self.individual_task_list) - 1]
        if last_task.exec_pos == 0:
            return last_task.task.end_time
        else:
            optimal_v, optimal_k = self.delay_transmission(bandwidth_value, last_task.task.end_time,
                                                           last_task.task.output)
            return optimal_k

    # 整个工作流完工的能耗
    def calc_energy(self):
        energy = 0
        for individual_task in self.individual_task_list:
            energy += individual_task.task.energy

        last_individual_task = self.individual_task_list[len(self.individual_task_list) - 1]

        if last_individual_task.exec_pos == 1:
            optimal_v, optimal_k = self.delay_transmission(
                self.bandwidth_value, last_individual_task.task.end_time, last_individual_task.task.output)

            time_span = optimal_k - optimal_v
            energy += constant.MOBILE_RECEIVE_POWER * time_span

        return math.ceil(energy)

    @staticmethod
    def is_task_ready_to_exec(individual_task, finish_task_id_list):
        if len(individual_task.task.pre_task_id_list) == 0:
            return True

        for task_id in individual_task.task.pre_task_id_list:
            if task_id not in finish_task_id_list:
                return False

        return True

    def get_task_input_value(self, individual_task):
        task_input = 0

        pre_task_id_list = individual_task.task.pre_task_id_list
        for pre_task_id in pre_task_id_list:
            pre_task = self.get_individual_task_by_id(pre_task_id)

            if pre_task.exec_pos != individual_task.exec_pos:
                task_input += pre_task.task.output

        return task_input

    def delay_transmission(self, bandwidth_value, cur_time, task_input):
        cur_bw_value = bandwidth_value[cur_time]
        span = 1
        value = cur_bw_value
        while value < task_input:
            span += 1
            value += bandwidth_value[cur_time + span]

        # 无延时传输机制时的结束时间点
        k1 = cur_time + span

        # 加入延时传输机制

        min_span = span
        optimal_v = cur_time
        optimal_k = k1

        i = 1
        while i <= self.delta:
            # 新的传输结束时间点
            k2 = k1 + i
            value = bandwidth_value[k2 - 1]
            # 新的传输开始时间点
            v = k2 - 1
            while value < task_input:
                v -= 1
                value += bandwidth_value[v]
            span_dt = k2 - v
            if span_dt < min_span:
                min_span = span_dt
                optimal_v = v
                optimal_k = k2

            i += 1

        return optimal_v, optimal_k

    def update(self, individual_task, cur_time, optimal_v, optimal_k):
        individual_task.task.start_time = cur_time
        individual_task.task.transmission_time = optimal_k - optimal_v
        individual_task.task.span_time = optimal_k - cur_time

        if individual_task.exec_pos == 0:
            capacity = constant.MOBILE_CAPACITY
            power = constant.MOBILE_RECEIVE_POWER
            process_power = constant.MOBILE_PROCESS_POWER
        else:
            capacity = constant.CLOUD_CAPACITY
            power = constant.MOBILE_SEND_POWER
            process_power = 0

        individual_task.task.excu_time = math.ceil(individual_task.task.work_load / capacity)
        individual_task.task.end_time = \
            individual_task.task.start_time + individual_task.task.span_time + individual_task.task.excu_time

        transmission_energy = power * individual_task.task.transmission_time
        process_energy = individual_task.task.excu_time * process_power
        individual_task.task.energy = transmission_energy + process_energy

    def get_pre_task_all_finish_time(self, individual_task):
        time = 0

        for task_id in individual_task.task.pre_task_id_list:
            task_temp = self.get_individual_task_by_id(task_id).task
            if task_temp.end_time > time:
                time = task_temp.end_time

        return time

    def schedule(self):
        # 初始化移动设备和云端待执行的任务列表
        mobile_task_list = list()
        cloud_task_list = list()

        for individual_task in self.individual_task_list:
            if individual_task.exec_pos == 0:
                mobile_task_list.append(individual_task)
            else:
                cloud_task_list.append(individual_task)

        # 已完成任务列表
        finish_task_id_list = list()

        mobile_task = None
        cloud_task = None
        if len(mobile_task_list) > 0:
            mobile_task = mobile_task_list[0]
        if len(cloud_task_list) > 0:
            cloud_task = cloud_task_list[0]

        mobile_task_index = 0
        cloud_task_index = 0

        # 任务调度，移动设备和云端同时进行
        while mobile_task_index < len(mobile_task_list) or cloud_task_index < len(cloud_task_list):
            # print(mobile_task_index,cloud_task_index)
            if mobile_task is not None and self.is_task_ready_to_exec(mobile_task, finish_task_id_list):
                mobile_cur_time = self.get_pre_task_all_finish_time(mobile_task)

                task_input = self.get_task_input_value(mobile_task)

                optimal_v, optimal_k = self.delay_transmission(self.bandwidth_value, mobile_cur_time, task_input)

                self.update(mobile_task, mobile_cur_time, optimal_v, optimal_k)
                finish_task_id_list.append(mobile_task.task.task_id)

                mobile_task_index += 1
                if mobile_task_index < len(mobile_task_list):
                    mobile_task = mobile_task_list[mobile_task_index]

            if cloud_task is not None and self.is_task_ready_to_exec(cloud_task, finish_task_id_list):
                cloud_cur_time = self.get_pre_task_all_finish_time(cloud_task)
                task_input = self.get_task_input_value(cloud_task)

                optimal_v, optimal_k = self.delay_transmission(self.bandwidth_value, cloud_cur_time, task_input)

                self.update(cloud_task, cloud_cur_time, optimal_v, optimal_k)
                finish_task_id_list.append(cloud_task.task.task_id)

                cloud_task_index += 1
                if cloud_task_index < len(cloud_task_list):
                    cloud_task = cloud_task_list[cloud_task_index]

        self.makespan = self.calc_makespan(self.bandwidth_value)
        self.energy = self.calc_energy()
