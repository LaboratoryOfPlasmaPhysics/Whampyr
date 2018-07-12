from .quantity import Quantity
from .population import Population
from copy import deepcopy


class Plasma:
    def __init__(self, B=Quantity(100,'nT')):
        self.B = B
        self.populations = {}

    def add_population(self, pop, copy=False):
        if type(pop) is not Population:
            raise TypeError("Expecting a population object!")
        if copy:
            pop = deepcopy(pop)
        self.populations[pop.name] = pop
        pop.set_B(self.B)

    def normalize(self, ref_population):
        self.B /= ref_population.B
        for pop_name in self.populations.keys():
            self.populations[pop_name] = self.populations[pop_name] / ref_population
        return self

    def unnormalize(self, ref_population):
        self.B *= ref_population.B
        for pop_name in self.populations.keys():
            self.populations[pop_name] = self.populations[pop_name] * ref_population
        return self

    def change(self, source_reference, destination_reference):
        self.B = (self.B * source_reference.B) / destination_reference.B
        for pop_name in self.populations.keys():
            self.populations[pop_name] = (self.populations[pop_name] * source_reference) / destination_reference
        return self

    def __repr__(self):
        return """Plasma: 
    B : {B}
    Populations : {pops}
        """.format(B=self.B, pops=self.populations)
