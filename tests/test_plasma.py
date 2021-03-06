import pytest
from whampyr.plasma.quantity import Quantity
from whampyr.plasma.population import Population
from whampyr.plasma.plasma import Plasma
from whampyr.plasma.distributions import MaxwellianDistribution
from copy import deepcopy
import astropy.constants as cst
import jsonpickle

@pytest.fixture
def simple_ion():
    maxwellian = MaxwellianDistribution(density=Quantity(2, "cm^-3"))
    p = Population("IONS", Z=10.,
                   is_electrons=False,
                   me=Quantity(cst.m_e),
                   mp=Quantity(cst.m_p),
                   distribution=maxwellian)
    return p

@pytest.fixture
def simple_electron():
    maxwellian = MaxwellianDistribution(density=Quantity(2, "cm^-3"))
    p = Population("Electrons",
                   Z=-1.,
                   is_electrons=True,
                   me=Quantity(cst.m_e),
                   mp=Quantity(cst.m_p),
                   distribution=maxwellian)
    return p

@pytest.fixture
def simple_plasma():
    ions = simple_ion()
    electrons = simple_electron()
    plasma = Plasma(Quantity(100.,'nT'))
    plasma.add_population(ions)
    plasma.add_population(electrons)
    return plasma


def test_can_normalize_and_unnormalize_a_plasma(simple_plasma):
    electrons = simple_plasma.populations['Electrons']
    ions = simple_plasma.populations['IONS']

    normalized_plasma = deepcopy(simple_plasma).normalize(electrons)
    assert normalized_plasma.populations['Electrons'].B.value() == 1.
    assert normalized_plasma.populations['Electrons'].charge.value() == 1.
    assert normalized_plasma.populations['Electrons'].mass.value() == 1.

    assert normalized_plasma.populations['IONS'].B.u == ''
    assert normalized_plasma.populations['IONS'].charge.u == ''
    assert normalized_plasma.populations['IONS'].mass.u == ''

    normalized_plasma.change(ions)

    assert normalized_plasma.populations['IONS'].B.value() == 1.
    assert normalized_plasma.populations['IONS'].charge.value() == 1.
    assert normalized_plasma.populations['IONS'].mass.value() == 1.

    assert normalized_plasma.populations['Electrons'].B.u == ''
    assert normalized_plasma.populations['Electrons'].charge.u == ''
    assert normalized_plasma.populations['Electrons'].mass.u == ''

    assert normalized_plasma.populations['IONS'].B.u == ''
    assert normalized_plasma.populations['IONS'].charge.u == ''
    assert normalized_plasma.populations['IONS'].mass.u == ''

    normalized_plasma.unnormalize()

    assert normalized_plasma.populations['IONS'].B.value() == ions.B.value()
    assert normalized_plasma.populations['IONS'].charge.value() == ions.charge.value()
    assert normalized_plasma.populations['IONS'].mass.value() == ions.mass.value()

    assert normalized_plasma.populations['Electrons'].B.value() == electrons.B.value()
    assert normalized_plasma.populations['Electrons'].charge.value() == electrons.charge.value()
    assert normalized_plasma.populations['Electrons'].mass.value() == electrons.mass.value()


def test_can_iterate_populations_in_a_plasma(simple_plasma):
    pops = [p for p in simple_plasma]
    assert len(pops) == len(simple_plasma)
    assert pops[0].name != pops[1].name


def test_can_get_electrons(simple_plasma):
    assert len(simple_plasma.electrons()) == 1
