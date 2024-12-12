#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Andreas Mussgiller
"""

import importlib.resources as pkg_resources
import xml.etree.ElementTree as ET

import logging

from physeng.singleton import Singleton
from physeng.units import *

from physeng.materials.utilities import MaterialDBException
from physeng.materials.materialproperty import *

class Material():
    
    _logger = None
    
    def __init__(self, name, title, category):
        if Material._logger is None:
            logging.basicConfig(format="{asctime} [{levelname}:{name}]: {message}",
                                style="{",
                                datefmt="%Y-%m-%d %H:%M",
                                level=logging.INFO)
            Material._logger = logging.getLogger('Material')
        Material._logger.debug(f'__init__: {name}, {title}')
        
        self._Name = name
        self._Title = title
        self._Category = category
        self._Groups = []
        self._Properties = {}

    def name(self):
        return self._Name

    def title(self):
        return self._Title
    
    def properties(self):
        return self._Properties

    def category(self):
        return self._Category
    
    def addToGroup(self, group):
        self._Groups.append(group)
    
    def addProperty(self, prop):
        self._logger.debug(f'addProperty: {prop.name()}')
        self._Properties[(prop.name(), prop.axis())] = prop
        
    def getProperty(self, prop: str, axis: str = None) -> MaterialProperty:
        if (prop, axis) in self._Properties:
            return self._Properties[(prop, axis)]
        raise MaterialDBException(f"Property {prop} {axis} not known to material {self.__Name}")
    
    def _initialize(self):
         for prop in self._Properties.keys():
            attribName = prop[0]
            if prop[1] is not None:
                attribName += prop[1]
            setattr(self, attribName, self._Properties[prop].value())

    def __str__(self):
        t =  f"{self.__class__.__name__}\n"
        t += f"Name:     {self._Name}\n"
        t += f"Title:    {self._Title}\n"
        t += f"Category: {self._Category}\n"
        t += "Groups:   "
        if len(self._Groups)==0:
            t += 'None'
        else:
            for i,g in enumerate(self._Groups):
                if i > 0:
                    t += ', '
                    t += g
        t += "\n"
        t += "Properties:\n"
        for n,p in self._Properties.items():
            p = str(p).replace('\n', '\n  ')
            t += '  ' + p + '\n'
        return t
