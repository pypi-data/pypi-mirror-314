#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Andreas Mussgiller
"""

import pytest

from physeng.singleton import Singleton
    
def test_singletone():
    
    @Singleton
    class TestSingleton:
        pass

    test1 = TestSingleton()
    test2 = TestSingleton()
    
    assert test1 is test2
