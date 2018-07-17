#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `Quantity` class."""

"""
{"Bfield":[100.0,"nT"], "refpop": "electron",
"populations":{
"electron":{"mass":[0.0005, "u"], "charge":[-1.0, "e"], "distribution": "Maxwellian"},
"ion1":{"mass":[1.0, "u"], "charge":[1.0, "e"], "distribution":"Maxwellian"}
},
"maxwell_params":{
"electron":{"density":[1.0,"cm^-3"], "Tpara":[1.0, "eV"], "Tperp":[1.0, "eV"], 
"vdrift_para":[5.0e5,"m/s"]},
"ion1":{"density":[1.0,"cm^-3"], "Tpara":[0.1, "eV"], "Tperp":[0.1, "eV"], "vdrift_para":[0.0,"m/s"]}
}
}
"""

import pytest
from whampyr.plasma.quantity import Quantity
from whampyr.plasma.population import Population
from whampyr.plasma.distributions import MaxwellianDistribution
from copy import deepcopy
import jsonpickle
import astropy.constants as cst

@pytest.fixture
def simple_ions():
    maxwellian = MaxwellianDistribution(density=Quantity(2,"cm^-3"))
    p = Population("IONS", Z=10.,
                   is_electrons=False,
                   me=Quantity(cst.m_e),
                   mp=Quantity(cst.m_p),
                   distribution=maxwellian
                   )
    p.set_B(Quantity(100., 'nT'))
    return p



def test_divide_two_compatible_populations(simple_ions):
    normalized_pop = simple_ions / simple_ions


def test_cant_divide_two_incompatible_populations(simple_ions):
    normalized_pop = simple_ions / simple_ions
    with pytest.raises(ValueError):
        fail = simple_ions / normalized_pop
    with pytest.raises(ValueError):
        fail =  normalized_pop / simple_ions


def test_can_un_normalize_population(simple_ions):
    normalized_pop = simple_ions / simple_ions
    origin = normalized_pop * simple_ions
    with pytest.raises(TypeError):
        origin = simple_ions * normalized_pop


def test_cant_un_normalize_population_with_wrong_ref_population(simple_ions):
    normalized_pop = simple_ions / simple_ions
    simple_ions2 = deepcopy(simple_ions)

    with pytest.raises(ValueError):
        origin = normalized_pop * simple_ions2

    with pytest.raises(ValueError):
        origin = simple_ions2 * normalized_pop


def test_can_change_ref_population(simple_ions):
    normalized_pop = simple_ions / simple_ions
    simple_ions2 = deepcopy(simple_ions)
    normalized_pop2 = normalized_pop.change(simple_ions,simple_ions2)


def test_save_and_load_json(simple_ions):
    test = jsonpickle.loads(jsonpickle.dumps(simple_ions))
    test2 = (test / simple_ions) * simple_ions
