#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Andreas Mussgiller
"""

import pytest
from physeng.iso286 import ISO286Hole, ISO286Shaft
from physeng.units import Length

def test_ISO286():
    iso286hole = ISO286Hole()
    iso286shaft = ISO286Shaft()
    
    dm6 = iso286shaft.dimensionsForGrade('m6')
    assert dm6 == (Length(0.0, 'mm'), Length(400.0, 'mm'))
    
    t4m6 = iso286shaft.tolerance(Length(4.0, 'mm'), 'm6')
    assert t4m6 == (Length(4.0, 'um'), Length(12.0, 'um'))
    
    dH7 = iso286hole.dimensionsForGrade('H7')
    assert dH7 == (Length(0.0, 'mm'), Length(400.0, 'mm'))
    
    t16H7 = iso286hole.tolerance(Length(16.0, 'mm'), 'H7')
    assert t16H7 == (Length(0.0, 'um'), Length(18.0, 'um'))
