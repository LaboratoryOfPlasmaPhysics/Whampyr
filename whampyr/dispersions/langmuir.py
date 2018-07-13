


from scipy.special import  ive

from plasmapy.mathematics import plasma_dispersion_func as Z
from plasmapy.mathematics import plasma_dispersion_func_deriv as Zp



class Lamguir_Mode():
    """The anisotric lamgmuir mode"""

    def __init__(self, plasma):
        self.plasma = plasma
        self.B = plasma.B


    def dispersion_function(self, w, **kwargs):
        """equation 10.105 from Wolfram and co"""

        kperp = kwargs['kperp']
        kpara = kwargs['kpara']

        value = 0
        for elec in self.plasma.electrons():
            eta = kperp ** 2 * elec.wp() ** 2 / (2 * elec.wc() ** 2)
            xi = w / kpara
            k2 = kperp ** 2 + kpara ** 2
            value = value + 1 - 1 / k2 * ive(0, eta) * Zp(xi)

        return value


    def dispersion_function_prime(self, w, **kwargs):
        """equation 10.105 from Wolfram and co"""

        kperp = kwargs['kperp']
        kpara = kwargs['kpara']


        value = 0
        for elec in self.plasma.electrons():
            eta = kperp ** 2. * elec.pulsation ** 2 / (2. * elec.w_c ** 2)

            xi = w / kpara
            k2 = kperp ** 2 + kpara ** 2

            value = value + 2. / k2 * ive(0, eta) * (Z(xi) + xi * Zp(xi))

        return value / kpara
