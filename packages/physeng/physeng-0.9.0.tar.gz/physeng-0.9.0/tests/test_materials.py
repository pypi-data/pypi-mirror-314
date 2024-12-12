#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Andreas Mussgiller
"""

import pytest
from physeng.units import *
from physeng.materials import *


def test_Materials():
    matDB = MaterialDB()
        
    mat = matDB.getMaterial('Entegris PocoFoam')
    
    k1 = mat.ThermalConductivityZ
    k2 = ThermalConductivity(135.0, 'W/(m*K)')
    
    assert k1 == k2
