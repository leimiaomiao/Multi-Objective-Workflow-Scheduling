from config import constant
import os


class FileUtil(object):
    @staticmethod
    def dump_result_to_file(result, algorithm_name):
        dir_path = "../experiment_data/"

        file_name = "%s_%s_%s_%s_%s_%s" % \
                    (algorithm_name,
                     constant.TASK_NUM,
                     constant.MIN_OUTPUT_NUM,
                     constant.MAX_OUTPUT_NUM,
                     constant.MIN_WORKLOAD_NUM,
                     constant.MAX_WORKLOAD_NUM
                     )

        file_path = "%s%s.csv" % (dir_path, file_name)

        file = open(file_path, "w", encoding="utf-8")
        for individual in result:
            string = "%s,%s\n" % (individual.makespan, individual.energy)
            file.write(string)
        file.close()

    @staticmethod
    def dump_metric_result_to_file(result_list, name):
        dir_path = "../experiment_data/"
        file_name = "metric_%s_%s_%s_%s_%s_%s" % \
                    (name,
                     constant.TASK_NUM,
                     constant.MIN_OUTPUT_NUM,
                     constant.MAX_OUTPUT_NUM,
                     constant.MIN_WORKLOAD_NUM,
                     constant.MAX_WORKLOAD_NUM)

        file_path = "%s%s.txt" % (dir_path, file_name)

        file = open(file_path, "w", encoding="utf-8")
        for result in result_list:
            file.write("%s\n" % result)
        file.close()

