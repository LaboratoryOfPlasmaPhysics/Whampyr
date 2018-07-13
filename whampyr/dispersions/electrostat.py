
import numpy as np


from scipy.special import  iv

from plasmapy.mathematics import plasma_dispersion_func as Z
from plasmapy.mathematics import plasma_dispersion_func_deriv as Zp


def ive(x):
    iv(x) * np.exp(-x)



class electrostatic():
    """The more complex mode of equaton 10.104 s calculated"""

    def __init__(self, plasma):
        self.plasma = plasma
        self.B = plasma.B
        self.N = 10 # todo change in a smart way
        self.l_vect = np.linspace(-self.N, self.N, 1 + 2 * self.N)


    def contrib(self, population, w, **kwargs):
        """the contribution of one population"""

        kperp = kwargs['kperp']
        kpara = kwargs['kpara']

        wp = population.wp()
        wc = population.wc

        anisotropy = population.anisotropy # to add pop.anisotropy == pop.Tperp/pop.Tpara
        vth_para = population.vth_para
        vth_perp = population.vth_perp

        k2 = kperp ** 2 + kpara ** 2

        eta = kperp ** 2 * vth_perp ** 2 / (2 * wc ** 2)

        l = self.l_vect * wc
        xi = w.reshape(1, len(w)) - l.reshape(len(l), 1)
        xi = xi / (kpara * vth_para) # shape (nl, nw)

        factor = wp ** 2 * ive(self.l_vect, eta) / (k2 * vth_perp ** 2) # shape (l)
        factor = np.diag(factor)

        zz = Z(xi)
        zp = -2*(1 + xi * zz)

        return -np.sum(factor @ (anisotropy * zp) - 2 / (kpara*vth_para) * (np.diag(l) @ zz), axis=0)




    def dispersion_function(self, w, **kwargs):
        """equation 10.104 from Baumjohann et al."""

        contribs = [self.contrib(pop, w, **kwargs) for pop in self.plasma]
        return 1. + sum(contribs)




    def contrib_prim(self, population, w, **kwargs):
        """the contribution of one population"""

        kperp = kwargs['kperp']
        kpara = kwargs['kpara']

        wp = population.wp
        wc = population.wc
        anisotropy = population.anisotropy
        vth_para = population.vth_para
        vth_perp = population.vth_perp

        k2 = kperp ** 2 + kpara ** 2

        eta = kperp ** 2 * vth_perp ** 2 / (2 * wc ** 2)

        l = self.l_vect * wc
        xi = w.reshape(1, len(w)) - l.reshape(len(l), 1)
        xi = xi / (kpara * vth_para) # shape (nw,l)

        factor1 = wp ** 2 * ive(l, eta) / (k2 * vth_perp ** 2)
        factor1 = np.diag(factor1)

        zz = Z(xi)
        zp = -2*(1 + xi * zz)

        factor2 = (anisotropy * xi(l)) * zp + (np.diag(l) * wc / (kpara * vth_para)) @ zp + anisotropy * zz

        return 2 / (kpara * vth_para) * np.sum(factor1 @ factor2, axis = 0)




    def dispersion_function_prim(self, w, **kwargs):
        """equation 10.105 from Wolfram and co"""

        return sum([self.contrib_prim(pop, w, **kwargs) for pop in self.plasma])

        return value
