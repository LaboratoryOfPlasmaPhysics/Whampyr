from .quantity import Quantity


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
    def __init__(self, t_para=Quantity(1., 'eV'), t_perp=Quantity(1., 'eV'), density=Quantity(1.,'cm^-3'), vdrift_para=Quantity(1.,'m/s')):
        self.Tpara = t_para
        self.Tperp = t_perp
        self.density = density
        self.vdrift_para = vdrift_para

    def anisotropy(self):
        Tperp = self.Tperp.converted('eV').value
        Tpara = self.Tpara.converted('eV').value
        return Tperp/Tpara

    def normalize(self,B, mass, charge, density):
        pass

    def unnormalize(self,B, mass, charge, density):
        pass

    @property
    def vth_para(self):
        mass = self.mass_si
        Tpara = self.distribution.Tpara.converted('eV').value
        return (Tpara / mass)**0.5

    @property
    def vth_perp(self):
        mass = self.mass_si
        Tperp = self.distribution.Tperp.converted('eV').value
        return (Tperp / mass)**0.5

