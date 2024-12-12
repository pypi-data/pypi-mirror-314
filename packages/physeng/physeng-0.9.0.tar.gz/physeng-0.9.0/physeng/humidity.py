#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Andreas Mussgiller
"""

import numpy as np 

from physeng.singleton import Singleton
from physeng.units import Dimensionless, Temperature, Pressure, Density

@Singleton
class Humidity:

    @staticmethod
    def saturationVaporPressureWagnerPruss(T: Temperature) -> Pressure:
        '''
        Returns the saturation water vapor pressure according to Wagner
        and Pruss (https://doi.org/10.1063/1.1461829) for a given temperature.

        Parameters
        ----------
        T : Temperature
            Temperature

        Returns
        -------
        Pressure
            Saturation water vapor pressure
        '''
            
        Tv = T.asFloat('K')
        Tc = 647.096 # K
        Pc = 220640 # hPa
    
        C1 = -7.85951783
        C2 = 1.84408259
        C3 = -11.7866497
        C4 = 22.6807411
        C5 = -15.9618719
        C6 = 1.80122502
    
        t = 1.0 - Tv/Tc
    
        temp = C1 * t
        temp += C2 * np.power(t, 1.5)
        temp += C3 * np.power(t, 3.0)
        temp += C4 * np.power(t, 3.5)
        temp += C5 * np.power(t, 4.0)
        temp += C6 * np.power(t, 7.5)
        temp *= Tc/Tv
    
        return Pressure(Pc * np.exp(temp), 'hPa')
        
    @staticmethod
    def saturationVaporPressureAlduchovEskridge(T: Temperature) -> Pressure:
        '''
        Returns the saturation water vapor pressure according to Alduchov
        and Eskridge (https://doi.org/10.1175/1520-0450(1996)035%3C0601:IMFAOS%3E2.0.CO;2)
        for a given temperature.

        Parameters
        ----------
        T : Temperature
            Temperature

        Returns
        -------
        Pressure
            Saturation water vapor pressure
        '''
        
        Tv = T.asFloat('K')
        A = 17.625
        B = 243.04 # °C
        C = 6.1094 # Pa;

        return Pressure(C * np.exp(A*(Tv-273.15)/(B+(Tv-273.15))), 'hPa')
    
    @staticmethod
    def saturationVaporPressure(T: Temperature) -> Pressure:
        '''
        Returns the saturation water vapor pressure according to Alduchov
        and Eskridge (https://doi.org/10.1175/1520-0450(1996)035%3C0601:IMFAOS%3E2.0.CO;2)
        for a given temperature.
        
        Parameters
        ----------
        T : Temperature
            Temperature

        Returns
        -------
        Pressure
            Saturation water vapor pressure
        '''

        return Humidity.saturationVaporPressureAlduchovEskridge(T)
        
    @staticmethod
    def waterVaporPartialPressure(T: Temperature, relH: Dimensionless) -> Pressure:
        '''
        Returns the water vapor partial pressure for a given temperature and
        relative humidity.

        Parameters
        ----------
        T : Temperature
            Temperature
        relH : Dimensionless
            Relative humnidity

        Returns
        -------
        Pressure
            water vapor partial pressure
        '''
        
        return Humidity.saturationVaporPressure(T) * relH

    @staticmethod
    def absoluteHumidity(T: Temperature, relH: Dimensionless) -> Density:
        '''
        Returns the absolute humidity for a given temperature and relative
        humidity.

        Parameters
        ----------
        T : Temperature
            Temperature
        relH : Dimensionless
            Relative humnidity

        Returns
        -------
        Density
            Absolute humidity
        '''
        
        return Density(10 * Humidity.waterVaporPartialPressure(T, relH).asFloat('hPa') /
                       (461.52 * T.asFloat()), 'g/cm^3')

    @staticmethod
    def dewPointLawrence(T: Temperature, relH: Dimensionless) -> Temperature:
        '''
        Returns the dew point according to Lawrence
        (https://doi.org/10.1175/BAMS-86-2-225) for a given temperature and
        relative humidity.

        Parameters
        ----------
        T : Temperature
            Temperature
        relH : Dimensionless
            Relative humnidity

        Returns
        -------
        Temperature
            Dew point

        '''
        
        A = 17.625
        B = 243.04 # °C
        C = 610.94 # Pa

        pp = Humidity.waterVaporPartialPressure(T, relH).asFloat('Pa')

        return Temperature(273.15 + B*np.log(pp/C)/(A-np.log(pp/C)), 'K')

    @staticmethod
    def dewPoint(T: Temperature, relH: Dimensionless) -> Temperature:
        '''
        Returns the dew point according to Lawrence
        (https://doi.org/10.1175/BAMS-86-2-225) for a given temperature and
        relative humidity.

        Parameters
        ----------
        T : float
            Temperature in K
        relH : float
            Relative humnidity [0,1]

        Returns
        -------
        float
            Dew point in K

        '''

        return Humidity.dewPointLawrence(T, relH)
    
    @staticmethod
    def relativeHumidityFromAbsoluteHumidity(T: Temperature, ah: Density) -> Dimensionless:
        '''
        Returns the relative humidity for a given temperature and absolute
        humidity.

        Parameters
        ----------
        T : Temperature
            Temperature
        ah : Density
            Absolute humidity

        Returns
        -------
        Dimensionless
            Relative humnidity

        '''
        return Dimensionless(0.1 * ah.asFloat('g/cm^3') * T.asFloat('K') * 461.52 /
                             Humidity.saturationVaporPressure(T).asFloat('hPa'))
    
    @staticmethod
    def dewPointFromAbsoluteHumidity(T: Temperature, ah: Density) -> Temperature:
        '''
        Returns the dew point for a given temperature and absolute humidity.

        Parameters
        ----------
        T : Temperature
            Temperature
        ah : Density
            Absolute humidity

        Returns
        -------
        Temperature
            Dew point

        '''
        return Humidity.dewPoint(T, Humidity.relativeHumidityFromAbsoluteHumidity(T, ah))
    
    @staticmethod
    def relativeHumidityFromDewPoint(T: Temperature, Td: Temperature) -> Dimensionless:
        '''
        Returns the realtive humidity for a given temperature and dew point.

        Parameters
        ----------
        T : Temperature
            Temperature
        Td : Temperature
            Dew point

        Returns
        -------
        Dimensionless
            Relative humidity

        '''
        pv = Humidity.saturationVaporPressure(T)
        pp = Humidity.saturationVaporPressure(Td)
        return pp/pv
    
    @staticmethod
    def absoluteHumidityFromDewPoint(T: Temperature, Td: Temperature) -> Density:
        '''
        Returns the absolute humidity for a given temperature and dew point.

        Parameters
        ----------
        T : Temperature
            Temperature
        Td : Temperature
            Dew point

        Returns
        -------
        Density
            Absolute humidity

        '''
        relh = Humidity.relativeHumidityFromDewPoint(T, Td);
        return Humidity.absoluteHumidity(T, relh)
