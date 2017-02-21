from util.ParetoAlgorithm import ParetoAlgorithm
from util.CrowdingDistanceAlgorithm import CrowdingDistanceAlgorithm
import math


class EvaluationMetric(object):
    @staticmethod
    def q_metric(pareto_1, pareto_2):
        print((len(pareto_1), len(pareto_2)))
        mix_pareto_list = ParetoAlgorithm.get_pareto_result(pareto_1 + pareto_2)
        mix_pareto_list_length = len(mix_pareto_list)
        print("pareto 1")
        for individual in pareto_1:
            individual.print_results()

        print("pareto 2")
        for individual in pareto_2:
            individual.print_results()

        if mix_pareto_list_length > 0:
            print("pareto mix")
            pareto_1_left_num = 0
            pareto_2_left_num = 0
            for individual in mix_pareto_list:
                individual.print()
                print("===========")
                for i in pareto_1:
                    if individual.makespan == i.makespan and individual.energy == i.energy:
                        pareto_1_left_num += 1

                for i in pareto_2:
                    if individual.makespan == i.makespan and individual.energy == i.energy:
                        pareto_2_left_num += 1

            q_ref1_ref2 = pareto_1_left_num / mix_pareto_list_length
            q_ref2_ref1 = pareto_2_left_num / mix_pareto_list_length

            if q_ref1_ref2 > q_ref2_ref1 or q_ref1_ref2 > 0.5:
                return True

        return False

    @staticmethod
    def fs_metric(pareto):
        if len(pareto) < 2:
            return 0

        pareto_sorted_by_makespan = sorted(pareto, key=lambda individual: individual.makespan)
        min_makespan_dif = pareto_sorted_by_makespan[1].makespan - pareto_sorted_by_makespan[0].makespan

        index = 0
        while index < len(pareto_sorted_by_makespan) - 1:
            dif = pareto_sorted_by_makespan[index + 1].makespan - pareto_sorted_by_makespan[index].makespan
            if dif < min_makespan_dif:
                min_makespan_dif = dif
            index += 1

        pareto_sorted_by_energy = sorted(pareto, key=lambda individual: individual.energy)
        min_energy_dif = pareto_sorted_by_energy[1].energy - pareto_sorted_by_energy[0].energy

        index = 0
        while index < len(pareto_sorted_by_energy) - 1:
            dif = pareto_sorted_by_energy[index + 1].energy - pareto_sorted_by_energy[index].energy
            if dif < min_energy_dif:
                min_energy_dif = dif
            index += 1

        return math.sqrt(math.pow(min_makespan_dif, 2) + math.pow(min_energy_dif, 2))

    @staticmethod
    def s_metric(pareto):
        length = len(pareto)
        if length == 0:
            return

        distance_sum = 0

        min_distance = list()
        for individual in pareto:
            d = CrowdingDistanceAlgorithm.get_min_distance(pareto, individual)
            min_distance.append(d)
            distance_sum += d

        distance_average = distance_sum / length

        s = 0
        for distance in min_distance:
            s += math.pow((distance - distance_average), 2)

        return math.sqrt(s / length)
