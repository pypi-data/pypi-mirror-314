#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Andreas Mussgiller
"""

import pytest
import numpy as np

from physeng.humidity import Humidity as h
from physeng.units import *

def test_humidity():

    T = Temperature(293.0, 'K')
    p = Pressure(23.118590600388863, 'hPa')

    assert np.isclose(h.saturationVaporPressure(T).asFloat(),
                      p.asFloat()) == True
    
    Td = Temperature(285.0088776258169, 'K')
    
    assert np.isclose(h.dewPoint(T, 0.6).asFloat(),
                      Td.asFloat()) == True

    T = Temperature(293.15, 'K')
    ah = Density(0.0010348265917773552, 'g/cm^3')
   
    assert np.isclose(h.absoluteHumidity(T, 0.6).asFloat(),
                      ah.asFloat()) == True

    RH = h.relativeHumidityFromAbsoluteHumidity(T, ah)
    
    assert np.isclose(RH.asFloat(), 0.6) == True

    Td = Temperature(285.14989461574544, 'K')

    assert np.isclose(h.dewPointFromAbsoluteHumidity(T, ah).asFloat(),
                      Td.asFloat()) == True
     
    assert np.isclose(h.absoluteHumidityFromDewPoint(T, Td).asFloat(),
                      ah.asFloat()) == True
