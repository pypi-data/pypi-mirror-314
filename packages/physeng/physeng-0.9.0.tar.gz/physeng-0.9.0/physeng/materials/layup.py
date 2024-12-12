#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Andreas Mussgiller
"""

import math
import numpy as np

from collections.abc import Iterable

from physeng.singleton import Singleton
from physeng.units import *

from physeng.materials.utilities import MaterialDBException
from physeng.materials.materialproperty import MaterialProperty
from physeng.materials.material import Material
from physeng.materials.orthotropicmaterial import OrthotropicMaterial
from physeng.materials.ply import Ply

class Layup(OrthotropicMaterial):
    def __init__(self, name, title):
        super().__init__(name, title, None)
        Material._logger.debug(f'__init__: {name}, {title}')
        
        self._plies = []

    def addPly(self, ply: Ply, angle: float, thickness: Length):
        self._plies.append((ply, angle, thickness))

        self._totalThickness = Length(0, 'mm')
        for (p,a,t) in self._plies:
            self._totalThickness += t
        
        d = Density(0)
        for (p,a,t) in self._plies:
            d += p.Density * ( t / self._totalThickness )
        p = MaterialProperty('Density', d, None, None)
        self.addProperty(p)

        cX = AbsoluteThermalConductance(0)
        cY = AbsoluteThermalConductance(0)
        RZ = ThermalResistance(0)
        for (p,a,t) in self._plies:
            cX += p.thermalConductivityXY(-1.0 * a) * t
            cY += p.thermalConductivityXY(90.0 + -1.0 * a) * t
            RZ += t / p.ThermalConductivityZ;
        
        kx = cX / self._totalThickness
        self._kx = kx.asFloat('W/(m*K)')
        p = MaterialProperty('ThermalConductivity', kx, None, 'X')
        self.addProperty(p)
        
        ky = cY / self._totalThickness
        self._ky = kx.asFloat('W/(m*K)')
        p = MaterialProperty('ThermalConductivity', ky, None, 'Y')
        self.addProperty(p)
        
        kz = self._totalThickness / RZ
        self._kz = kx.asFloat('W/(m*K)')
        p = MaterialProperty('ThermalConductivity', kz, None, 'Z')
        self.addProperty(p)
        
    def thermalConductivityXY(self, angle):
        if not isinstance(angle, Iterable):
            c = AbsoluteThermalConductance(0)
            for (p,a,t) in self._plies:
                c += p.thermalConductivityXY(a - angle) * t
            return c / self._totalThickness
        else:
            kxys = []
            for a1 in angle:
                c = AbsoluteThermalConductance(0)
                for (p,a,t) in self._plies:
                    c += p.thermalConductivityXY(a - a1) * t
                kxys.append(c / self._totalThickness)
            return kxys
