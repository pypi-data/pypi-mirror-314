#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Andreas Mussgiller
"""

import math
import numbers
from collections.abc import Iterable

class UnitException(Exception):
    def __init__(self, message):
        self.message = message
        
'''
###########################################################
# Unit
###########################################################
'''
class Unit():
    def __init__(self, value: float, unit: str):
        if isinstance(value, Iterable):
            raise UnitException(f"{self.__class__.__name__}: initialize from container")
        if unit not in self._conversions:
            raise UnitException(f"{self.__class__.__name__}: unknown unit '{unit}'")
        self._value = self._valueFromUnit(value, unit)[0]

    def basevalue(self) -> float:
        return self._valueForUnit(self._baseunit)[0]

    def value(self, unit: str = None) -> float:
        if unit == None:
            return self._valueForUnit(self._baseunit)[0]
        else:
            return self._valueForUnit(unit)[0]
    
    def valueWithUnit(self, unit: str = None) -> (float, str):
        if unit == None:
            return self._valueForUnit(self._preferredunit)
        else:
            return self._valueForUnit(unit)
    
    def asFloat(self, unit: str = None) -> float:
        return self.value(unit)
    
    def asString(self, unit: str = None) -> str:
        if unit == None:
            (v,u) = self._valueForUnit(self._preferredunit)
        else:
            (v,u) = self._valueForUnit(unit)
        return f"{v} {u}"
    
    def _valueForUnit(self, unit: str = None) -> (float, str):
        if unit not in self._conversions:
            return (self._value, self._baseunit)
        return (self._conversions[unit] * self._value, unit)
            
    def _valueFromUnit(self, value: float, unit: str = None) -> (float, str):
        if unit not in self._conversions:
            return (self._value, self._baseunit)
        return (value / self._conversions[unit], unit)

    def dimension(self) -> str:
        return self._dimension

    def baseUnit(self) -> str:
        return self._baseunit

    def preferredUnit(self) -> str:
        return self._preferredunit
    
    def knownunits(self) -> [str]:
        return list(self._conversions.values())
        
    def __str__(self):
        return self.asString()
    
    def __repr__(self):
        return self.asString()
    
    def __abs__(self):
        return abs(self._value)
    
    def __float__(self):
        return self._value
    
    def __eq__(self, other):
        if self.__class__ == other.__class__:
            return self._value.__eq__(other._value)
        raise TypeError
    
    def __lt__(self, other):
        if self.__class__ == other.__class__:
            return self._value.__lt__(other._value)
        raise TypeError
    
    def __le__(self, other):
        if self.__class__ == other.__class__:
            return self._value.__le__(other._value)
        raise TypeError
    
    def __hash__(self):
        return hash(self._value)

'''
###########################################################
# Dimensionless
###########################################################
'''
class Dimensionless(Unit):
    def __init__(self, value: float, unit: str = '1'):
        self._dimension = '1'
        self._baseunit = '1'
        self._preferredunit = unit
        self._conversions = {
            '1':  1.0,
            '%':  1.0e2,
            }
        super().__init__(value, unit)
    
    def __add__(self, value2):
        if isinstance(value2, numbers.Number):
            return Dimensionless(self._value + value2)
        if isinstance(value2, Dimensionless):
            return Dimensionless(self._value + value2._value)
        raise UnitException(f"{self.__class__.__name__}: add {value2.__class__.__name__}")
    
    def __radd__(self, value2):
        if not isinstance(value2, numbers.Number):
            raise UnitException(f"{self.__class__.__name__}: add to {value2.__class__.__name__}")
        return Dimensionless(self._value + value2)
    
    def __iadd__(self, value2):
        if isinstance(value2, numbers.Number):
            self._value += value2
            return self
        if isinstance(value2, Dimensionless):
            self._value += value2._value
            return self
        raise UnitException(f"{self.__class__.__name__}: add {value2.__class__.__name__}")
    
    def __sub__(self, value2):
        if isinstance(value2, numbers.Number):
            return Dimensionless(self._value - value2)
        if isinstance(value2, Dimensionless):
            return Dimensionless(self._value - value2._value)
        raise UnitException(f"{self.__class__.__name__}: subtract {value2.__class__.__name__}")
    
    def __rsub__(self, value2):
        if not isinstance(value2, numbers.Number):
            raise UnitException(f"{self.__class__.__name__}: subtract from {value2.__class__.__name__}")
        return Dimensionless(self._value - value2)
    
    def __isub__(self, value2):
        if isinstance(value2, numbers.Number):
            self._value -= value2
            return self
        if isinstance(value2, Dimensionless):
            self._value -= value2._value
            return self
        raise UnitException(f"{self.__class__.__name__}: subtract {value2.__class__.__name__}")
        
    def __mul__(self, value2):
        if isinstance(value2, numbers.Number):
            return Dimensionless(self._value * value2)
        if isinstance(value2, Dimensionless):
            return Dimensionless(self._value * value2._value)
        if isinstance(value2, Length):
            return Length(self._value * value2._value)
        if isinstance(value2, Area):
            return Area(self._value * value2._value)
        if isinstance(value2, Volume):
            return Volume(self._value * value2._value)
        if isinstance(value2, Density):
            return Density(self._value * value2._value)
        if isinstance(value2, ThermalConductivity):
            return ThermalConductivity(self._value * value2._value)
        raise UnitException(f"{self.__class__.__name__}: multiply {value2.__class__.__name__}")
        
    def __rmul__(self, value2):
        if isinstance(value2, numbers.Number):
            return Dimensionless(self._value * value2)
        if isinstance(value2, Dimensionless):
            return Dimensionless(self._value * value2._value)
        if isinstance(value2, Length):
            return Length(self._value * value2._value)
        if isinstance(value2, Area):
            return Area(self._value * value2._value)
        if isinstance(value2, Volume):
            return Volume(self._value * value2._value)
        raise UnitException(f"{self.__class__.__name__}: multiply {value2.__class__.__name__}")
    
    def __truediv__(self, value2):
        if isinstance(value2, numbers.Number):
            return Dimensionless(self._value / value2)
        if isinstance(value2, Dimensionless):
            return Dimensionless(self._value / value2._value)
        if isinstance(value2, ThermalConductivity):
            return ThermalResistance(self._value / value2._value)
        if isinstance(value2, ThermalResistance):
            return ThermalConductivity(self._value / value2._value)
        raise UnitException(f"{self.__class__.__name__}: divide {value2.__class__.__name__}")
    
    def __rtruediv__(self, value2):
        if isinstance(value2, numbers.Number):
            return Dimensionless(value2 / self._value)
        if isinstance(value2, Dimensionless):
            return Dimensionless(value2._value / self._value)
        raise UnitException(f"{self.__class__.__name__}: divide {value2.__class__.__name__}")
    
    def __pow__(self, value2):
        if isinstance(value2, numbers.Number):
            return Dimensionless(self._value.__pow__(value2))
        if isinstance(value2, Dimensionless):
            return Dimensionless(self._value.__pow__(value2._value))
        raise TypeError        
    
    def __eq__(self, other):
        if self.__class__ == other.__class__:
            return self._value.__eq__(other._value)
        if isinstance(other, numbers.Number):
            return self._value.__eq__(other)
        raise TypeError
    
    def __lt__(self, other):
        if self.__class__ == other.__class__:
            return self._value.__lt__(other._value)
        if isinstance(other, numbers.Number):
            return self._value.__lt__(other)
        raise TypeError
    
    def __le__(self, other):
        if self.__class__ == other.__class__:
            return self._value.__le__(other._value)
        if isinstance(other, numbers.Number):
            return self._value.__le__(other)
        raise TypeError

'''
###########################################################
# Angle
###########################################################
'''
class Angle(Unit):
    def __init__(self, value: float, unit: str = 'rad'):
        self._dimension = '1'
        self._baseunit = 'rad'
        self._preferredunit = unit
        self._conversions = {
            'rad': 1.0,
            'deg': 1.0,
            }
        super().__init__(value, unit)
        
    def _valueForUnit(self, unit: str = '') -> (float, str):
        if unit not in self._conversions:
            return (self._value, self._baseunit)
        if unit == 'rad': return (self._value, unit)
        if unit == 'deg': return (self._value * 180.0 / math.pi, unit)
        return (self._value, self._baseunit)
            
    def _valueFromUnit(self, value: float, unit: str = '') -> (float, str):
        if unit not in self._conversions:
            return (value, self._baseunit)
        if unit == 'rad': return (value, unit)
        if unit == 'deg': return (value * math.pi / 180.0, unit)
        return (value, self._baseunit)

    def __add__(self, value2):
        if not isinstance(value2, Mass):
            raise UnitException(f"{self.__class__.__name__}: add {value2.__class__.__name__}")
        return Angle(self._value + value2._value)
    
    def __sub__(self, value2):
        if not isinstance(value2, Mass):
            raise TypeError
        return Angle(self._value - value2._value)
    
    def __mul__(self, value2):
        if isinstance(value2, numbers.Number):
            return Angle(self._value * value2)
        if isinstance(value2, Dimensionless):
            return Angle(self._value * value2._value)
        raise TypeError
    
    def __truediv__(self, value2):
        if isinstance(value2, numbers.Number):
            return Angle(self._value / value2)
        if isinstance(value2, Dimensionless):
            return Angle(self._value / value2._value)
        raise TypeError

'''
###########################################################
# Mass
###########################################################
'''
class Mass(Unit):
    def __init__(self, value: float, unit: str = 'kg'):
        self._dimension = 'M'
        self._baseunit = 'kg'
        self._preferredunit = unit
        self._conversions = {
            't': 1.0e-3,
            'kg': 1.0,
            'g': 1.0e3,
            'mg': 1.0e6,
            'lb': 2.2046226218,
            'lbs': 2.2046226218,
            'pound': 2.2046226218,
            'oz': 35.27396195,
            'ounce': 35.27396195,
            }
        super().__init__(value, unit)
    
    def __add__(self, value2):
        if not isinstance(value2, Mass):
            raise UnitException(f"{self.__class__.__name__}: add {value2.__class__.__name__}")
        return Mass(self._value + value2._value)
    
    def __sub__(self, value2):
        if not isinstance(value2, Mass):
            raise TypeError
        return Mass(self._value - value2._value)
    
    def __mul__(self, value2):
        if isinstance(value2, numbers.Number):
            return Mass(self._value * value2)
        if isinstance(value2, Dimensionless):
            return Mass(self._value * value2._value)
        raise TypeError
    
    def __truediv__(self, value2):
        if isinstance(value2, numbers.Number):
            return Mass(self._value / value2)
        if isinstance(value2, Dimensionless):
            return Mass(self._value / value2._value)
        if isinstance(value2, Volume):
            return Density(self._value / value2._value)
        if isinstance(value2, Duration):
            return MassFlowRate(self._value / value2._value)
        if isinstance(value2, Mass):
            return Dimensionless(self._value / value2._value)
        raise TypeError

'''
###########################################################
# Force
###########################################################
'''
class Force(Unit):
    def __init__(self, value: float, unit: str = 'N'):
        self._dimension = 'M L T^-2'
        self._baseunit = 'N'
        self._preferredunit = unit
        self._conversions = {
            'kN':  1.0e-3,
            'N':  1.0,
            'mN':  1.0e3,
            'kgf':  0.1019716213,
            'kp':  0.1019716213,
            'lbf':  0.22480894387,
            }
        super().__init__(value, unit)
    
    def __add__(self, value2):
        if not isinstance(value2, Force):
            raise UnitException(f"{self.__class__.__name__}: add {value2.__class__.__name__}")
        return Force(self._value + value2._value)
    
    def __sub__(self, value2):
        if not isinstance(value2, Force):
            raise TypeError
        return Force(self._value - value2._value)
    
    def __mul__(self, value2):
        if isinstance(value2, numbers.Number):
            return Force(self._value * value2)
        if isinstance(value2, Dimensionless):
            return Force(self._value * value2._value)
        if isinstance(value2, Length):
            return Energy(self._value * value2._value)
        raise TypeError
    
    def __truediv__(self, value2):
        if isinstance(value2, numbers.Number):
            return Force(self._value / value2)
        if isinstance(value2, Dimensionless):
            return Force(self._value / value2._value)
        if isinstance(value2, Area):
            return Pressure(self._value / value2._value)
        if isinstance(value2, Force):
            return Dimensionless(self._value / value2._value)
        raise TypeError

'''
###########################################################
# Length
###########################################################
'''
class Length(Unit):
    def __init__(self, value: float, unit: str = 'm'):
        self._dimension = 'L'
        self._baseunit = 'm'
        self._preferredunit = unit
        self._conversions = {
            'km':      pow(1.0e-3, 1),
            'm':       pow(1.0, 1),
            'cm':      pow(1.0e2, 1),
            'mm':      pow(1.0e3, 1),
            'um':      pow(1.0e6, 1),
            'nm':      pow(1.0e9, 1),
            'ft':      pow(3.280839895, 1),
            'in':      pow(39.37007874, 1),
            'mil':     pow(39370.07874, 1),
            'mi':      pow(0.62137119224e-3, 1),
            'yd':      pow(1.0936132983, 1),
            }
        super().__init__(value, unit)
    
    def __add__(self, value2):
        if not isinstance(value2, Length):
            raise UnitException(f"{self.__class__.__name__}: add {value2.__class__.__name__}")
        return Length(self._value + value2._value)
    
    def __sub__(self, value2):
        if not isinstance(value2, Length):
            raise TypeError
        return Length(self._value - value2._value)
    
    def __mul__(self, value2):
        if isinstance(value2, numbers.Number):
            return Length(self._value * value2)
        if isinstance(value2, Dimensionless):
            return Length(self._value * value2._value)
        if isinstance(value2, InverseLength):
            return Dimensionless(self._value * value2._value)
        if isinstance(value2, Length):
            return Area(self._value * value2._value)
        if isinstance(value2, Area):
            return Volume(self._value * value2._value)
        if isinstance(value2, Force):
            return Energy(self._value * value2._value)
        if isinstance(value2, TemperatureGradient):
            return TemperatureDifference(self._value * value2._value)
        if isinstance(value2, ThermalConductivity):
            return AbsoluteThermalConductance(self._value * value2._value)
        if isinstance(value2, ThermalConductance):
            return ThermalConductivity(self._value * value2._value)
        raise TypeError
    
    def __truediv__(self, value2):
        if isinstance(value2, numbers.Number):
            return Length(self._value / value2)
        if isinstance(value2, Dimensionless):
            return Length(self._value / value2._value)
        if isinstance(value2, Duration):
            return Velocity(self._value / value2._value)
        if isinstance(value2, Length):
            return Dimensionless(self._value / value2._value)
        if isinstance(value2, ThermalResistance):
            return ThermalConductivity(self._value / value2._value)
        if isinstance(value2, ThermalConductivity):
            return ThermalResistance(self._value / value2._value)
        if isinstance(value2, TemperatureDifference):
            return InverseTemperatureGradient(self._value / value2._value)
        raise TypeError
        
    def __rtruediv__(self, value2):
        if isinstance(value2, numbers.Number):
            #if value2!=1.0: raise ValueError
            return InverseLength(value2 / self._value)
        if isinstance(value2, Dimensionless):
            #if value2._value!=1.0: raise ValueError
            return InverseLength(value2._value / self._value)
        raise TypeError

'''
###########################################################
# InverseLength
###########################################################
'''
class InverseLength(Unit):
    def __init__(self, value: float, unit: str = 'm^-1'):
        self._dimension = 'L^-1'
        self._baseunit = 'm^-1'
        self._preferredunit = unit
        self._conversions = {
            'km^-1':  1.0e-3,
            'm^-1':  1.0,
            'cm^-1':  1.0e2,
            'mm^-1':  1.0e3,
            'um^-1':  1.0e6,
            'nm^-1':  1.0e9,
            'ft^-1':  3.280839895,
            'in^-1':  39.37007874,
            'mil^-1':  39370.07874,
            'mi^-1':  0.62137119224e-3,
            'yd^-1':  1.0936132983,
            }
        super().__init__(value, unit)
    
    def __add__(self, value2):
        if not isinstance(value2, InverseLength):
            raise UnitException(f"{self.__class__.__name__}: add {value2.__class__.__name__}")
        return InverseLength(self._value + value2._value)
    
    def __sub__(self, value2):
        if not isinstance(value2, InverseLength):
            raise TypeError
        return InverseLength(self._value - value2._value)
    
    def __mul__(self, value2):
        if isinstance(value2, numbers.Number):
            return InverseLength(self._value * value2)
        if isinstance(value2, Dimensionless):
            return InverseLength(self._value * value2._value)
        if isinstance(value2, Length):
            return Dimensionless(self._value * value2._value)
        raise TypeError
    
    def __truediv__(self, value2):
        if isinstance(value2, numbers.Number):
            return InverseLength(self._value / value2)
        if isinstance(value2, Dimensionless):
            return InverseLength(self._value / value2._value)
        if isinstance(value2, InverseLength):
            return Dimensionless(self._value / value2._value)
        raise TypeError
        
    def __rtruediv__(self, value2):
        if isinstance(value2, numbers.Number):
            #if value2!=1.0: raise ValueError
            return Length(value2 / self._value)
        if isinstance(value2, Dimensionless):
            #if value2._value!=1.0: raise ValueError
            return Length(value2._value / self._value)
        raise TypeError

'''
###########################################################
# Area
###########################################################
'''
class Area(Unit):
    def __init__(self, value: float, unit: str = 'm^2'):
        self._dimension = 'L^2'
        self._baseunit = 'm^2'
        self._preferredunit = unit
        self._conversions = {
            'km^2':      pow(1.0e-3, 2),
            'm^2':       pow(1.0, 2),
            'cm^2':      pow(1.0e2, 2),
            'mm^2':      pow(1.0e3, 2),
            'um^2':      pow(1.0e6, 2),
            'nm^2':      pow(1.0e9, 2),
            'ft^2':      pow(3.280839895, 2),
            'in^2':     pow(39.37007874, 2),
            'mil^2': pow(39370.07874, 2),
            'mi^2':      pow(0.62137119224e-3, 2),
            'yd^2':      pow(1.0936132983, 2),
             }
        super().__init__(value, unit)
    
    def __add__(self, value2):
        if not isinstance(value2, Area):
            raise UnitException(f"{self.__class__.__name__}: add {value2.__class__.__name__}")
        return Area(self._value + value2._value)
    
    def __sub__(self, value2):
        if not isinstance(value2, Area):
            raise TypeError
        return Area(self._value - value2._value)
    
    def __mul__(self, value2):
        if isinstance(value2, numbers.Number):
            return Area(self._value * value2)
        if isinstance(value2, Dimensionless):
            return Area(self._value * value2._value)
        if isinstance(value2, Length):
            return Volume(self._value * value2._value)
        if isinstance(value2, Pressure):
            return Force(self._value * value2._value)
        if isinstance(value2, HeatFlux):
            return Power(self._value * value2._value)
        if isinstance(value2, ThermalConductance):
            return AbsoluteThermalConductance(self._value * value2._value)
        raise TypeError
    
    def __truediv__(self, value2):
        if isinstance(value2, numbers.Number):
            return Area(self._value / value2)
        if isinstance(value2, Dimensionless):
            return Area(self._value / value2._value)
        if isinstance(value2, Length):
            return Length(self._value / value2._value)
        if isinstance(value2, Area):
            return Dimensionless(self._value / value2._value)
        raise TypeError

'''
###########################################################
# Volume
###########################################################
'''
class Volume(Unit):
    def __init__(self, value: float, unit: str = 'm^3'):
        self._dimension = 'L^3'
        self._baseunit = 'm^3'
        self._preferredunit = unit
        self._conversions = {
            'km^3':      pow(1.0e-3, 3),
            'm^3':       pow(1.0, 3),
            'cm^3':      pow(1.0e2, 3),
            'mm^3':      pow(1.0e3, 3),
            'um^3':      pow(1.0e6, 3),
            'nm^3':      pow(1.0e9, 3),
            'ft^3':      pow(3.280839895, 3),
            'in^3':     pow(39.37007874, 3),
            'mil^3': pow(39370.07874, 3),
            'mi^3':      pow(0.62137119224e-3, 3),
            'yd^3':      pow(1.0936132983, 3),
            }
        super().__init__(value, unit)
    
    def __add__(self, value2):
        if not isinstance(value2, Volume):
            raise UnitException(f"{self.__class__.__name__}: add {value2.__class__.__name__}")
        return Volume(self._value + value2._value)
    
    def __sub__(self, value2):
        if not isinstance(value2, Volume):
            raise TypeError
        return Volume(self._value - value2._value)
    
    def __mul__(self, value2):
        if isinstance(value2, numbers.Number):
            return Volume(self._value * value2)
        if isinstance(value2, Dimensionless):
            return Volume(self._value * value2._value)
        if isinstance(value2, Density):
            return Mass(self._value * value2._value)
        raise TypeError
    
    def __truediv__(self, value2):
        if isinstance(value2, numbers.Number):
            return Volume(self._value / value2)
        if isinstance(value2, Dimensionless):
            return Volume(self._value / value2._value)
        if isinstance(value2, Length):
            return Area(self._value / value2._value)
        if isinstance(value2, Area):
            return Length(self._value / value2._value)
        if isinstance(value2, Duration):
            return VolumeFlowRate(self._value / value2._value)
        if isinstance(value2, Volume):
            return Dimensionless(self._value / value2._value)
        raise TypeError

'''
###########################################################
# Density
###########################################################
'''
class Density(Unit):
    def __init__(self, value: float, unit: str = 'kg/m^3'):
        self._dimension = 'M L^-3'
        self._baseunit = 'kg/m^3'
        self._preferredunit = unit
        self._conversions = {
            'g/m^3':  1.0e3,
            'kg/m^3':  1.0,
            'g/cm^3':  1.0e-3,
            'g/ml':  1.0e-3,
            'lb/ft^3':  62427.960841e-6,
            'lbs/ft^3':  62427.960841e-6,
            }
        super().__init__(value, unit)
    
    def __add__(self, value2):
        if not isinstance(value2, Density):
            raise UnitException(f"{self.__class__.__name__}: add {value2.__class__.__name__}")
        return Density(self._value + value2._value)
    
    def __sub__(self, value2):
        if not isinstance(value2, Density):
            raise TypeError
        return Density(self._value - value2._value)
    
    def __mul__(self, value2):
        if isinstance(value2, numbers.Number):
            return Density(self._value * value2)
        if isinstance(value2, Dimensionless):
            return Density(self._value * value2._value)
        if isinstance(value2, Volume):
            return Mass(self._value * value2._value)
        if isinstance(value2, KinematicViscosity):
            return DynamicViscosity(self._value * value2._value)
        raise TypeError
    
    def __truediv__(self, value2):
        if isinstance(value2, numbers.Number):
            return Density(self._value / value2)
        if isinstance(value2, Dimensionless):
            return Density(self._value / value2._value)
        if isinstance(value2, Density):
            return Dimensionless(self._value / value2._value)
        raise TypeError

'''
###########################################################
# Pressure
###########################################################
'''
class Pressure(Unit):
    def __init__(self, value: float, unit: str = 'Pa'):
        self._dimension = 'M L^-1 T^-2'
        self._baseunit = 'Pa'
        self._preferredunit = unit
        self._conversions = {
            'GPa':  1.0e-9,
            'MPa':  1.0e-6,
            'kPa':  1.0e-3,
            'hPa':  1.0e-2,
            'Pa':  1.0,
            'mPa':  1.0e+3,
            'N/m^2':  1.0,
            'N/cm^2':  1.0e+2 * 1.0e+2,
            'bar':  1.0e-5,
            'mbar':  1.0e-3,
            'psi':  145.03773801e-6,
            'psf':  20.885434273e-3,
            'torr':  7.5006167382e-3,
            }
        super().__init__(value, unit)
    
    def __add__(self, value2):
        if not isinstance(value2, Pressure):
            raise UnitException(f"{self.__class__.__name__}: add {value2.__class__.__name__}")
        return Pressure(self._value + value2._value)
    
    def __sub__(self, value2):
        if not isinstance(value2, Pressure):
            raise TypeError
        return Pressure(self._value - value2._value)
    
    def __mul__(self, value2):
        if isinstance(value2, numbers.Number):
            return Pressure(self._value * value2)
        if isinstance(value2, Dimensionless):
            return Pressure(self._value * value2._value)
        if isinstance(value2, Area):
            return Force(self._value * value2._value)
        raise TypeError
    
    def __truediv__(self, value2):
        if isinstance(value2, numbers.Number):
            return Pressure(self._value / value2)
        if isinstance(value2, Dimensionless):
            return Pressure(self._value / value2._value)
        if isinstance(value2, Pressure):
            return Dimensionless(self._value / value2._value)
        raise TypeError

'''
###########################################################
# Duration
###########################################################
'''
class Duration(Unit):
    def __init__(self, value: float, unit: str = 's'):
        self._dimension = 'T'
        self._baseunit = 's'
        self._preferredunit = unit
        self._conversions = {
            'w':  1.0/(7.*24.*60.*60.),
            'd':  1.0/(24.*60.*60.),
            'h':  1.0/(60.*60.),
            'min':  1.0/60.,
            's':  1.0,
            'ms':  1.0e3,
            'us':  1.0e6,
            'ns':  1.0e9,
            }
        super().__init__(value, unit)
    
    def __add__(self, value2):
        if not isinstance(value2, Duration):
            raise UnitException(f"{self.__class__.__name__}: add {value2.__class__.__name__}")
        return Duration(self._value + value2._value)
    
    def __sub__(self, value2):
        if not isinstance(value2, Duration):
            raise TypeError
        return Duration(self._value - value2._value)
    
    def __mul__(self, value2):
        if isinstance(value2, numbers.Number):
            return Duration(self._value * value2)
        if isinstance(value2, Dimensionless):
            return Duration(self._value * value2._value)
        if isinstance(value2, VolumeFlowRate):
            return Volume(self._value * value2._value)
        if isinstance(value2, MassFlowRate):
            return Mass(self._value * value2._value)
        if isinstance(value2, Velocity):
            return Length(self._value * value2._value)
        if isinstance(value2, Power):
            return Energy(self._value * value2._value)
        raise TypeError
    
    def __truediv__(self, value2):
        if isinstance(value2, numbers.Number):
            return Duration(self._value / value2)
        if isinstance(value2, Dimensionless):
            return Duration(self._value / value2._value)
        if isinstance(value2, Duration):
            return Dimensionless(self._value / value2._value)
        raise TypeError

'''
###########################################################
# VolumeFlowRate
###########################################################
'''
class VolumeFlowRate(Unit):
    def __init__(self, value: float, unit: str = 'm^3/s'):
        self._dimension = 'L^3 T^-1'
        self._baseunit = 'm^3/s'
        self._preferredunit = unit
        self._conversions = {
            'm^3/s':  1.0,
            'l/s':  1.0e3,
            'cm^3/s':  1.0e6,
            'm^3/min':  60.*1.0,
            'l/min':  60.*1.0e3,
            'cm^3/min':  60.*1.0e6,
            'm^3/h':  3600.*1.0,
            'l/h':  3600.*1.0e3,
            'cm^3/h':  3600.*1.0e6,
            }
        super().__init__(value, unit)
    
    def __add__(self, value2):
        if not isinstance(value2, VolumeFlowRate):
            raise UnitException(f"{self.__class__.__name__}: add {value2.__class__.__name__}")
        return VolumeFlowRate(self._value + value2._value)
    
    def __sub__(self, value2):
        if not isinstance(value2, VolumeFlowRate):
            raise TypeError
        return VolumeFlowRate(self._value - value2._value)
    
    def __mul__(self, value2):
        if isinstance(value2, numbers.Number):
            return VolumeFlowRate(self._value * value2)
        if isinstance(value2, Dimensionless):
            return VolumeFlowRate(self._value * value2._value)
        if isinstance(value2, Duration):
            return Volume(self._value * value2._value)
        raise TypeError
    
    def __truediv__(self, value2):
        if isinstance(value2, numbers.Number):
            return VolumeFlowRate(self._value / value2)
        if isinstance(value2, Dimensionless):
            return VolumeFlowRate(self._value / value2._value)
        if isinstance(value2, VolumeFlowRate):
            return Dimensionless(self._value / value2._value)
        raise TypeError

'''
###########################################################
# MassFlowRate
###########################################################
'''
class MassFlowRate(Unit):
    def __init__(self, value: float, unit: str = 'kg/s'):
        self._dimension = 'M T^-1'
        self._baseunit = 'kg/s'
        self._preferredunit = unit
        self._conversions = {
            'kg/s':  1.0,
            'g/s':  1.0e3,
            'kg/min':  60.*1.0,
            'g/min':  60.*1.0e3,
            'kg/h':  3600.*1.0,
            'g/h':  3600.*1.0e3,
            }
        super().__init__(value, unit)
    
    def __add__(self, value2):
        if not isinstance(value2, MassFlowRate):
            raise UnitException(f"{self.__class__.__name__}: add {value2.__class__.__name__}")
        return MassFlowRate(self._value + value2._value)
    
    def __sub__(self, value2):
        if not isinstance(value2, MassFlowRate):
            raise TypeError
        return MassFlowRate(self._value - value2._value)
    
    def __mul__(self, value2):
        if isinstance(value2, numbers.Number):
            return MassFlowRate(self._value * value2)
        if isinstance(value2, Dimensionless):
            return MassFlowRate(self._value * value2._value)
        if isinstance(value2, Duration):
            return Mass(self._value * value2._value)
        raise TypeError
    
    def __truediv__(self, value2):
        if isinstance(value2, numbers.Number):
            return MassFlowRate(self._value / value2)
        if isinstance(value2, Dimensionless):
            return MassFlowRate(self._value / value2._value)
        if isinstance(value2, MassFlowRate):
            return Dimensionless(self._value / value2._value)
        raise TypeError

'''
###########################################################
# Velocity
###########################################################
'''
class Velocity(Unit):
    def __init__(self, value: float, unit: str = 'm/s'):
        self._dimension = 'L T^-1'
        self._baseunit = 'm/s'
        self._preferredunit = unit
        self._conversions = {
            'km/h':  3600./1000.,
            'm/s':  1.0,
            'cm/s':  1.0e2,
            'mm/s':  1.0e3,
            'mph':  2.2369362921,
            'mi/h':  2.2369362921,
            'in/s':  39.37007874,
            }
        super().__init__(value, unit)
    
    def __add__(self, value2):
        if not isinstance(value2, Velocity):
            raise UnitException(f"{self.__class__.__name__}: add {value2.__class__.__name__}")
        return Velocity(self._value + value2._value)
    
    def __sub__(self, value2):
        if not isinstance(value2, Velocity):
            raise TypeError
        return Velocity(self._value - value2._value)
    
    def __mul__(self, value2):
        if isinstance(value2, numbers.Number):
            return Velocity(self._value * value2)
        if isinstance(value2, Dimensionless):
            return Velocity(self._value * value2._value)
        if isinstance(value2, Duration):
            return Length(self._value * value2._value)
        raise TypeError
    
    def __truediv__(self, value2):
        if isinstance(value2, numbers.Number):
            return Velocity(self._value / value2)
        if isinstance(value2, Dimensionless):
            return Velocity(self._value / value2._value)
        if isinstance(value2, Velocity):
            return Dimensionless(self._value / value2._value)
        raise TypeError

'''
###########################################################
# Energy
###########################################################
'''
class Energy(Unit):
    def __init__(self, value: float, unit: str = 'J'):
        self._dimension = 'M L^2 T^-2'
        self._baseunit = 'J'
        self._preferredunit = unit
        self._conversions = {
            'MJ':  1.0e6,
            'kJ':  1.0e3,
            'J':  1.0,
            'mJ':  1.0e-3,
            'J':  1.0,
            'Nm':  1.0,
            'Ws':  1.0,
            'Wh':  1.0*3600.,
            'kWh':  1.0e3*3600.,
            'MWh':  1.0e6*3600.,
            'GWh':  1.0e9*3600.,
            'Btu':  1055.,
            }
        super().__init__(value, unit)
    
    def __add__(self, value2):
        if not isinstance(value2, Energy):
            raise UnitException(f"{self.__class__.__name__}: add {value2.__class__.__name__}")
        return Energy(self._value + value2._value)
    
    def __sub__(self, value2):
        if not isinstance(value2, Energy):
            raise TypeError
        return Energy(self._value - value2._value)
    
    def __mul__(self, value2):
        if isinstance(value2, numbers.Number):
            return Energy(self._value * value2)
        if isinstance(value2, Dimensionless):
            return Energy(self._value * value2._value)
        raise TypeError
    
    def __truediv__(self, value2):
        if isinstance(value2, numbers.Number):
            return Energy(self._value / value2)
        if isinstance(value2, Dimensionless):
            return Energy(self._value / value2._value)
        if isinstance(value2, Energy):
            return Dimensionless(self._value / value2._value)
        if isinstance(value2, Length):
            return Force(self._value / value2._value)
        if isinstance(value2, Duration):
            return Power(self._value / value2._value)
        raise TypeError

'''
###########################################################
# Power
###########################################################
'''
class Power(Unit):
    def __init__(self, value: float, unit: str = 'W'):
        self._dimension = 'M L^2 T^-3'
        self._baseunit = 'W'
        self._preferredunit = unit
        self._conversions = {
            'GW':  1.0e-9,
            'MW':  1.0e-6,
            'kW':  1.0e-3,
            'W':  1.0,
            'mW':  1.0e3,
            'Btu/h':  3.4121416351,
            'Btu/min':  56.869027252e-3,
            'Btu/s':  947.81712087e-6,
            }
        super().__init__(value, unit)
    
    def __add__(self, value2):
        if not isinstance(value2, Power):
            raise UnitException(f"{self.__class__.__name__}: add {value2.__class__.__name__}")
        return Power(self._value + value2._value)
    
    def __sub__(self, value2):
        if not isinstance(value2, Power):
            raise TypeError
        return Power(self._value - value2._value)
    
    def __mul__(self, value2):
        if isinstance(value2, numbers.Number):
            return Power(self._value * value2)
        if isinstance(value2, Dimensionless):
            return Power(self._value * value2._value)
        if isinstance(value2, Duration):
            return Energy(self._value * value2._value)
        raise TypeError
    
    def __truediv__(self, value2):
        if isinstance(value2, numbers.Number):
            return Power(self._value / value2)
        if isinstance(value2, Dimensionless):
            return Power(self._value / value2._value)
        if isinstance(value2, Power):
            return Dimensionless(self._value / value2._value)
        if isinstance(value2, Area):
            return HeatFlux(self._value / value2._value)
        if isinstance(value2, TemperatureDifference):
            return AbsoluteThermalConductance(self._value / value2._value)
        raise TypeError

'''
###########################################################
# HeatFlux
###########################################################
'''
class HeatFlux(Unit):
    def __init__(self, value: float, unit: str = 'W/m^2'):
        self._dimension = 'M T^-3'
        self._baseunit = 'W/m^2'
        self._preferredunit = unit
        self._conversions = {
            'kW/m^2':  1.0e3,
            'W/m^2':  1.0,
            'W/cm^2':  1.0e-2 * 1.0e-2,
            'W/mm^2':  1.0e-3 * 1.0e-3,
            }
        super().__init__(value, unit)
    
    def __add__(self, value2):
        if not isinstance(value2, HeatFlux):
            raise UnitException(f"{self.__class__.__name__}: add {value2.__class__.__name__}")
        return HeatFlux(self._value + value2._value)
    
    def __sub__(self, value2):
        if not isinstance(value2, HeatFlux):
            raise TypeError
        return HeatFlux(self._value - value2._value)
    
    def __mul__(self, value2):
        if isinstance(value2, numbers.Number):
            return HeatFlux(self._value * value2)
        if isinstance(value2, Dimensionless):
            return HeatFlux(self._value * value2._value)
        if isinstance(value2, Area):
            return Power(self._value * value2._value)
        raise TypeError
    
    def __truediv__(self, value2):
        if isinstance(value2, numbers.Number):
            return HeatFlux(self._value / value2)
        if isinstance(value2, Dimensionless):
            return HeatFlux(self._value / value2._value)
        if isinstance(value2, HeatFlux):
            return Dimensionless(self._value / value2._value)
        if isinstance(value2, TemperatureGradient):
            return ThermalConductivity(self._value / value2._value)
        raise TypeError

'''
###########################################################
# Voltage
###########################################################
'''
class Voltage(Unit):
    def __init__(self, value: float, unit: str = 'V'):
        self._dimension = 'M L^2 I^-1 T^-3'
        self._baseunit = 'V'
        self._preferredunit = unit
        self._conversions = {
            'mV':  1.0e3,
            'V':  1.0,
            'kV':  1.0e-3,
            'MV':  1.0e-6,
            }
        super().__init__(value, unit)
    
    def __add__(self, value2):
        if not isinstance(value2, Voltage):
            raise UnitException(f"{self.__class__.__name__}: add {value2.__class__.__name__}")
        return Voltage(self._value + value2._value)
    
    def __sub__(self, value2):
        if not isinstance(value2, Voltage):
            raise TypeError
        return Voltage(self._value - value2._value)
    
    def __mul__(self, value2):
        if isinstance(value2, numbers.Number):
            return Voltage(self._value * value2)
        if isinstance(value2, Dimensionless):
            return Voltage(self._value * value2._value)
        if isinstance(value2, Current):
            return Power(self._value * value2._value)
        raise TypeError
    
    def __truediv__(self, value2):
        if isinstance(value2, numbers.Number):
            return Voltage(self._value / value2)
        if isinstance(value2, Dimensionless):
            return Voltage(self._value / value2._value)
        if isinstance(value2, Voltage):
            return Dimensionless(self._value / value2._value)
        if isinstance(value2, Current):
            return Resistance(self._value / value2._value)
        if isinstance(value2, Resistance):
            return Current(self._value / value2._value)
        raise TypeError

'''
###########################################################
# Current
###########################################################
'''
class Current(Unit):
    def __init__(self, value: float, unit: str = 'A'):
        self._dimension = 'I'
        self._baseunit = 'A'
        self._preferredunit = unit
        self._conversions = {
            'nA': 1.0e9,
            'uA': 1.0e6,
            'mA': 1.0e3,
            'A':  1.0,
            'kA': 1.0e-3,
            }
        super().__init__(value, unit)
    
    def __add__(self, value2):
        if not isinstance(value2, Current):
            raise UnitException(f"{self.__class__.__name__}: add {value2.__class__.__name__}")
        return Current(self._value + value2._value)
    
    def __sub__(self, value2):
        if not isinstance(value2, Current):
            raise TypeError
        return Current(self._value - value2._value)
    
    def __mul__(self, value2):
        if isinstance(value2, numbers.Number):
            return Current(self._value * value2)
        if isinstance(value2, Dimensionless):
            return Current(self._value * value2._value)
        if isinstance(value2, Voltage):
            return Power(self._value * value2._value)
        if isinstance(value2, Resistance):
            return Voltage(self._value * value2._value)
        raise TypeError
    
    def __truediv__(self, value2):
        if isinstance(value2, numbers.Number):
            return Current(self._value / value2)
        if isinstance(value2, Dimensionless):
            return Current(self._value / value2._value)
        if isinstance(value2, Current):
            return Dimensionless(self._value / value2._value)
        raise TypeError

'''
###########################################################
# Resistance
###########################################################
'''
class Resistance(Unit):
    def __init__(self, value: float, unit: str = 'Ohm'):
        self._dimension = 'M L^2 I^−2 T^−3'
        self._baseunit = 'Ohm'
        self._preferredunit = unit
        self._conversions = {
            'mOhm':  1.0e3,
            'Ohm':  1.0,
            'kOhm':  1.0e-3,
            'MOhm':  1.0e-6,
            }
        super().__init__(value, unit)
    
    def __add__(self, value2):
        if not isinstance(value2, Resistance):
            raise UnitException(f"{self.__class__.__name__}: add {value2.__class__.__name__}")
        return Resistance(self._value + value2._value)
    
    def __sub__(self, value2):
        if not isinstance(value2, Resistance):
            raise TypeError
        return Resistance(self._value - value2._value)
    
    def __mul__(self, value2):
        if isinstance(value2, numbers.Number):
            return Resistance(self._value * value2)
        if isinstance(value2, Dimensionless):
            return Resistance(self._value * value2._value)
        if isinstance(value2, Current):
            return Voltage(self._value * value2._value)
        raise TypeError
    
    def __truediv__(self, value2):
        if isinstance(value2, numbers.Number):
            return Resistance(self._value / value2)
        if isinstance(value2, Dimensionless):
            return Resistance(self._value / value2._value)
        if isinstance(value2, Resistance):
            return Dimensionless(self._value / value2._value)
        raise TypeError

'''
###########################################################
# SpecificHeat
###########################################################
'''
class SpecificHeat(Unit):
    def __init__(self, value: float, unit: str = 'J/(kg*K)'):
        self._dimension = 'L^2 T^-2 θ^-1'
        self._baseunit = 'J/(kg*K)'
        self._preferredunit = unit
        self._conversions = {
            'J/(kg*K)':  1.0,
            }
        super().__init__(value, unit)
    
    def __add__(self, value2):
        if not isinstance(value2, SpecificHeat):
            raise UnitException(f"{self.__class__.__name__}: add {value2.__class__.__name__}")
        return SpecificHeat(self._value + value2._value)
    
    def __sub__(self, value2):
        if not isinstance(value2, SpecificHeat):
            raise TypeError
        return SpecificHeat(self._value - value2._value)
    
    def __mul__(self, value2):
        if isinstance(value2, numbers.Number):
            return SpecificHeat(self._value * value2)
        if isinstance(value2, Dimensionless):
            return SpecificHeat(self._value * value2._value)
        raise TypeError
    
    def __truediv__(self, value2):
        if isinstance(value2, numbers.Number):
            return SpecificHeat(self._value / value2)
        if isinstance(value2, Dimensionless):
            return SpecificHeat(self._value / value2._value)
        if isinstance(value2, SpecificHeat):
            return Dimensionless(self._value / value2._value)
        raise TypeError

'''
###########################################################
# Temperature
###########################################################
'''
class Temperature(Unit):
    def __init__(self, value: float, unit: str = 'K'):
        self._dimension = 'θ'
        self._baseunit = 'K'
        self._preferredunit = unit
        self._conversions = {
            'K':  1.0,
            '°C':  1.0,
            'C':  1.0,
            '°F':  1.0,
            'F':  1.0,
            }
        super().__init__(value, unit)
    
    def _valueForUnit(self, unit: str = '') -> (float, str):
        if unit not in self._conversions:
            return (self._value, self._baseunit)
        if unit == 'K': return (self._value, unit)
        if unit == '°C': return (self._value - 273.15, unit)
        if unit == 'C': return (self._value - 273.15, unit)
        if unit == '°F': return (self._ * 1.8 - 459.67, unit)
        if unit == 'F': return (self._ * 1.8 - 459.67, unit)        
        return (self._value, self._baseunit)
            
    def _valueFromUnit(self, value: float, unit: str = '') -> (float, str):
        if unit not in self._conversions:
            return (value, self._baseunit)
        if unit == 'K': return (value, unit)
        if unit == '°C': return (value + 273.15, unit)
        if unit == 'C': return (value + 273.15, unit)
        if unit == '°F': return ((value + 459.69)/1.8, unit)
        if unit == 'F': return ((value + 459.69)/1.8, unit)        
        return (value, self._baseunit)
    
    def __add__(self, value2):
        if not isinstance(value2, TemperatureDifference):
            raise UnitException(f"{self.__class__.__name__}: add {value2.__class__.__name__}")
        return Temperature(self._value + value2._value)
    
    def __sub__(self, value2):
        if not isinstance(value2, Temperature):
            raise TypeError
        return TemperatureDifference(self._value - value2._value)
    
    def __mul__(self, value2):
        if isinstance(value2, numbers.Number):
            return Temperature(self._value * value2)
        if isinstance(value2, Dimensionless):
            return Temperature(self._value * value2._value)
        raise TypeError
    
    def __truediv__(self, value2):
        if isinstance(value2, numbers.Number):
            return Temperature(self._value / value2)
        if isinstance(value2, Dimensionless):
            return Temperature(self._value / value2._value)
        if isinstance(value2, Temperature):
            return Dimensionless(self._value / value2._value)
        raise TypeError

'''
###########################################################
# TemperatureDifference
###########################################################
'''
class TemperatureDifference(Unit):
    def __init__(self, value: float, unit: str = 'K'):
        self._dimension = 'θ'
        self._baseunit = 'K'
        self._preferredunit = unit
        self._conversions = {
            'K':  1.0,
            'mK':  1.0e-3,
            '°C':  1.0,
            'C':  1.0,
            '°F':  1.8,
            'F':  1.8,
            }
        super().__init__(value, unit)
    
    def __add__(self, value2):
        if isinstance(value2, TemperatureDifference):
            return TemperatureDifference(self._value + value2._value)
        if isinstance(value2, Temperature):
            return Temperature(self._value + value2._value)
        raise UnitException(f"{self.__class__.__name__}: add {value2.__class__.__name__}")
    
    def __sub__(self, value2):
        if not isinstance(value2, TemperatureDifference):
            raise TypeError
        return TemperatureDifference(self._value - value2._value)
    
    def __mul__(self, value2):
        if isinstance(value2, numbers.Number):
            return TemperatureDifference(self._value * value2)
        if isinstance(value2, Dimensionless):
            return TemperatureDifference(self._value * value2._value)
        raise TypeError
    
    def __truediv__(self, value2):
        if isinstance(value2, numbers.Number):
            return TemperatureDifference(self._value / value2)
        if isinstance(value2, Dimensionless):
            return TemperatureDifference(self._value / value2._value)
        if isinstance(value2, TemperatureDifference):
            return Dimensionless(self._value / value2._value)
        if isinstance(value2, Length):
            return TemperatureGradient(self._value / value2._value)
        if isinstance(value2, Power):
            return AbsoluteThermalResistance(self._value / value2._value)
        raise TypeError

'''
###########################################################
# TemperatureGradient
###########################################################
'''
class TemperatureGradient(Unit):
    def __init__(self, value: float, unit: str = 'K/m'):
        self._dimension = 'θ L^-1'
        self._baseunit = 'K/m'
        self._preferredunit = unit
        self._conversions = {
            'K/m':  1.0,
            'K/cm':  1.0e-2,
            'K/mm':  1.0e-3,
            '°C/m':  1.0,
            '°C/cm':  1.0e-2,
            '°C/mm':  1.0e-3,
            'C/m':  1.0,
            'C/cm':  1.0e-2,
            'C/mm':  1.0e-3,
            '°F/m':  1.8,
            '°F/cm':  1.8e-2,
            '°F/mm':  1.8e-3,
            'F/m':  1.8,
            'F/cm':  1.8e-2,
            'F/mm':  1.8e-3,
            }
        super().__init__(value, unit)
    
    def __add__(self, value2):
        if not isinstance(value2, TemperatureGradient):
            raise UnitException(f"{self.__class__.__name__}: add {value2.__class__.__name__}")
        return TemperatureGradient(self._value + value2._value)
    
    def __sub__(self, value2):
        if not isinstance(value2, TemperatureGradient):
            raise TypeError
        return TemperatureGradient(self._value - value2._value)
    
    def __mul__(self, value2):
        if isinstance(value2, numbers.Number):
            return TemperatureGradient(self._value * value2)
        if isinstance(value2, Dimensionless):
            return TemperatureGradient(self._value * value2._value)
        if isinstance(value2, Length):
            return TemperatureDifference(self._value * value2._value)
        raise TypeError
    
    def __truediv__(self, value2):
        if isinstance(value2, numbers.Number):
            return TemperatureGradient(self._value / value2)
        if isinstance(value2, Dimensionless):
            return TemperatureGradient(self._value / value2._value)
        if isinstance(value2, TemperatureGradient):
            return Dimensionless(self._value / value2._value)
        if isinstance(value2, HeatFlux):
            return ThermalResistivity(self._value / value2._value)
        raise TypeError
        
    def __rtruediv__(self, value2):
        if isinstance(value2, numbers.Number):
            #if value2!=1.0: raise ValueError
            return InverseTemperatureGradient(value2 / self._value)
        if isinstance(value2, Dimensionless):
            #if value2._value!=1.0: raise ValueError
            return InverseTemperatureGradient(value2._value / self._value)
        raise TypeError

'''
###########################################################
# InverseTemperatureGradient
###########################################################
'''
class InverseTemperatureGradient(Unit):
    def __init__(self, value: float, unit: str = 'm/K'):
        self._dimension = 'L θ^-1'
        self._baseunit = 'm/K'
        self._preferredunit = unit
        self._conversions = {
            'm/K':  1.0,
            'cm/K':  1.0/1.0e-2,
            'mm/K':  1.0/1.0e-3,
            'm/°C':  1.0,
            'cm/°C':  1.0/1.0e-2,
            'mm/°C':  1.0/1.0e-3,
            'm/C':  1.0,
            'cm/C':  1.0/1.0e-2,
            'mm/C':  1.0/1.0e-3,
            'm/°F':  1.0/1.8,
            'cm/°F':  1.0/1.8e-2,
            'mm/°F':  1.0/1.8e-3,
            'm/F':  1.0/1.8,
            'cm/F':  1.0/1.8e-2,
            'mm/F':  1.0/1.8e-3,
            }
        super().__init__(value, unit)
    
    def __add__(self, value2):
        if not isinstance(value2, InverseTemperatureGradient):
            raise UnitException(f"{self.__class__.__name__}: add {value2.__class__.__name__}")
        return InverseTemperatureGradient(self._value + value2._value)
    
    def __sub__(self, value2):
        if not isinstance(value2, InverseTemperatureGradient):
            raise TypeError
        return InverseTemperatureGradient(self._value - value2._value)
    
    def __mul__(self, value2):
        if isinstance(value2, numbers.Number):
            return InverseTemperatureGradient(self._value * value2)
        if isinstance(value2, Dimensionless):
            return InverseTemperatureGradient(self._value * value2._value)
        if isinstance(value2, TemperatureDifference):
            return Length(self._value * value2._value)
        raise TypeError
    
    def __truediv__(self, value2):
        if isinstance(value2, numbers.Number):
            return InverseTemperatureGradient(self._value / value2)
        if isinstance(value2, Dimensionless):
            return InverseTemperatureGradient(self._value / value2._value)
        if isinstance(value2, InverseTemperatureGradient):
            return Dimensionless(self._value / value2._value)
        raise TypeError
        
    def __rtruediv__(self, value2):
        if isinstance(value2, numbers.Number):
            #if value2!=1.0: raise ValueError
            return TemperatureGradient(value2 / self._value)
        if isinstance(value2, Dimensionless):
            #if value2._value!=1.0: raise ValueError
            return TemperatureGradient(value2._value / self._value)
        raise TypeError

'''
###########################################################
# ThermalConductance
###########################################################
'''
class ThermalConductance(Unit):
    def __init__(self, value: float, unit: str = 'W/(m^2*K)'):
        self._dimension = 'M T^-3 θ^-1'
        self._baseunit = 'W/(m^2*K)'
        self._preferredunit = unit
        self._conversions = {
            'kW/(m^2*K)':  1.0e3,
            'W/(m^2*K)':  1.0,
            '10^4*W/(m^2*K)':  1.0e-4,
            'W/(cm^2*K)':  1.0e-2 * 1.0e-2,
            'W/(mm^2*K)':  1.0e-3 * 1.0e-3,
            }
        super().__init__(value, unit)
    
    def __add__(self, value2):
        if not isinstance(value2, ThermalConductance):
            raise UnitException(f"{self.__class__.__name__}: add {value2.__class__.__name__}")
        return ThermalConductance(self._value + value2._value)
    
    def __sub__(self, value2):
        if not isinstance(value2, ThermalConductance):
            raise TypeError
        return ThermalConductance(self._value - value2._value)
    
    def __mul__(self, value2):
        if isinstance(value2, numbers.Number):
            return ThermalConductance(self._value * value2)
        if isinstance(value2, Dimensionless):
            return ThermalConductance(self._value * value2._value)
        if isinstance(value2, Area):
            return AbsoluteThermalConductance(self._value * value2._value)
        if isinstance(value2, Length):
            return ThermalConductivity(self._value * value2._value)
        raise TypeError
    
    def __truediv__(self, value2):
        if isinstance(value2, numbers.Number):
            return ThermalConductance(self._value / value2)
        if isinstance(value2, Dimensionless):
            return ThermalConductance(self._value / value2._value)
        if isinstance(value2, ThermalConductance):
            return Dimensionless(self._value / value2._value)
        raise TypeError
        
    def __rtruediv__(self, value2):
        if isinstance(value2, numbers.Number):
            #if value2!=1.0: raise ValueError
            return ThermalResistance(value2 / self._value)
        if isinstance(value2, Dimensionless):
            #if value2._value!=1.0: raise ValueError
            return ThermalResistance(value2._value / self._value)
        raise TypeError

'''
###########################################################
# ThermalResistance
###########################################################
'''
class ThermalResistance(Unit):
    def __init__(self, value: float, unit: str = '(m^2*K)/W'):
        self._dimension = 'M^-1 T^3 θ'
        self._baseunit = '(m^2*K)/W'
        self._preferredunit = unit
        self._conversions = {
            '(mm^2*K)/W':  1.0e3 * 1.0e3,
            '(cm^2*K)/W':  1.0e2 * 1.0e2,
            '(m^2*K)/W':  1.0,
            '10^-4*(m^2*K)/W':  1.0e4,
            '(m^2*K)/kW':  1.0e-3,
            }
        super().__init__(value, unit)
    
    def __add__(self, value2):
        if not isinstance(value2, ThermalResistance):
            raise UnitException(f"{self.__class__.__name__}: add {value2.__class__.__name__}")
        return ThermalResistance(self._value + value2._value)
    
    def __sub__(self, value2):
        if not isinstance(value2, ThermalResistance):
            raise TypeError
        return ThermalResistance(self._value - value2._value)
    
    def __mul__(self, value2):
        if isinstance(value2, numbers.Number):
            return ThermalResistance(self._value * value2)
        if isinstance(value2, Dimensionless):
            return ThermalResistance(self._value * value2._value)
        raise TypeError
    
    def __truediv__(self, value2):
        if isinstance(value2, numbers.Number):
            return ThermalResistance(self._value / value2)
        if isinstance(value2, Dimensionless):
            return ThermalResistance(self._value / value2._value)
        if isinstance(value2, ThermalResistance):
            return Dimensionless(self._value / value2._value)
        if isinstance(value2, Length):
            return ThermalResistivity(self._value / value2._value)

        raise TypeError
        
    def __rtruediv__(self, value2):
        if isinstance(value2, numbers.Number):
            #if value2!=1.0: raise ValueError
            return ThermalConductance(value2 / self._value)
        if isinstance(value2, Dimensionless):
            #if value2._value!=1.0: raise ValueError
            return ThermalConductance(value2._value / self._value)
        raise TypeError

'''
###########################################################
# AbsoluteThermalConductance
###########################################################
'''
class AbsoluteThermalConductance(Unit):
    def __init__(self, value: float, unit: str = 'W/K'):
        self._dimension = 'M L^2 T^-3 θ^-1'
        self._baseunit = 'W/K'
        self._preferredunit = unit
        self._conversions = {
            'W/K':  1.0,
            }
        super().__init__(value, unit)
    
    def __add__(self, value2):
        if not isinstance(value2, AbsoluteThermalConductance):
            raise UnitException(f"{self.__class__.__name__}: add {value2.__class__.__name__}")
        return AbsoluteThermalConductance(self._value + value2._value)
    
    def __sub__(self, value2):
        if not isinstance(value2, AbsoluteThermalConductance):
            raise TypeError
        return AbsoluteThermalConductance(self._value - value2._value)
    
    def __mul__(self, value2):
        if isinstance(value2, numbers.Number):
            return AbsoluteThermalConductance(self._value * value2)
        if isinstance(value2, Dimensionless):
            return AbsoluteThermalConductance(self._value * value2._value)
        raise TypeError
    
    def __truediv__(self, value2):
        if isinstance(value2, numbers.Number):
            return AbsoluteThermalConductance(self._value / value2)
        if isinstance(value2, Dimensionless):
            return AbsoluteThermalConductance(self._value / value2._value)
        if isinstance(value2, AbsoluteThermalConductance):
            return Dimensionless(self._value / value2._value)
        if isinstance(value2, Length):
            return ThermalConductivity(self._value / value2._value)
        raise TypeError
        
    def __rtruediv__(self, value2):
        if isinstance(value2, numbers.Number):
            #if value2!=1.0: raise ValueError
            return AbsoluteThermalResistance(value2 / self._value)
        if isinstance(value2, Dimensionless):
            #if value2._value!=1.0: raise ValueError
            return AbsoluteThermalResistance(value2._value / self._value)
        raise TypeError

'''
###########################################################
# AbsoluteThermalResistance
###########################################################
'''
class AbsoluteThermalResistance(Unit):
    def __init__(self, value: float, unit: str = 'K/W'):
        self._dimension = 'M^-1 L^-2 T^3 θ'
        self._baseunit = 'K/W'
        self._preferredunit = unit
        self._conversions = {
            'K/W':  1.0,
            }
        super().__init__(value, unit)
    
    def __add__(self, value2):
        if not isinstance(value2, AbsoluteThermalResistance):
            raise UnitException(f"{self.__class__.__name__}: add {value2.__class__.__name__}")
        return AbsoluteThermalResistance(self._value + value2._value)
    
    def __sub__(self, value2):
        if not isinstance(value2, AbsoluteThermalResistance):
            raise TypeError
        return AbsoluteThermalResistance(self._value - value2._value)
    
    def __mul__(self, value2):
        if isinstance(value2, numbers.Number):
            return AbsoluteThermalResistance(self._value * value2)
        if isinstance(value2, Dimensionless):
            return AbsoluteThermalResistance(self._value * value2._value)
        raise TypeError
    
    def __truediv__(self, value2):
        if isinstance(value2, numbers.Number):
            return AbsoluteThermalResistance(self._value / value2)
        if isinstance(value2, Dimensionless):
            return AbsoluteThermalResistance(self._value / value2._value)
        if isinstance(value2, AbsoluteThermalResistance):
            return Dimensionless(self._value / value2._value)
        raise TypeError
        
    def __rtruediv__(self, value2):
        if isinstance(value2, numbers.Number):
            #if value2!=1.0: raise ValueError
            return AbsoluteThermalConductance(value2 / self._value)
        if isinstance(value2, Dimensionless):
            #if value2._value!=1.0: raise ValueError
            return AbsoluteThermalConductance(value2._value / self._value)
        raise TypeError

'''
###########################################################
# ThermalConductivity
###########################################################
'''
class ThermalConductivity(Unit):
    def __init__(self, value: float, unit: str = 'W/(m*K)'):
        self._dimension = 'M L T^-3 θ^-1'
        self._baseunit = 'W/(m*K)'
        self._preferredunit = unit
        self._conversions = {
            'W/(m*K)':  1.0,
            'W/(cm*K)':  1.0e-2,
            'W/(mm*K)':  1.0e-3,
            }
        super().__init__(value, unit)
    
    def __add__(self, value2):
        if not isinstance(value2, ThermalConductivity):
            raise UnitException(f"{self.__class__.__name__}: add {value2.__class__.__name__}")
        return ThermalConductivity(self._value + value2._value)
    
    def __sub__(self, value2):
        if not isinstance(value2, ThermalConductivity):
            raise TypeError
        return ThermalConductivity(self._value - value2._value)
    
    def __mul__(self, value2):
        if isinstance(value2, numbers.Number):
            return ThermalConductivity(self._value * value2)
        if isinstance(value2, Dimensionless):
            return ThermalConductivity(self._value * value2._value)
        if isinstance(value2, Length):
            return AbsoluteThermalConductance(self._value * value2._value)

        raise TypeError
    
    def __truediv__(self, value2):
        if isinstance(value2, numbers.Number):
            return ThermalConductivity(self._value / value2)
        if isinstance(value2, Dimensionless):
            return ThermalConductivity(self._value / value2._value)
        if isinstance(value2, ThermalConductivity):
            return Dimensionless(self._value / value2._value)
        raise TypeError
        
    def __rtruediv__(self, value2):
        if isinstance(value2, numbers.Number):
            #if value2!=1.0: raise ValueError
            return ThermalResistivity(value2 / self._value)
        if isinstance(value2, Dimensionless):
            #if value2._value!=1.0: raise ValueError
            return ThermalResistivity(value2._value / self._value)
        raise TypeError

'''
###########################################################
# ThermalResistivity
###########################################################
'''
class ThermalResistivity(Unit):
    def __init__(self, value: float, unit: str = '(m*K)/W'):
        self._dimension = 'M^-1 L^-1 T^3 θ'
        self._baseunit = '(m*K)/W'
        self._preferredunit = unit
        self._conversions = {
            '(mm*K)/W':  1.0e3,
            '(cm*K)/W':  1.0e2,
            '(m*K)/W':  1.0,
            }
        super().__init__(value, unit)
    
    def __add__(self, value2):
        if not isinstance(value2, ThermalResistivity):
            raise UnitException(f"{self.__class__.__name__}: add {value2.__class__.__name__}")
        return ThermalResistivity(self._value + value2._value)
    
    def __sub__(self, value2):
        if not isinstance(value2, ThermalResistivity):
            raise TypeError
        return ThermalResistivity(self._value - value2._value)
    
    def __mul__(self, value2):
        if isinstance(value2, numbers.Number):
            return ThermalResistivity(self._value * value2)
        if isinstance(value2, Dimensionless):
            return ThermalResistivity(self._value * value2._value)
        raise TypeError
    
    def __truediv__(self, value2):
        if isinstance(value2, numbers.Number):
            return ThermalResistivity(self._value / value2)
        if isinstance(value2, Dimensionless):
            return ThermalResistivity(self._value / value2._value)
        if isinstance(value2, ThermalResistivity):
            return Dimensionless(self._value / value2._value)
        raise TypeError
        
    def __rtruediv__(self, value2):
        if isinstance(value2, numbers.Number):
            #if value2!=1.0: raise ValueError
            return ThermalConductivity(value2 / self._value)
        if isinstance(value2, Dimensionless):
            #if value2._value!=1.0: raise ValueError
            return ThermalConductivity(value2._value / self._value)
        raise TypeError

'''
###########################################################
# DynamicViscosity
###########################################################
'''
class DynamicViscosity(Unit):
    def __init__(self, value: float, unit: str = '(N*s)/m^2'):
        self._dimension = 'M L^-1 T^-1'
        self._baseunit = '(N*s)/m^2'
        self._preferredunit = unit
        self._conversions = {
            '(N*s)/m^2': 1.0,
            'Pa*s': 1.0,
            'kg/(m*s)': 1.0,
            'P': 1.0e1,
            'Poise': 1.0e1,
            'mPa*s': 1.0e3,
            'cP': 1.0e3
            }
        super().__init__(value, unit)
    
    def __add__(self, value2):
        if not isinstance(value2, DynamicViscosity):
            raise TypeError
        return DynamicViscosity(self._value + value2._value)
    
    def __sub__(self, value2):
        if not isinstance(value2, DynamicViscosity):
            raise TypeError
        return DynamicViscosity(self._value - value2._value)
    
    def __mul__(self, value2):
        if isinstance(value2, numbers.Number):
            return DynamicViscosity(self._value * value2)
        if isinstance(value2, Dimensionless):
            return DynamicViscosity(self._value * value2._value)
        raise TypeError
    
    def __truediv__(self, value2):
        if isinstance(value2, numbers.Number):
            return DynamicViscosity(self._value / value2)
        if isinstance(value2, Dimensionless):
            return DynamicViscosity(self._value / value2._value)
        if isinstance(value2, DynamicViscosity):
            return Dimensionless(self._value / value2._value)
        if isinstance(value2, Density):
            return KinematicViscosity(self._value / value2._value)
        if isinstance(value2, KinematicViscosity):
            return Density(self._value / value2._value)
        raise TypeError
        
    def __rtruediv__(self, value2):
        if isinstance(value2, numbers.Number):
            #if value2!=1.0: raise ValueError
            return DynamicViscosity(value2 / self._value)
        if isinstance(value2, Dimensionless):
            #if value2._value!=1.0: raise ValueError
            return DynamicViscosity(value2._value / self._value)
        raise TypeError


'''
###########################################################
# KinematicViscosity
###########################################################
'''
class KinematicViscosity(Unit):
    def __init__(self, value: float, unit: str = 'm^2/s'):
        self._dimension = 'L^2 T^-1'
        self._baseunit = 'm^2/s'
        self._preferredunit = unit
        self._conversions = {
            'm^2/s': 1.0,
            'J*s/kg': 1.0
            }
        super().__init__(value, unit)
    
    def __add__(self, value2):
        if not isinstance(value2, KinematicViscosity):
            raise TypeError
        return KinematicViscosity(self._value + value2._value)
    
    def __sub__(self, value2):
        if not isinstance(value2, KinematicViscosity):
            raise TypeError
        return KinematicViscosity(self._value - value2._value)
    
    def __mul__(self, value2):
        if isinstance(value2, numbers.Number):
            return KinematicViscosity(self._value * value2)
        if isinstance(value2, Dimensionless):
            return KinematicViscosity(self._value * value2._value)
        if isinstance(value2, Density):
            return DynamicViscosity(self._value * value2._value)
        raise TypeError
    
    def __truediv__(self, value2):
        if isinstance(value2, numbers.Number):
            return KinematicViscosity(self._value / value2)
        if isinstance(value2, Dimensionless):
            return KinematicViscosity(self._value / value2._value)
        if isinstance(value2, KinematicViscosity):
            return Dimensionless(self._value / value2._value)
        raise TypeError
        
    def __rtruediv__(self, value2):
        if isinstance(value2, numbers.Number):
            #if value2!=1.0: raise ValueError
            return KinematicViscosity(value2 / self._value)
        if isinstance(value2, Dimensionless):
            #if value2._value!=1.0: raise ValueError
            return KinematicViscosity(value2._value / self._value)
        raise TypeError

if __name__ == '__main__':
    import sys, inspect
    clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    for (n,cl) in clsmembers:
        if n == 'Iterable': continue
        if n == 'UnitException': continue
        if n == 'Unit': continue
        i = cl(0)
        print('{:30s}  {:15s}  {:15s}'.format(n, i.getDimension(), i.getBaseUnit()))
