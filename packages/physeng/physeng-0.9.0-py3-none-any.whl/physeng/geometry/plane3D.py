#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Andreas Mussgiller
"""

import math
import numbers

from physeng.units import Length, Area, Angle

from .geometry import ArgumentError
from .point3D import Point3D
from .vector3D import Vector3D

class Plane3D():
    
    def __init__(self, a, b, c = None):
        
        if isinstance(a, Point3D) and isinstance(b, Vector3D) and c==None:
            
            # Point and Normal
            self._point = a
            self._normal = b.unit
        
        elif isinstance(a, Point3D) and isinstance(b, Point3D) and isinstance(c, Point3D):

            # Three Points
            self._point = a
            v1 = Vector3D(a, b)
            v2 = Vector3D(a, c)
            self._normal = v1.cross(v2).unit
            
        elif isinstance(a, Point3D) and isinstance(b, Vector3D) and isinstance(c, Vector3D):
            
            # Point and two Vectors
            self._point = a
            self._normal = b.cross(c).unit
        
        else:
            
            raise ArgumentError('unsupported argument types')

    def __str__(self):
        return f'Plane3D({self._point}, {self._normal})'
