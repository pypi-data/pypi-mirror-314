#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Andreas Mussgiller
"""

import numpy as np
import matplotlib.pyplot as plt

from physeng.units import *

from physeng.materials.materialdb import MaterialDB
from physeng.materials.ply import Ply

plt.rcParams.update({
    'figure.figsize': (4, 4),
    'font.size': 6,
})

matDB = MaterialDB()

fiberC2U = matDB.getMaterial('Mitsubishi K13C2U')
fiberD2U = matDB.getMaterial('Mitsubishi K13D2U')
matrix = matDB.getMaterial('Toray EX-1515')

plyC2U = Ply('K13C2U/EX1515', '67% K13C2U / 33% EX1515',
             fiberC2U, Dimensionless(0.67),
             matrix, Dimensionless(0.33))

plyD2U = Ply('K13D2U/EX1515', '67% K13D2U / 33% EX1515',
             fiberD2U, Dimensionless(0.67),
             matrix, Dimensionless(0.33))

phi = np.linspace(0, 360, 120, True)
kxysC2U = plyC2U.thermalConductivityXY(phi)
kxysD2U = plyD2U.thermalConductivityXY(phi)

fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

ax.plot(np.pi*phi/180.,
        [k.asFloat('W/(m*K)') for k in kxysC2U],
        label=plyC2U.title())

ax.plot(np.pi*phi/180.,
        [k.asFloat('W/(m*K)') for k in kxysD2U],
        label=plyD2U.title())

ax.set_rmax(600)
ax.set_rticks(np.arange(100, 600, 100))

ax.set_rlabel_position(-45)

ax.grid(True)

ax.legend(fontsize=5)

plt.show()
