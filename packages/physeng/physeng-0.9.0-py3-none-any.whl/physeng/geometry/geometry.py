#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Andreas Mussgiller
"""

class ArgumentError(Exception):
    def __init__(self, message):
        self.message = message
