from util.GeneticAlgorithm import GeneticAlgorithm
from util.MOHEFTAlgorithm import MOHEFTAlgorithm
from model.Bandwidth import Bandwidth
from model.WorkFlow import WorkFlow
from config import constant


if __name__ == "__main__":
    # 初始化一个工作流
    workflow = WorkFlow()
    workflow.create(constant.TASK_NUM)
    workflow.print()

    # 随机初始化带宽环境
    bandwidth = Bandwidth(time_slots=constant.TOTAL_TIME_SLOT)
    bw_value = bandwidth.value

    geneticAlgorithm = GeneticAlgorithm(workflow, bw_value)
    geneticAlgorithm.process()

    moheftAlgorithm = MOHEFTAlgorithm(workflow, bw_value)
    moheftAlgorithm.process()
