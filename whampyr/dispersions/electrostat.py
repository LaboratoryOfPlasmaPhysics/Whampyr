
import numpy as np


from scipy.special import  ive

from plasmapy.mathematics import plasma_dispersion_func as Z
from plasmapy.mathematics import plasma_dispersion_func_deriv as Zp




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

        def xi(l = 0):
            return (w - l * wc) / (kpara * vth_para)

        def factor(l):
            return wp ** 2 * ive(l, eta) / (k2 * vth_perp ** 2)

        return -sum([factor(l) * (anisotropy * Zp(xi(l)) -
                             2 * l * wc / (kpara * vth_para) * Z(xi(l))) for l in self.l_vect])



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

        def xi(l=0):
            return (w - l * wc) / (kpara * vth_para)

        def factor1(l):
            return wp ** 2 * ive(l, eta) / (k2 * vth_perp ** 2)

        def factor2(l):
            return Zp(xi(l)) * (anisotropy * xi(l) + l * wc / (kpara * vth_para)) + anisotropy * Z(xi(l))

        return 2 / (kpara * vth_para) * sum([factor1(l) * factor2(l) for l in self.l_vect])




    def dispersion_function_prim(self, w, **kwargs):
        """equation 10.105 from Wolfram and co"""

        return sum([self.contrib_prim(pop, w, **kwargs) for pop in self.plasma])

        return value
