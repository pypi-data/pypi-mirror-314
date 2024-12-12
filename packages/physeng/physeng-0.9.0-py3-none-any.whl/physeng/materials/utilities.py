#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: mussgill
"""

class MaterialDBException(Exception):
    def __init__(self, message):
        self.message = message
