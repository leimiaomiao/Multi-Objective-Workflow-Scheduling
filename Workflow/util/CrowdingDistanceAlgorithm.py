import math


class CrowdingDistanceAlgorithm(object):
    @staticmethod
    def get_min_distance(individual_list, individual):
        if len(individual_list) < 2:
            return 0

        distance_list = list()
        for ind in individual_list:
            if ind.individual_id != individual.individual_id:
                distance = math.sqrt(
                    math.pow((ind.energy - individual.energy), 2) + math.pow((ind.makespan - individual.makespan), 2))
                distance_list.append(distance)

        return min(distance_list)

    def individual_select_by_crowding_distance(self, individual_list, num):
        result = list()

        makespan_distance_dict, first_individual_makespan, last_individual_makespan = \
            self.individual_sort_by_attr(individual_list, "makespan")

        energy_distance_dict, first_individual_energy, last_individual_energy = \
            self.individual_sort_by_attr(individual_list, "energy")

        crowding_distance = list()

        makespan_dis_id_list = makespan_distance_dict.keys()
        energy_dis_id_list = energy_distance_dict.keys()

        for indi_id in makespan_dis_id_list:
            if indi_id in energy_dis_id_list:
                distance = makespan_distance_dict[indi_id] + energy_distance_dict[indi_id]
                crowding_distance.append((indi_id, distance))

        sorted_crowding_distance = sorted(crowding_distance, key=lambda d: d[1])

        prior_list = []

        for individual in [first_individual_makespan, last_individual_makespan, first_individual_energy,
                           last_individual_energy]:
            exist = False
            for i in prior_list:
                if individual.individual_id == i.individual_id:
                    exist = True
                    break
            if exist is False:
                prior_list.append(individual)

        if num >= len(prior_list):
            result.extend(prior_list)

            left_num = num - len(prior_list)

            j = 0
            while j < left_num and j < len(sorted_crowding_distance):
                individual_id = sorted_crowding_distance[j][0]

                for individual in individual_list:
                    if individual.individual_id == individual_id:
                        result.append(individual)
                        break
                j += 1
        else:
            result = prior_list[:num]

        return result

    @staticmethod
    def individual_sort_by_attr(individual_list, attr):
        individual_list_sorted = sorted(individual_list, key=lambda ind: getattr(ind, attr))
        first_individual = individual_list_sorted[0]
        last_individual = individual_list_sorted[len(individual_list_sorted) - 1]

        first_value = getattr(first_individual, attr)
        last_value = getattr(last_individual, attr)
        distance_dict = dict()

        i = 1
        while i < len(individual_list_sorted) - 1:
            individual_left = individual_list_sorted[i - 1]
            individual_right = individual_list_sorted[i + 1]

            right_value = getattr(individual_right, attr)
            left_value = getattr(individual_left, attr)

            if (last_value - first_value) != 0:
                distance = math.fabs(right_value - left_value) / (last_value - first_value)
            else:
                distance = 0

            distance_dict[individual_list_sorted[i].individual_id] = distance
            i += 1

        return distance_dict, first_individual, last_individual
