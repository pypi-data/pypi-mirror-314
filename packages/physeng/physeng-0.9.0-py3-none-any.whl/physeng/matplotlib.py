#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Andreas Mussgiller
"""

import math
import numpy as np
from matplotlib import ticker

class HoursFromSecondsLocator(ticker.Locator):
    def __init__(self, interval = 2):
        self.__interval = interval

    def __call__(self):
        vmin, vmax = self.axis.get_view_interval()
        #hmin = self.__hours(vmin)
        #hmax = self.__hours(vmax)
        ticks = np.linspace(0, 24*60*60, int(24/self.__interval)+1)
        return ticks

    def __hours(self, x):
        return int(math.floor(x/(60*60)))

class TimeFromSecondsFormatter(ticker.Formatter):
    def __call__(self, x, pos=None):
        hours = math.floor(x/(60*60))
        minutes = math.floor(x/60) - hours * 60
        return '{:02d}:{:02d}'.format(hours, minutes)
