#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Andreas Mussgiller
"""

import numpy as np

from physeng.iso2768 import ISO2768Length
from physeng.units import Length

iso2768length = ISO2768Length()

print(iso2768length.gradesForDimension(Length(2, 'mm')))
print(iso2768length.gradesForDimension(Length(40, 'mm')))
print(iso2768length.gradesForDimension(Length(3000, 'mm')))
print()

print(iso2768length.dimensionsForGrade('f'))
print(iso2768length.dimensionsForGrade('m'))
print(iso2768length.dimensionsForGrade('c'))
print(iso2768length.dimensionsForGrade('v'))
print()

print(iso2768length.tolerance(Length(5, 'mm'), 'f'))
