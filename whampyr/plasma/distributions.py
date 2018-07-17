from .quantity import Quantity

from astropy.constants import c
distributions_dict = {}


def registered_distribution(cls):
    name = cls.__name__
    if "Distribution" in name:
        name = name.replace("Distribution","")
    distributions_dict[name] = cls
    return cls


def f_maxwell(density, vdrift_para, vth_para, vth_perp, vpara, vperp):

    """
    value of the maxwell distribution function

    """

    return density*((2*np.pi)**(-1.5)/(vth_para*vth_perp**2)) \
                  *np.exp(-0.5*((vpara - vdrift_para)/vth_para)**2) \
                  *np.exp(-0.5*((vperp              )/vth_perp)**2)


@registered_distribution
class MaxwellianDistribution:
    def __init__(self, t_para=Quantity(1., 'eV'),
                 t_perp=Quantity(1., 'eV'), density=Quantity(1.,'cm^-3'), vdrift_para=Quantity(1.,'m/s'),
                 mass = None):

        self.Tpara = t_para
        self.Tperp = t_perp
        self.mass = mass
        self.density = density
        self.vdrift_para = vdrift_para
        self.anisotropy = t_perp / t_para
        self.vth_para = None
        self.vth_perp = None

    def set_mass(self, mass):
        self.mass = mass
        if mass is not None:
            self.vth_para = self._vth_para()
            self.vth_perp = self._vth_perp()

    def normalize(self,B, mass, charge, density):
        self.density = float(self.density / density)
        self.vdrift_para = float(self.vdrift_para / Quantity(1.*c))
        self.Tpara = float(self.Tpara / (mass * Quantity(1.*c*c)))
        self.Tperp = float(self.Tperp / (mass * Quantity(1.*c*c)))
        self.mass = float(self.mass/mass)
        self.vth_perp = self._vth_para()
        self.vth_para = self._vth_para()

    def unnormalize(self,B, mass, charge, density):
        self.density = density * self.density
        self.vdrift_para = Quantity(1.*c) * self.vdrift_para
        self.Tpara = (mass * Quantity(1.*c*c)) * self.Tpara
        self.Tperp = (mass * Quantity(1.*c*c)) * self.Tperp
        self.mass = mass *  self.mass
        self.vth_perp = self._vth_perp()
        self.vth_para = self._vth_para()

    def _vth_para(self):
        return (self.Tpara / self.mass)**0.5

    def _vth_perp(self):
        return (self.Tperp / self.mass)**0.5

