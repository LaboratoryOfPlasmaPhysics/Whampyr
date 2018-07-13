import numpy as np
from scipy.constants import e, proton_mass, epsilon_0, Boltzmann, c
from astropy import units as u
from .quantity import Quantity
from .distributions import distributions_dict
from copy import deepcopy
import astropy.constants as cst


def wc(charge, B , mass):
    return charge * B / mass


def wp(density, charge, mass):
    return np.sqrt(density * charge**2 / mass)


def wp_ref(density, charge, mass):
    return np.sqrt(density * charge**2 / (mass*epsilon_0))


def rho(mass, vth, charge, B):
    return mass * vth / (charge*B)


class Population:
    def __init__(self, name, charge=Quantity(1.6021766e-19, 'C'),
                 Z=1,
                 is_electrons = False,
                 me=Quantity(cst.m_e),
                 mp=Quantity(cst.m_p),
                 *args, **kwargs):
        self.name = name
        self.me = me
        self.mp = mp
        self.mass = Quantity(abs(Z)*me.value(),me.u) if is_electrons else Quantity(abs(Z)*mp.value(),mp.u)
        self.charge = charge
        self.Z = Z
        self.is_electrons = is_electrons
        self.distribution = distributions_dict["Maxwellian"]()
        self.B = None
        self.__attrs_to_norm__ = ["Z","charge","B", "mass"]

    def set_B(self, B):
        self.B = B

    @property
    def anisotropy(self):
        return self.distribution.anisotropy

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

                for attr in self.__attrs_to_norm__:
                    new_pop.__dict__[attr] = self.__dict__[attr] * other.__dict__[attr]

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

        for attr in self.__attrs_to_norm__:
            new_pop.__dict__[attr] = self.__dict__[attr] / other.__dict__[attr]

        new_pop.distribution.normalize(other.B, other.mass, other.charge, other.distribution.density)
        new_pop.__ref_pop__ = id(other)
        return new_pop

    def __repr__(self):
        return """Population: {name} 
charge : {charge}
Z : {mass}
    """.format(name=self.name, mass=self.Z, charge=self.charge)

