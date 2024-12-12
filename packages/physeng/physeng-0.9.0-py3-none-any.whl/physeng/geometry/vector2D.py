#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Andreas Mussgiller
"""

import math
import numbers

from physeng.units import Length, Area, Angle

from .geometry import ArgumentError
from .point2D import Point2D

class Vector2D():
    
    def __init__(self, a, b):
        
        if isinstance(a, Point2D) and isinstance(b, Point2D):
            
            self._x = b.x - a.x
            self._y = b.y - a.y
        
        elif isinstance(a, Length) and isinstance(b, Length):

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

    @property
    def length(self) -> Length:
        return Length(math.sqrt(float(self._x)**2 + float(self._y)**2))

    @length.setter
    def length(self, value):
        if not isinstance(value, Length):
            raise ArgumentError('unsupported argument type: {type(value)}')
        pass
    
    @property
    def phi(self) -> Angle:
        return Angle(math.atan2(float(self._y), float(self._x)))
    
    @property
    def unit(self):
        l = float(self.length)
        return Vector2D(self._x/l, self._y/l)
    
    def dot(self, other) -> Area:
        if not isinstance(other, Vector2D):
            raise ArgumentError('unsupported argument type: {type(other)}')
            
        x1 = float(self._x)   
        y1 = float(self._y)   
        x2 = float(other._x)   
        y2 = float(other._y)   

        return Area(x1*x2 + y1*y2)
    
    def angleBetween(self, other) -> Angle:
        if not isinstance(other, Vector2D):
            raise ArgumentError('unsupported argument type: {type(other)}')
    
        v1 = self.unit
        v2 = other.unit
        
        angle = math.acos(v1.dot(v2))
        
        return Angle(angle)
    
    def __str__(self):
        return f'Vector2D({self._x}, {self._y})'
