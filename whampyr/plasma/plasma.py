from .quantity import Quantity
from .population import Population
from copy import deepcopy
import astropy.constants as cst
import astropy.units as u


class Plasma:
    def __init__(self, name = "", B=Quantity(100., 'nT'),
                 me=Quantity(cst.m_e),
                 mp=Quantity(cst.m_p)):
        self.B = B
        self.populations = {}
        self.name = name
        self.me = me
        self.mp = mp
        self.ref_population = None

    def set_ref_population(self, ref_population):
        self.ref_population = ref_population

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
        self.set_ref_population(ref_population)
        return self

    def unnormalize(self, ref_population):
        self.B *= ref_population.B
        for pop_name in self.populations.keys():
            self.populations[pop_name] = self.populations[pop_name] * ref_population
        return self

    def electrons(self):
        c = 1.
        if self.ref_population is not None:
            c = self.ref_population.Z
        electrons = [pop for pop in self.populations.values() if pop.is_electrons]
        return electrons

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

    def __len__(self):
        return self.populations.__len__()

    def __getitem__(self, key):
        return self.populations.__getitem__(key)

    def __contains__(self, item):
        return self.populations.__contains__(item)

    def __iter__(self):
        return self.populations.values().__iter__()
