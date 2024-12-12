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

class Vector3D():
    
    def __init__(self, a, b, c = None):
        
        if isinstance(a, Point3D) and isinstance(b, Point3D) and c==None:
            
            self._x = b.x - a.x
            self._y = b.y - a.y
            self._z = b.y - a.z
        
        elif isinstance(a, Length) and isinstance(b, Length) and isinstance(c, Length):

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

    @property
    def length(self) -> Length:
        return Length(math.sqrt(float(self._x)**2 + float(self._y)**2 + float(self._z)**2))

    @length.setter
    def length(self, value):
        if not isinstance(value, Length):
            raise ArgumentError('unsupported argument type: {type(value)}')
        pass
    
    @property
    def theta(self) -> Angle:
        
        lxy = math.sqrt(float(self._x)**2 + float(self._y)**2)
        
        if self._z>0:
            t = math.atan2(lxy, self._z)
        elif self._z<0:
            t = math.pi + math.atan2(lxy, self._z)
        else:
            if lxy!=0.0:
                t = math.pi/2
            else:
                t = math.nan
        
        return Angle(t)
    
    @property
    def phi(self) -> Angle:
        
        if self._x>0:
            t = math.atan2(self._y, self._x)
        elif self._x<0 and self._y>=0:
            t = math.atan2(self._y, self._x) + math.pi
        elif self._x<0 and self._y<0:
            t = math.atan2(self._y, self._x) - math.pi
        elif self._x==0 and self._y>0:
            t = math.pi/2
        elif self._x==0 and self._y<0:
            t = -math.pi/2
        else:
            t = math.nan
            
        return Angle(t)
        
    @property
    def unit(self):
        l = float(self.length)
        return Vector3D(self._x/l, self._y/l, self._z/l)
    
    def dot(self, other) -> Area:
        if not isinstance(other, Vector3D):
            raise ArgumentError('unsupported argument type: {type(other)}')

        x1 = float(self._x)   
        y1 = float(self._y)   
        z1 = float(self._z)   
        x2 = float(other._x)   
        y2 = float(other._y)   
        z2 = float(other._z)   

        return Area(x1*x2 + y1*y2 + z1*z2)
    
    def cross(self, other):
        if not isinstance(other, Vector3D):
            raise ArgumentError('unsupported argument type: {type(other)}')

        x1 = float(self._x)
        y1 = float(self._y)
        z1 = float(self._z)
        x2 = float(other._x)
        y2 = float(other._y)
        z2 = float(other._z)

        x3 = y1*z2 - z1*y2
        y3 = z1*x2 - x1*z2
        z3 = x1*y2 - y1*x2

        return Vector3D(Length(x3), Length(y3), Length(z3))
    
    def angleBetween(self, other) -> Angle:
        if not isinstance(other, Vector3D):
            raise ArgumentError('unsupported argument type: {type(other)}')
    
        v1 = self.unit
        v2 = other.unit
        
        angle = math.acos(v1.dot(v2))
        
        return Angle(angle)

    def __str__(self):
        return f'Vector3D({self._x}, {self._y}, {self._z})'
