#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Andreas Mussgiller
"""

from physeng.materials.material import Material

class IsotropicMaterial(Material):
    def __init__(self, name, title, category):
        super().__init__(name, title, category)
        Material._logger.debug(f'__init__: {name}, {title}')
