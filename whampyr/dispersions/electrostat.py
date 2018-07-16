import numpy as np
from ..utils import ive, Z


class electrostatic():
    """Electrostatic dispersion function"""

    def __init__(self, plasma):
        self.plasma = plasma
        self.B = plasma.B
        self.N = 0  # todo change in a smart way
        self.l_vect = np.linspace(-self.N, self.N, 1 + 2 * self.N)

    def contrib(self, population, w, **kwargs):
        """the contribution of one population"""

        kperp = kwargs['kperp']
        kpara = kwargs['kpara']

        wp = population.wp
        wc = population.wc

        anisotropy = float(population.anisotropy)  # to add pop.anisotropy == pop.Tperp/pop.Tpara
        vth_para = float(population.distribution.vth_para)
        vth_perp = float(population.distribution.vth_perp)

        if type(w) is not np.ndarray:
            ww = np.asarray(w)
            ll = self.l_vect

        else:
            ww, ll = np.meshgrid(w, self.l_vect, indexing='ij')
            w_shape = w.shape

        kparavth = kpara * vth_para
        xi = (ww - ll * wc) / kparavth
        k2 = kperp ** 2 + kpara ** 2
        eta = kperp ** 2 * vth_perp ** 2 / (2 * wc ** 2)
        Kns = wp ** 2 * ive(ll, eta) / (k2 * vth_perp ** 2)
        Ans = anisotropy
        Bns = 2 * ll * wc / (kpara * vth_para)
        zz = Z(xi)

        if type(w) is not np.ndarray:
            return np.sum(Kns * (2 * Ans * (1 + xi * zz) + Bns * zz))

        else:
            return np.sum(Kns * (2 * Ans * (1 + xi * zz) + Bns * zz), axis=1).reshape(w_shape)



    def contrib_prim(self, population, w, **kwargs):
        """the derivative of the ontribution of one population"""

        kperp = kwargs['kperp']
        kpara = kwargs['kpara']

        wp =  population.wp
        wc =  population.wc

        anisotropy = float(population.anisotropy)  # to add pop.anisotropy == pop.Tperp/pop.Tpara
        vth_para = float(population.distribution.vth_para)
        vth_perp = float(population.distribution.vth_perp)

        if type(w) is not np.ndarray:
            ww = np.asarray(w)
            ll = self.l_vect

        else:
            ww, ll = np.meshgrid(w, self.l_vect, indexing='ij')
            w_shape = w.shape

        kparavth = kpara * vth_para
        xi = (ww - ll * wc) / (kparavth)
        k2 = kperp ** 2 + kpara ** 2
        eta = kperp ** 2 * vth_perp ** 2 / (2 * wc ** 2)
        Kns = wp ** 2 * ive(ll, eta) / (k2 * vth_perp ** 2)
        Ans = anisotropy
        Bns = 2 * ll * wc / (kpara * vth_para)

        zz = Z(xi)

        if type(w) is not np.ndarray:
            return - 1. / kparavth * np.sum(Kns * (Ans * (4 * xi + zz * (4 * xi ** 2 - 2)) + 2 * Bns * (1 + xi * zz)))

        else:
            return - 1. / kparavth * np.sum(Kns * (Ans * (4 * xi + zz * (4 * xi ** 2 - 2)) + 2 * Bns * (1 + xi * zz)),
                                            axis=1).reshape(w_shape)

    def dispersion_function(self, w, **kwargs):
        """equation 10.104 from Baumjohann et al."""

        contribs = [self.contrib(pop, w, **kwargs) for pop in self.plasma]
        return 1. + sum(contribs)

    def dispersion_function_prime(self, w, **kwargs):
        """equation 10.105 from Wolfram and co"""
        return sum([self.contrib_prim(pop, w, **kwargs) for pop in self.plasma if pop.is_electrons])


