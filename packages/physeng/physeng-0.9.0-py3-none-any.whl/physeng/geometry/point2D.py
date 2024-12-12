#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Andreas Mussgiller
"""

import math
import numbers

from physeng.units import Length, Angle

from .geometry import ArgumentError

class Point2D():
    
    def __init__(self, a, b):
        
        if isinstance(a, Length) and isinstance(b, Length):
            
            self._x = a
            self._y = b
        
        elif isinstance(a, Length) and isinstance(b, Angle):
        
            self._x = a * math.cos(b)
            self._y = a * math.sin(b)
        
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
    
    def distanceTo(self, other) -> Length:
        if not isinstance(other, Point2D):
            raise ArgumentError(f'unsupported argument type: {type(other)}')
            
        x1 = float(self._x)   
        y1 = float(self._y)   
        x2 = float(other._x)   
        y2 = float(other._y)   
        
        return Length(math.sqrt((x2-x1)**2 + (y2-y1)**2))
 
    def __str__(self):
        return f'Point2D({self._x}, {self._y})'
