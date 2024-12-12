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

class Ply(OrthotropicMaterial):
    def __init__(self, name, title,
                 fiber: Material, fibermassfraction: Dimensionless,
                 matrix: Material, matrixmassfraction: Dimensionless):
        super().__init__(name, title, None)
        Material._logger.debug(f'__init__: {name}, {title}')
        
        self._fiber = fiber
        self._fibermassfraction = fibermassfraction
        self._matrix = matrix
        self._matrixmassfraction = matrixmassfraction
        
        d = ( fiber.Density * fibermassfraction + 
              matrix.Density * matrixmassfraction )
        p = MaterialProperty('Density', d, None, None)
        self.addProperty(p)
        
        k = ( fibermassfraction * fiber.ThermalConductivityX  + 
              matrixmassfraction * matrix.ThermalConductivity )
        self._kx = k.asFloat('W/(m*K)')
        p = MaterialProperty('ThermalConductivity', k, None, 'X')
        self.addProperty(p)

        R = ( fibermassfraction / fiber.ThermalConductivityY + 
              matrixmassfraction / matrix.ThermalConductivity )
        k = ( fibermassfraction + matrixmassfraction ) / R
        self._ky = k.asFloat('W/(m*K)')
        p = MaterialProperty('ThermalConductivity', k, None, 'Y')
        self.addProperty(p)

        R = ( fibermassfraction / fiber.ThermalConductivityZ + 
              matrixmassfraction / matrix.ThermalConductivity )
        k = ( fibermassfraction + matrixmassfraction ) / R
        p = MaterialProperty('ThermalConductivity', k, None, 'Z')
        self.addProperty(p)
        
        self._initialize()
    
    def thermalConductivityXY(self, angle):
        if not isinstance(angle, Iterable):
            a = angle * np.pi / 180.
            kxy = self._amplitude(pow(math.cos(a), 4) * self._kx,
                                  pow(math.sin(a), 4) * self._ky)
            return ThermalConductivity(kxy, 'W/(m*K)')
        else:
            kxys = []
            for a in angle:
                a = a * np.pi / 180.
                kxy = self._amplitude(pow(math.cos(a), 4) * self._kx,
                                      pow(math.sin(a), 4) * self._ky)
                kxys.append(ThermalConductivity(kxy, 'W/(m*K)'))
            return kxys
        
    def _amplitude(self, x: float, y: float):
        return np.sqrt(x*x + y*y)
