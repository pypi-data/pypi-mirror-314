#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: mussgill
"""

import importlib.resources as pkg_resources
import xml.etree.ElementTree as ET

import logging

from physeng.singleton import Singleton
from physeng.units import *

from physeng.materials.utilities import MaterialDBException

class MaterialProperty():
    
    _logger = None
    
    def __init__(self, name, Value, Tref, Axis = None):
        if MaterialProperty._logger is None:
            logging.basicConfig(format="{asctime} [{levelname}:{name}]: {message}",
                                style="{",
                                datefmt="%Y-%m-%d %H:%M",
                                level=logging.INFO)
            MaterialProperty._logger = logging.getLogger('MaterialProperty')
        MaterialProperty._logger.debug(f'__init__: {name}')

        self._Name = name
        self._Values = {Tref: Value}
        self._Axis = Axis
        
    @classmethod
    def fromXML(cls, element):
        
        name = element.tag
        values = element.attrib
        
        dimension = name
        if name not in globals():
            if 'Dimension' not in values.keys():
                raise MaterialDBException(f"MaterialProperty '{name}' unknown and dimension not specified")
            dimension = values['Dimension']
        
        Value = globals()[dimension](float(values['Value']), values['Unit'])
        
        Tref = None
        if 'T' in values.keys() and 'Tunit' in values.keys():
            Tref = Temperature(float(values['T']), values['Tunit'])
                
        Axis = None
        if 'Axis' in values.keys():
            a = values['Axis'].upper()
            if a!='X' and a!='Y' and a!='Z':
                raise MaterialDBException(f"Material axis '{a}' unknown")
            Axis = a
                       
        return cls(name, Value, Tref, Axis)
           
    def name(self):
        return self._Name
            
    def axis(self):
        return self._Axis
    
    def value(self, Tref: Temperature = None):
        return list(self._Values.values())[0]
    
    def values(self):
        return list(self._Values.values())
    
    def referencetemperature(self):
        return list(self._Values.keys())[0]
        
    def referencetemperatures(self):
        return list(self._Values.keys())
    
    def __str__(self):
        t = ''
        n = self._Name
        if self._Axis is not None:
            n += ' ' + self._Axis
        for k,v in self._Values.items():
            if t != '': t += '\n'
            t += f"{n:30s}"
            t += f"{v.value(v.preferredUnit()):9.3f} "
            t += f"{v.preferredUnit()}"
            if k is not None:
                t += f" (@{k.asString()})"
            n = ''
        return t

class TemperatureDependentMaterialProperty():
    
    _logger = None
    
    def __init__(self, name, TemperatureDependentValues, Axis = None):
        if TemperatureDependentMaterialProperty._logger is None:
            logging.basicConfig(format="{asctime} [{levelname}:{name}]: {message}",
                                style="{",
                                datefmt="%Y-%m-%d %H:%M",
                                level=logging.INFO)
            TemperatureDependentMaterialProperty._logger = logging.getLogger('TemperatureDependentMaterialProperty')
        TemperatureDependentMaterialProperty._logger.debug(f'__init__: {name}')

        self._Name = name
        self._Values = TemperatureDependentValues
        self._Axis = Axis
       
    @classmethod
    def fromXML(cls, element):
        
        name = element.tag
        values = element.attrib
        
        dimension = name
        if name not in globals():
            if 'Dimension' not in values.keys():
                raise MaterialDBException(f"MaterialProperty '{name}' unknown and dimension not specified")
            dimension = values['Dimension']
        
        Axis = None
        if 'Axis' in values.keys():
            a = values['Axis'].upper()
            if a!='X' and a!='Y' and a!='Z':
                raise MaterialDBException(f"Material axis '{a}' unknown")
            Axis = a
        
        TemperatureDependentValues = {}
        tvs = element.findall('Value')
        for v in tvs:
            values = v.attrib
            Value = globals()[dimension](float(values['Value']), values['Unit'])
            
            if 'T' in values.keys() and 'Tunit' in values.keys():
                Tref = Temperature(float(values['T']), values['Tunit'])
            else:
                Tref = None
            
            TemperatureDependentValues[Tref] = Value
            
        return cls(name, TemperatureDependentValues, Axis)
            
    def name(self):
        return self._Name
            
    def axis(self):
        return self._Axis
    
    def value(self, Tref: Temperature = None):
        return list(self._Values.values())[0]
    
    def values(self):
        return list(self._Values.values())
    
    def referencetemperature(self):
        return list(self._Values.keys())[0]
        
    def referencetemperatures(self):
        return list(self._Values.keys())
    
    def __str__(self):
        t = ''
        n = self._Name
        if self._Axis is not None:
            n += ' ' + self._Axis
        for k,v in self._Values.items():
            if t != '': t += '\n'
            t += f"{n:30s}"
            t += f"{v.value(v.preferredUnit()):9.3f} "
            t += f"{v.preferredUnit()}"
            if k is not None:
                t += f" (@{k.asString()})"
            n = ''
        return t

class DerivedMaterialProperty(MaterialProperty):
    def __init__(self, name, Value, Tref, Axis = None):
        super().__init__(name, Value, Tref, Axis)
        MaterialProperty._logger.debug(f'__init__: {name}')
        
    def __str__(self):
        t = ''
        n = self._Name
        if self._Axis is not None:
            n += ' ' + self._Axis
        n += ' *'
        for k,v in self._Values.items():
            if t != '': t += '\n'
            t += f"{n:30s}"
            t += f"{v.value(v.preferredUnit()):9.3f} "
            t += f"{v.preferredUnit()}"
            if k is not None:
                t += f" (@{k.asString()})"
            n = ''
        return t

class DerivedTemperatureDependentMaterialProperty(TemperatureDependentMaterialProperty):
    def __init__(self, name, TemperatureDependentValues, Axis = None):
        super().__init__(name, TemperatureDependentValues, Axis)
        TemperatureDependentMaterialProperty._logger.debug(f'__init__: {name}')
        
    def __str__(self):
        t = ''
        n = self._Name
        if self._Axis is not None:
            n += ' ' + self._Axis
        n += ' *'
        for k,v in self._Values.items():
            if t != '': t += '\n'
            t += f"{n:30s}"
            t += f"{v.value(v.preferredUnit()):9.3f} "
            t += f"{v.preferredUnit()}"
            if k is not None:
                t += f" (@{k.asString()})"
            n = ''
        return t
