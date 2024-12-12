#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Andreas Mussgiller
"""

import pytest
import math
import numpy as np

from physeng.units import Length, Angle
from physeng.geometry import *

def test_Geometry2D():

    p1 = Point2D(Length(1.0), Length(1.0))
    p2 = Point2D(Length(2.0), Length(2.0))
    
    d1 = p1.distanceTo(p2)
    
    assert d1==Length(math.sqrt(2))

    p3 = Point2D(Length(0.0), Length(2.0))
    
    v1 = 

if __name__ == '__main__':
    test_Geometry2D()
