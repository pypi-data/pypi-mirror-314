#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Andreas Mussgiller
"""

import pytest
from datetime import datetime
import physeng as pe

def test_DateTimeFromDecimalYear():
    dt = pe.DateTimeFromDecimalYear(2024.25)
    assert dt == datetime(2024, 4, 1, 12, 0, 0)
