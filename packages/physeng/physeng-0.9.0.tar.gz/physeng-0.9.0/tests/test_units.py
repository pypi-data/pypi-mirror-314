#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Andreas Mussgiller
"""

import pytest
import numpy as np
from physeng.units import *

def test_Dimensionless():
    d0 = Dimensionless(3.0)
    d1 = Dimensionless(4.0)
    d2 = Dimensionless(7.0)

    assert d0 + d1 == d2
    assert d0 != d1
    assert d0 != 4.0
    assert d0 <= d1

def test_Length():
    l1 = Length(1.0, 'm')
    l2 = Length(100.0, 'cm')
    l3 = Length(2.0, 'm')
    
    assert np.isclose(l1.value(), l2.value()) == True
    
    l4 = l1 + l2
    
    assert np.isclose(l3.value(), l4.value()) == True
    
    a1 = l3 * l4
    a2 = Area(4.0, 'm^2')

    assert np.isclose(a1.value(), a2.value()) == True

def test_Area():
    a1 = Area(1.0, 'm^2')
    a2 = Area(10000.0, 'cm^2')
    a3 = Area(4.0, 'm^2')
    
    assert np.isclose(a1.value(), a2.value()) == True

def test_Density():
    m1 = Mass(2.0, 'kg')
    v1 = Volume(4.0, 'm^3')
    
    d1 = Density(0.5, 'kg/m^3')
    d2 = m1 / v1
    
    assert np.isclose(d1.value(), d2.value()) == True

def test_Pressure():
    f1 = Force(10.0, 'N')
    a1 = Area(1.0, 'm^2')
    
    p1 = Pressure(10.0, 'Pa')
    p2 = f1 / a1
    
    assert np.isclose(p1.value(), p2.value()) == True

def test_VolumeFlowRate():
    v1 = Volume(20.0, 'cm^3')
    t1 = Duration(5.0, 's')
    
    vr1 = VolumeFlowRate(4.0, 'cm^3/s')
    vr2 = v1 / t1
    
    assert np.isclose(vr1.value(), vr2.value()) == True

def test_MassFlowRate():
    m1 = Mass(20.0, 'g')
    t1 = Duration(5.0, 's')
    
    mr1 = MassFlowRate(4.0, 'g/s')
    mr2 = m1 / t1
    
    assert np.isclose(mr1.value(), mr2.value()) == True

def test_Velocity():
    s1 = Length(20.0, 'm')
    t1 = Duration(5.0, 's')
    
    v1 = Velocity(4.0, 'm/s')
    v2 = s1 / t1
    
    assert np.isclose(v1.value(), v2.value()) == True
    
    s2 = v2 * t1
    
    assert np.isclose(s1.value(), s2.value()) == True
    
def test_Energy():
    f1 = Force(10.0, 'N')
    s1 = Length(20.0, 'm')
    
    e1 = Energy(200.0, 'J')
    e2 = f1 * s1
    assert e1 == e2
    
    f2 = e2 /  s1
    assert f1 == f2

def test_Power():
    e1 = Energy(200.0 ,'J')
    t1 = Duration(1.0, 's')
    
    p1 = Power(200.0, 'W')
    p2 = e1 / t1
    assert p1 == p2
    
    e2 = p2 * t1
    assert e1 == e2

def test_Temperature():
    T1 = Temperature(293.15, 'K')
    T2 = Temperature(20.0, '°C')
    
    assert T1 == T2
    
    T3 = Temperature(273.15, 'K')
    
    dT1 = TemperatureDifference(20.0, '°C')
    dT2 = T1 - T3
    
    assert dT1 == dT2
    
    T4 = dT2 + T3
    assert T1 == T4
    
    T5 = T3 + dT2
    assert T1 == T5

def test_TemperatureGradient():
    T1 = Temperature(273.15, 'K')
    T2 = Temperature(20.0, '°C')
    dT1 = T2 - T1
    l1 = Length(1.0, 'm')
    
    dTdl1 = dT1 / l1
    dTdl2 = TemperatureGradient(20.0, 'K/m')
    assert dTdl1 == dTdl2
    
    dT2 = dTdl1 * l1
    assert dT1 == dT2

def test_ThermalConductivity():
    P1 = Power(1, 'W')
    l1 = Length(1, 'm')
    dT1 = TemperatureDifference(2.0, 'K')
    
    k1 = ThermalConductivity(0.5, 'W/(m*K)')
    r1 = 1/k1
    assert k1 == 1/r1    

    k2 = P1 / dT1 / l1
    assert k1 == k2
