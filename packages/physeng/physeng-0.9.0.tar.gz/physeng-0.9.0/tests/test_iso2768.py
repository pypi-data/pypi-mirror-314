#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Andreas Mussgiller
"""

import pytest
from physeng.iso2768 import ISO2768Length
from physeng.units import Length

def test_ISO2768():
    iso2768length = ISO2768Length()
    
    m2 = iso2768length.tolerance(Length(2, 'mm'), 'm')
    assert m2 == Length(0.100, 'mm')
