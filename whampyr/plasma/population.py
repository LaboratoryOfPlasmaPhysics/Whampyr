import numpy as np
from scipy.constants import e, proton_mass, epsilon_0, Boltzmann, c
from astropy import units as u
from .quantity import Quantity
from .distributions import distributions_dict
from copy import deepcopy


def wc(charge, B , mass):
    return charge * B / mass


def wp(density, charge, mass):
    return np.sqrt(density * charge**2 / (mass*epsilon_0))


def rho(mass, vth, charge, B):
    return mass * vth / (charge*B)


class Population:
    def __init__(self, name, charge=Quantity(1.,'e'), mass=Quantity(1.,'u'), *args, **kwargs):
        self.name = name
        self.charge = charge
        self.mass = mass
        self.distribution = distributions_dict["Maxwellian"]()
        self.B = None

    def set_B(self, B):
        self.B = B

    @property
    def wp(self):
        return wp(self.distribution.density.value(), self.charge.value(), self.mass.value())

    @property
    def wc(self):
        return wc(self.charge.value(), self.B.value() , self.mass.value())

    def change(self, source_reference, destination_reference):
        if self.__dict__.get('__ref_pop__', id(1)) == id(source_reference):
            self = (self * source_reference) / destination_reference
        else:
            raise ValueError("Current population must have source_reference as population reference")

    def __mul__(self, other):
        if hasattr(self, '__ref_pop__') ^ hasattr(other, '__ref_pop__'):
            if (self.__dict__.get('__ref_pop__',id(1)) == id(other)) ^ (other.__dict__.get('__ref_pop__',id(1)) == id(self)):
                new_pop =  Population("{}*{}".format(self.name,other.name))
                new_pop.distribution = deepcopy(self.distribution)

                new_pop.mass = self.mass * other.mass
                new_pop.charge = self.charge * other.charge
                new_pop.B = self.B * other.B

                new_pop.distribution.unnormalize(other.B, other.mass, other.charge, other.distribution.density)
                if hasattr(new_pop,'__ref_pop__'):
                    new_pop.__dict__.pop('__ref_pop__')
                return new_pop
            else:
                raise ValueError("Wrong reference population")
        raise ValueError("Can't multiply two normalized or un-normalized population")

    def __truediv__(self, other):
        if hasattr(self, '__ref_pop__') or hasattr(other, '__ref_pop__'):
            raise ValueError("Both populations must un-normalized")
        new_pop = Population("{}/{}".format(self.name,other.name))
        new_pop.distribution = deepcopy(self.distribution)

        new_pop.mass = self.mass / other.mass
        new_pop.charge = self.charge / other.charge
        new_pop.B = self.B  / other.B

        new_pop.distribution.normalize(other.B, other.mass, other.charge, other.distribution.density)
        new_pop.__ref_pop__ = id(other)
        return new_pop

    def __repr__(self):
        return """Population: {name} 
charge : {charge}
mass : {mass}
    """.format(name=self.name, mass=self.mass, charge=self.charge)

