#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Andreas Mussgiller
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.ticker as ticker

from physeng.iso286 import ISO286Hole, ISO286Shaft
from physeng.units import Length

iso286hole = ISO286Hole()
iso286shaft = ISO286Shaft()

(toleranceMin1, toleranceMax1) = iso286shaft.toleranceAsFloat(Length(2.5, 'mm'), 'g6')
(toleranceMin2, toleranceMax2) = iso286hole.toleranceAsFloat(Length(2.5, 'mm'), 'H7')

fig, axs = plt.subplots(2, 1, sharex=True, figsize=(8,4))
fig.subplots_adjust(hspace=0)

axs[0].set_title('$2.5f7$ / $2.5^{-6}_{-16}$ vs. $2.5H7$ / $2.5^{+10}_{+0}$')

axs[0].set_xlabel('[$\\mu m$]')
axs[0].xaxis.set_major_locator(ticker.MultipleLocator(5.0))
axs[0].xaxis.set_minor_locator(ticker.MultipleLocator(1.0))

axs[0].set_xlim([-40, 40])
axs[0].set_ylim([-1, 1])

rect = patches.Rectangle((toleranceMin1, -0.9),
                         toleranceMax1-toleranceMin1, 1.8,
                         linewidth=0, facecolor='lightgrey')
axs[0].add_patch(rect)

axs[0].plot([0,0], [-1,1],
            color='black',
            linewidth=2)

axs[0].yaxis.set_visible(False)
axs[0].xaxis.set_visible(False)
axs[0].set_frame_on(False)

axs[1].set_xlabel('[$\\mu m$]')
axs[1].xaxis.set_major_locator(ticker.MultipleLocator(5.0))
axs[1].xaxis.set_minor_locator(ticker.MultipleLocator(1.0))

axs[1].set_xlim([-40, 40])
axs[1].set_ylim([-1, 1])

rect = patches.Rectangle((toleranceMin2, -0.9),
                         toleranceMax2-toleranceMin2, 1.8,
                         linewidth=0, facecolor='lightgrey')
axs[1].add_patch(rect)

axs[1].plot([0,0], [-1,1],
            color='black',
            linewidth=2)

axs[1].yaxis.set_visible(False)
axs[1].set_frame_on(False)

plt.show()