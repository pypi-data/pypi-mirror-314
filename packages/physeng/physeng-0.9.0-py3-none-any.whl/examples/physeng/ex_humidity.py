#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Andreas Mussgiller
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from physeng.humidity import Humidity as h
from physeng.units import *

def plotsaturationVaporPressure():
    arrX = [Temperature(T, '°C') for T in np.arange(-50, 101, 1)]
    arrYWagnerPruss = [h.saturationVaporPressureWagnerPruss(T) for T in arrX]
    arrYAlduchovEskridge = [h.saturationVaporPressureAlduchovEskridge(T) for T in arrX]
   
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_xlabel('Temperature [°C]')
    ax.set_ylabel('Pressure [hPa]')
    ax.set_title('Saturation Vapour Pressure')
    
    
    ax.plot([v.asFloat('°C') for v in arrX],
            [v.asFloat('hPa') for v in arrYWagnerPruss],
            label = "Wagner and Pruß")
    
    ax.plot([v.asFloat('°C') for v in arrX],
            [v.asFloat('hPa') for v in arrYAlduchovEskridge],
            label = "Alduchov and Eskridge")
    
    ax.legend()
    plt.show()

def plotDewPoint():
    ah1 = h.absoluteHumidity(Temperature( 20, '°C'), 0.45)
    ah2 = h.absoluteHumidity(Temperature( 20, '°C'), 0.04)
    ah3 = h.absoluteHumidity(Temperature(  0, '°C'), 0.04)
    ah4 = h.absoluteHumidity(Temperature(-20, '°C'), 0.04)
    
    arrX = [Temperature(T, '°C') for T in np.arange(-45, 101, 1)]
    arrY1 = [h.dewPointFromAbsoluteHumidity(T, ah1) for T in arrX]
    arrY2 = [h.dewPointFromAbsoluteHumidity(T, ah2) for T in arrX]
    arrY3 = [h.dewPointFromAbsoluteHumidity(T, ah3) for T in arrX]
    arrY4 = [h.dewPointFromAbsoluteHumidity(T, ah4) for T in arrX]
    
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_xlabel('Temperature [°C]')
    ax.set_ylabel('Dew Point [°C]')
    
    ax.plot([v.asFloat('°C') for v in arrX],
            [v.asFloat('°C') for v in arrY1],
            label='$rel_h$ = 45% @ 20°C')
    ax.plot([v.asFloat('°C') for v in arrX],
            [v.asFloat('°C') for v in arrY2],
            label='$rel_h$ = 4% @ 20°C')
    ax.plot([v.asFloat('°C') for v in arrX],
            [v.asFloat('°C') for v in arrY3],
            label='$rel_h$ = 4% @ 0°C')
    ax.plot([v.asFloat('°C') for v in arrX],
            [v.asFloat('°C') for v in arrY4],
            label='$rel_h$ = 4% @ -20°C')
    
    ax.legend(title='$\\rho_v$ = const (closed vessel)')
    plt.show()

def plotRelativeHumidity():
    ah1 = h.absoluteHumidity(Temperature( 20, '°C'), 0.45)
    ah2 = h.absoluteHumidity(Temperature( 20, '°C'), 0.04)
    ah3 = h.absoluteHumidity(Temperature(  0, '°C'), 0.04)
    ah4 = h.absoluteHumidity(Temperature(-20, '°C'), 0.04)
    
    arrX1 = [Temperature(T, '°C') for T in np.arange(  7.00, 101, 1)]
    arrX2 = [Temperature(T, '°C') for T in np.arange(-25.25, 101, 1)]
    arrX3 = [Temperature(T, '°C') for T in np.arange(-39.00, 101, 1)]
    arrX4 = [Temperature(T, '°C') for T in np.arange(-53.20, 101, 1)]
    arrY1 = [h.relativeHumidityFromAbsoluteHumidity(T, ah1) for T in arrX1]
    arrY2 = [h.relativeHumidityFromAbsoluteHumidity(T, ah2) for T in arrX2]
    arrY3 = [h.relativeHumidityFromAbsoluteHumidity(T, ah3) for T in arrX3]
    arrY4 = [h.relativeHumidityFromAbsoluteHumidity(T, ah4) for T in arrX4]
    
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_xlabel('Temperature [°C]')
    ax.set_ylabel('Relative Humidity [%]')
    
    ax.plot([v.asFloat('°C') for v in arrX1],
            [v.asFloat('%') for v in arrY1],
            label='$rel_h$ = 45% @ 20°C')
    ax.plot([v.asFloat('°C') for v in arrX2],
            [v.asFloat('%') for v in arrY2],
            label='$rel_h$ = 4% @ 20°C')
    ax.plot([v.asFloat('°C') for v in arrX3],
            [v.asFloat('%') for v in arrY3],
            label='$rel_h$ = 4% @ 0°C')
    ax.plot([v.asFloat('°C') for v in arrX4],
            [v.asFloat('%') for v in arrY4],
            label='$rel_h$ = 4% @ -20°C')
    
    ax.set_yscale('log')
    ax.legend(title='$\\rho_v$ = const (closed vessel)')
    plt.show()

def plotFlushing():
    # lab air is 20°C and 45% relative humidity
    ah1 = h.absoluteHumidity(Temperature(20, '°C'), 0.45)
    # dry air for flushing is 20°C with a dew point of -70°C
    ah2 = h.absoluteHumidityFromDewPoint(Temperature(20, '°C'),
                                         Temperature(-70, '°C'))
    
    arr_t = [Duration(d, 's') for d in np.logspace(0, np.log10(7*24*60*60), 500)]
    #for t in arr_t: print(t)
    
    V1s = [Volume(v, 'm^3') for v in [1.0, 10.0, 3.9*1.6*2.5]]
    #for v in V1s: print(v)
    
    dV2dts = [VolumeFlowRate(dVdt, 'l/min') for dVdt in [50, 100, 200]]
    #for dVdt in dV2dts: print(dVdt)
    
    lineStyles = ['dotted', 'solid', 'dashed']
    
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_xlabel('Time [h]')
    ax.xaxis.set_major_locator(ticker.FixedLocator([0, 8, 16, 24, 36, 48, 60, 72, 96, 120, 144, 168]))
    ax.set_ylabel('Dew Point [°C]')
    ax.set_title('Dew Point vs. Flushing Time')
    
    for dVdt, ls in zip(dV2dts, lineStyles):
        ax.plot([], [],
                color='black',
                linestyle=ls,
                label=dVdt.asString('l/min'))
    
    for i,V1 in enumerate(V1s):
    
        arr_Tds = []
    
        for dV2dt in dV2dts:
            
            arr_Td = []
    
            for t in arr_t:
                # Volume of dry air that the vessel has been flushed with [m^3]
                V2 = dV2dt * t
                #V2 = Volume(dV2dt * 1e-3/60 * t, 'm^3')
                
                # total volume: volume of vessel + volume of dry air that the vessel has been flushed with [m^3]
                V = V1 + V2
                
                # total mass of water vapour
                m_w = V1 * ah1 + V2 * ah2
                
                # absolute humidity in flushed vessel
                ah = m_w / V
                
                arr_Td.append(h.dewPointFromAbsoluteHumidity(Temperature(20, '°C'), ah))
    
            arr_Tds.append(arr_Td)
    
        for j,dVdt in enumerate(dV2dts):
            if j==1:
                ax.plot([t.asFloat('h') for t in arr_t],
                        [td.asFloat('°C') for td in arr_Tds[j]],
                        color=plt.rcParams['axes.prop_cycle'].by_key()['color'][i],
                        linestyle=lineStyles[j],
                        label='{:.1f} $m^3$'.format(V1.asFloat('m^3')))
            else:
                ax.plot([t.asFloat('h') for t in arr_t],
                        [td.asFloat('°C') for td in arr_Tds[j]],
                        color=plt.rcParams['axes.prop_cycle'].by_key()['color'][i],
                        linestyle=lineStyles[j])
            
    ax.set_axisbelow(True)
    ax.yaxis.grid(color='lightgray', linestyle='solid')
    ax.xaxis.grid(color='lightgray', linestyle='solid')
    
    ax.legend(title='rel. h$_{vessel}$ = 45% @ 20°C\ndp$_{dry\\,air}$ = -70°C')
    plt.show()


plotsaturationVaporPressure()
plotDewPoint()
plotRelativeHumidity()
plotFlushing()

