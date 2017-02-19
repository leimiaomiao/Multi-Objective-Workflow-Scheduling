import random


class Bandwidth(object):
    @staticmethod
    def generate_random_bw():
        return random.randint(1, 10)

    def __init__(self, time_slots=100):
        self.value = []
        for i in range(time_slots):
            self.value.append(self.generate_random_bw())
