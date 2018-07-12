#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `Quantity` class."""

import pytest
from astropy.units import UnitConversionError
import astropy.units as u
from whampyr.plasma.quantity import Quantity


@pytest.fixture
def default_constructed():
    # a default constructed quantity should be 0. with no unit
    return Quantity()


@pytest.fixture
def simple_speed():
    # a default constructed quantity should be 0. with no unit
    return Quantity(1., 'km/s')


def test_default_constructed_should_be_zero(default_constructed):
    q = default_constructed
    assert q.value() == 0.
    assert q.converted('') == 0.


def test_default_constructed_should_be_without_unit(default_constructed):
    q = default_constructed
    assert q.value().unit == u.Unit('')
    with pytest.raises(UnitConversionError):
        q.converted('m/s')

def test_can_multiply_and_divide_quantities(simple_speed):
    test = simple_speed * simple_speed / simple_speed
    assert test == simple_speed

def test_can_construct_a_quantity(simple_speed):
    q = simple_speed
    assert q.value() == 1. * u.Unit('km/s')
    assert q.converted('m/s') == 1000. * u.Unit('m/s')
    assert q.si_val('m/s') == 1000.
    assert (q.value()/q.value()).unit == u.Unit('')
    with pytest.raises(UnitConversionError):
        q.converted('J')
