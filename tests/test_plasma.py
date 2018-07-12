import pytest
from whampyr.plasma.quantity import Quantity
from whampyr.plasma.population import Population
from whampyr.plasma.plasma import Plasma
from copy import deepcopy
import jsonpickle

@pytest.fixture
def simple_ion():
    p = Population("IONS")
    p.charge = Quantity(1.6021766e-19, 'C')
    p.mass = Quantity(1., 'u')
    return p

@pytest.fixture
def simple_electron():
    p = Population("Electrons")
    p.charge = Quantity(-1.6021766e-19, 'C')
    p.mass = Quantity(.0005, 'u')
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

    normalized_plasma.change(electrons,ions)

    assert normalized_plasma.populations['IONS'].B.value() == 1.
    assert normalized_plasma.populations['IONS'].charge.value() == 1.
    assert normalized_plasma.populations['IONS'].mass.value() == 1.

    assert normalized_plasma.populations['Electrons'].B.u == ''
    assert normalized_plasma.populations['Electrons'].charge.u == ''
    assert normalized_plasma.populations['Electrons'].mass.u == ''

    assert normalized_plasma.populations['IONS'].B.u == ''
    assert normalized_plasma.populations['IONS'].charge.u == ''
    assert normalized_plasma.populations['IONS'].mass.u == ''

    with pytest.raises(ValueError):
        normalized_plasma.unnormalize(electrons)

    normalized_plasma.unnormalize(ions)

    assert normalized_plasma.populations['IONS'].B.value() == ions.B.value()
    assert normalized_plasma.populations['IONS'].charge.value() == ions.charge.value()
    assert normalized_plasma.populations['IONS'].mass.value() == ions.mass.value()

    assert normalized_plasma.populations['Electrons'].B.value() == electrons.B.value()
    assert normalized_plasma.populations['Electrons'].charge.value() == electrons.charge.value()
    assert normalized_plasma.populations['Electrons'].mass.value() == electrons.mass.value()
