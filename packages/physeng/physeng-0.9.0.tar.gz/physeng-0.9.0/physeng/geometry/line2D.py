#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Andreas Mussgiller
"""

import math

from physeng.units import Angle

from .geometry import ArgumentError
from .point2D import Point2D
from .vector2D import Vector2D

class Line2D():
    
    def __init__(self, a, b):

        if isinstance(a, Point2D) and isinstance(b, Vector2D):
            
            self._point = a
            self._direction = b

        elif isinstance(a, Point2D) and isinstance(b, Point2D):
            
            self._point = a
            self._direction = Point2D(a, b)

        else:
            
            raise ArgumentError('unsupported argument types')
   
    @property
    def point(self):
        return self._point

    @point.setter
    def point(self, point):
        if not isinstance(point, Point2D):
            raise ArgumentError('provided argument p/point is not of type Point2D')
        self._point = point
    
    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, direction):
        if not isinstance(direction, Vector2D):
            raise ArgumentError('provided argument d/direction is not of type Vector2D')
        self._direction = direction
            
    def angleBetween(self, other) -> Angle:
        if not isinstance(other, Vector2D) or not isinstance(other, Line2D):
            raise ArgumentError('unsupported argument type: {type(other)}')
    
        v1 = self._direction.unit
        if isinstance(other, Vector2D):
            v2 = other.unit
        else:
            v2 = other.direction.unit
        
        angle = math.acos(v1.dot(v2))
        
        return Angle(angle)

    def __str__(self):
        return f'Line2D({self._point}, {self._direction})'
