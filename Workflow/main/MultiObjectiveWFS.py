from util.GeneticAlgorithm import GeneticAlgorithm
from util.MOHEFTAlgorithm import MOHEFTAlgorithm
from util.EvaluationMetric import EvaluationMetric
from util.RandomAlgorithm import RandomAlgorithm
from util.FileUtil import FileUtil
from model.Bandwidth import Bandwidth
from model.WorkFlow import WorkFlow
from config import constant


def sort_result_by_makespan(result):
    return sorted(result, key=lambda individual: individual.makespan)


if __name__ == "__main__":
    # 初始化一个工作流
    workflow = WorkFlow()
    workflow.create(constant.TASK_NUM)
    workflow.print()

    # 随机初始化带宽环境
    bandwidth = Bandwidth(time_slots=constant.TOTAL_TIME_SLOT)
    bw_value = bandwidth.value

    # RANDOM算法
    randomAlgorithm = RandomAlgorithm(workflow, bw_value)
    random_result_sort_by_makespan = sort_result_by_makespan(randomAlgorithm.pareto_result)
    FileUtil.dump_result_to_file(random_result_sort_by_makespan, randomAlgorithm.name)

    # MOWS-DTM算法
    mowsDtmAlgorithm = GeneticAlgorithm(workflow, bw_value)
    mowsDtmAlgorithm.process()
    mows_dtm_result_sort_by_makespan = sort_result_by_makespan(mowsDtmAlgorithm.pareto_result)
    FileUtil.dump_result_to_file(mows_dtm_result_sort_by_makespan, mowsDtmAlgorithm.name)

    # MOHEFT算法
    moheftAlgorithm = MOHEFTAlgorithm(workflow, bw_value)
    moheftAlgorithm.process()
    moheft_result_sort_by_makespan = sort_result_by_makespan(moheftAlgorithm.pareto_result)
    FileUtil.dump_result_to_file(moheft_result_sort_by_makespan, moheftAlgorithm.name)

    metric_result = list()

    # Q-metric
    evaluation = EvaluationMetric()
    metric_result.append(evaluation.q_metric(randomAlgorithm.pareto_result, moheftAlgorithm.pareto_result))
    metric_result.append(evaluation.q_metric(randomAlgorithm.pareto_result, mowsDtmAlgorithm.pareto_result))
    metric_result.append(evaluation.q_metric(moheftAlgorithm.pareto_result, mowsDtmAlgorithm.pareto_result))

    # FS-metric
    metric_result.append(evaluation.fs_metric(randomAlgorithm.pareto_result))
    metric_result.append(evaluation.fs_metric(mowsDtmAlgorithm.pareto_result))
    metric_result.append(evaluation.fs_metric(moheftAlgorithm.pareto_result))

    # S-metric
    metric_result.append(evaluation.s_metric(randomAlgorithm.pareto_result))
    metric_result.append(evaluation.s_metric(mowsDtmAlgorithm.pareto_result))
    metric_result.append(evaluation.s_metric(moheftAlgorithm.pareto_result))

    FileUtil.dump_metric_result_to_file(
        metric_result,
        "%s_%s_%s" % (randomAlgorithm.name, mowsDtmAlgorithm.name, moheftAlgorithm.name)
    )

    # for delta in [0, 1, 3, 5, 7]:
    #     mowsDtmAlgorithm = GeneticAlgorithm(workflow, bw_value, delta=delta)
    #     mowsDtmAlgorithm.process()
    #     mows_dtm_result_sort_by_makespan = sort_result_by_makespan(mowsDtmAlgorithm.pareto_result)
    #     FileUtil.dump_result_to_file(mows_dtm_result_sort_by_makespan, mowsDtmAlgorithm.name)
