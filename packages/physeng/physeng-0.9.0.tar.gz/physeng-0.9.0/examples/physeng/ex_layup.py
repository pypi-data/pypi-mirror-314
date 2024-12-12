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
from physeng.materials.layup import Layup

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

layupC2U1 = Layup('K13C2U/EX-1515 (67/33) (0/90/0)',
                  'K13C2U/EX-1515 (67/33) (0/90/0)')
layupC2U1.addPly(plyC2U,  0, Length(0.1, 'mm'))
layupC2U1.addPly(plyC2U, 90, Length(0.1, 'mm'))
layupC2U1.addPly(plyC2U,  0, Length(0.1, 'mm'))

layupC2U2 = Layup('K13C2U/EX-1515 (67/33) (0/90/90/0)',
                  'K13C2U/EX-1515 (67/33) (0/90/90/0)')
layupC2U2.addPly(plyC2U,  0, Length(0.1, 'mm'))
layupC2U2.addPly(plyC2U, 90, Length(0.1, 'mm'))
layupC2U2.addPly(plyC2U, 90, Length(0.1, 'mm'))
layupC2U2.addPly(plyC2U,  0, Length(0.1, 'mm'))

layupC2U3 = Layup('K13C2U/EX-1515 (67/33) (0/60/-60)s',
                  'K13C2U/EX-1515 (67/33) (0/60/-60)s')
layupC2U3.addPly(plyC2U,   0, Length(0.1, 'mm'))
layupC2U3.addPly(plyC2U,  60, Length(0.1, 'mm'))
layupC2U3.addPly(plyC2U, -60, Length(0.1, 'mm'))
layupC2U3.addPly(plyC2U, -60, Length(0.1, 'mm'))
layupC2U3.addPly(plyC2U,  60, Length(0.1, 'mm'))
layupC2U3.addPly(plyC2U,   0, Length(0.1, 'mm'))

layupD2U1 = Layup('K13D2U/EX-1515 (67/33) (0/90/0)',
                  'K13D2U/EX-1515 (67/33) (0/90/0)')
layupD2U1.addPly(plyD2U,  0, Length(0.1, 'mm'))
layupD2U1.addPly(plyD2U, 90, Length(0.1, 'mm'))
layupD2U1.addPly(plyD2U,  0, Length(0.1, 'mm'))

layupD2U2 = Layup('K13D2U/EX-1515 (67/33) (0/90/90/0)',
                  'K13D2U/EX-1515 (67/33) (0/90/90/0)')
layupD2U2.addPly(plyD2U,  0, Length(0.1, 'mm'))
layupD2U2.addPly(plyD2U, 90, Length(0.1, 'mm'))
layupD2U2.addPly(plyD2U, 90, Length(0.1, 'mm'))
layupD2U2.addPly(plyD2U,  0, Length(0.1, 'mm'))

layupD2U3 = Layup('K13D2U/EX-1515 (67/33) (0/60/-60)s',
                  'K13D2U/EX-1515 (67/33) (0/60/-60)s')
layupD2U3.addPly(plyD2U,   0, Length(0.1, 'mm'))
layupD2U3.addPly(plyD2U,  60, Length(0.1, 'mm'))
layupD2U3.addPly(plyD2U, -60, Length(0.1, 'mm'))
layupD2U3.addPly(plyD2U, -60, Length(0.1, 'mm'))
layupD2U3.addPly(plyD2U,  60, Length(0.1, 'mm'))
layupD2U3.addPly(plyD2U,   0, Length(0.1, 'mm'))

phi = np.linspace(0, 360, 120, True)
kxys_layupC2U1 = layupC2U1.thermalConductivityXY(phi)
kxys_layupC2U2 = layupC2U2.thermalConductivityXY(phi)
kxys_layupC2U3 = layupC2U3.thermalConductivityXY(phi)
kxys_layupD2U1 = layupD2U1.thermalConductivityXY(phi)
kxys_layupD2U2 = layupD2U2.thermalConductivityXY(phi)
kxys_layupD2U3 = layupD2U3.thermalConductivityXY(phi)

fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

ax.plot(np.pi*phi/180.,
        [k.asFloat('W/(m*K)') for k in kxys_layupC2U1],
        label=layupC2U1.title())
ax.plot(np.pi*phi/180.,
        [k.asFloat('W/(m*K)') for k in kxys_layupC2U2],
        label=layupC2U2.title())
ax.plot(np.pi*phi/180.,
        [k.asFloat('W/(m*K)') for k in kxys_layupC2U3],
        label=layupC2U3.title())

ax.plot(np.pi*phi/180.,
        [k.asFloat('W/(m*K)') for k in kxys_layupD2U1],
        label=layupD2U1.title())
ax.plot(np.pi*phi/180.,
        [k.asFloat('W/(m*K)') for k in kxys_layupD2U2],
        label=layupD2U2.title())
ax.plot(np.pi*phi/180.,
        [k.asFloat('W/(m*K)') for k in kxys_layupD2U3],
        label=layupD2U3.title())

ax.set_rmax(400)
ax.set_rticks(np.arange(100, 400, 100))

ax.set_rlabel_position(-45)

ax.grid(True)

ax.legend(fontsize=5)

plt.show()
