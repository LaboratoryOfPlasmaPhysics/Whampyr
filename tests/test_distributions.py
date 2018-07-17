import pytest
from whampyr.plasma.quantity import Quantity
from whampyr.plasma.population import Population
from whampyr.plasma.distributions import distributions_dict, MaxwellianDistribution


def test_check_that_distributions_autoregisters():
    assert "Maxwellian" in distributions_dict
    assert distributions_dict[ "Maxwellian"] is MaxwellianDistribution
