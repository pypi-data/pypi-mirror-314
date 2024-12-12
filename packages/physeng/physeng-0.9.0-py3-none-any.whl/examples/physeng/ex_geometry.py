#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Andreas Mussgiller
"""

import math
import numpy as np
import matplotlib.pyplot as plt

from physeng.units import Length, Angle
from physeng.geometry import *

p1 = Point2D(Length(1.0, 'm'), Length(1.0, 'm'))
p2 = Point2D(Length(2.0, 'm'), Length(2.0, 'm'))
print(p1.distanceTo(p2))

v1 = Vector2D(p1, p2)
print(v1, v1.length)

l1 = Line2D(p2, v1)
print(l1)

p3 = Point3D(Length(1.0, 'm'), Length(1.0, 'm'), Length(1.0, 'm'))
p4 = Point3D(Length(2.0, 'm'), Length(2.0, 'm'), Length(2.0, 'm'))
print(p3.distanceTo(p4))

v2 = Vector3D(p3, p4)
print(v2.length)

l2 = Line3D(p3, v2)
print(l2)

p1 = Point3D(Length(1.0, 'm'), Length(1.0, 'm'), Length(1.0, 'm'))
p2 = Point3D(Length(2.0, 'm'), Length(2.0, 'm'), Length(1.0, 'm'))
p3 = Point3D(Length(2.0, 'm'), Length(-2.0, 'm'), Length(1.0, 'm'))

p1 = Plane3D(p1, p2, p3)
print(p1)

print()

p1 = Point2D(Length(0.0, 'm'), Length(0.0, 'm'))
p2 = Point2D(Length(1.0, 'm'), Length(0.0, 'm'))
p3 = Point2D(Length(0.0, 'm'), Length(1.0, 'm'))

v1 = Vector2D(p1, p2)
v2 = Vector2D(p1, p3)

print(v1.angleBetween(v2))

