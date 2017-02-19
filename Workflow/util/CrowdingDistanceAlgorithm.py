import math


class CrowdingDistanceAlgorithm(object):
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

        first_4 = [first_individual_makespan, last_individual_makespan, first_individual_energy, last_individual_energy]

        if num >= 4:
            result.extend(
                [first_individual_makespan, last_individual_makespan, first_individual_energy, last_individual_energy])

            left_num = num - 4

            j = 0
            while j < left_num and j < len(sorted_crowding_distance):
                individual_id = sorted_crowding_distance[j][0]

                for individual in individual_list:
                    if individual.individual_id == individual_id:
                        result.append(individual)
                        break
                j += 1
        else:
            result = first_4[:num]

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
