#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Andreas Mussgiller
"""

import math
import numbers

from physeng.units import Length, Angle

from .geometry import ArgumentError

class Point3D():
    
    def __init__(self, a, b, c):
        
        if isinstance(a, Length) and isinstance(b, Length) and isinstance(c, Length):
        
            self._x = a
            self._y = b
            self._z = c
        
        elif isinstance(a, Length) and isinstance(b, Angle) and isinstance(c, Angle):

            self._x = a * math.sin(b) * math.cos(c)
            self._y = a * math.sin(b) * math.sin(c)
            self._z = a * math.cos(b)
            
        elif isinstance(a, Length) and isinstance(b, Angle) and isinstance(c, Length):
            
            self._x = a * math.cos(b)
            self._y = a * math.sin(b)
            self._z = c
                   
        else:
            
            raise ArgumentError('unsupported argument types')
    
    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        if not isinstance(value, Length):
            raise ArgumentError('unsupported argument type: {type(value)}')
        self._x = value
    
    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if not isinstance(value, Length):
            raise ArgumentError('unsupported argument type: {type(value)}')
        self._y = value
    
    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        if not isinstance(value, Length):
            raise ArgumentError('unsupported argument type: {type(value)}')
        self._z = value
    
    def distanceTo(self, other):
        if not isinstance(other, Point3D):
            raise ArgumentError(f'unsupported argument type: {type(other)}')

        x1 = float(self._x)   
        y1 = float(self._y)   
        z1 = float(self._z)   
        x2 = float(other._x)   
        y2 = float(other._y)   
        z2 = float(other._z)   
        
        return Length(math.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2))
 
    def __str__(self):
        return f'Point3D({self._x}, {self._y}, {self._z})'
