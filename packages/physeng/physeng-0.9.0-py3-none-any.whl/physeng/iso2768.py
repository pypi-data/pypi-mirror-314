#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Andreas Mussgiller
"""

from typing import TypeAlias
import logging

import importlib.resources as pkg_resources
import csv

import numpy as np 

from physeng.singleton import Singleton
from physeng.units import Length

ISO2768LengthGrades: TypeAlias = list[str]
ISO2768LengthDimension: TypeAlias = Length
ISO2768LengthTolerance: TypeAlias = Length

@Singleton
class ISO2768Length():
    def __init__(self):
        logging.basicConfig(format="{asctime} [{levelname}:{name}]: {message}",
                        style="{",
                        datefmt="%Y-%m-%d %H:%M",
                        level=logging.INFO)
        self._logger = logging.getLogger('ISO2768')
        
        self._grades = []
        self._dataByDimension = {}
        self._dataByGrade = {}
        
        self._readData()
    
    def setLogLevel(self, loglevel):
        self._logger.setLevel(loglevel)
        
    def _delocalizeFloats(self, row):
        return [
            str(el).replace(',', '.') if isinstance(el, str) else el 
            for el in row
        ]

    def _readData(self):
        
        # Length
        csvfilename = pkg_resources.files('physeng.data').joinpath('ISO2768Length.csv')
        self._logger.debug(f'readData: {csvfilename}')
        
        with open(csvfilename, mode ='r') as file:
            rawrows = list(csv.reader(file, delimiter=';'))
            rows = []
            for r in rawrows:
                rows.append(self._delocalizeFloats(r))
            
            for g in rows[0][2:]:
                self._grades.append(g)

            for row in rows[1:]:
                #print(row)
                dimension = (Length(float(row[0]), 'mm'), Length(float(row[1]), 'mm'))
                self._dataByDimension[dimension] = {}
                
                for i,v in enumerate(row[2:]):
                    if v=='' or v=='': continue
                    value = Length(float(v), 'mm')
                    
                    if self._grades[i] not in self._dataByGrade:
                        self._dataByGrade[self._grades[i]] = {}
                    
                    self._dataByGrade[self._grades[i]][dimension] = value
                    self._dataByDimension[dimension][self._grades[i]] = value
                    
    def grades(self) -> ISO2768LengthGrades:
        '''
        Returns the known tolerance grades.
    
        Returns
        -------
        ISO2768LengthGrades
            List of tolerance grades
        '''
        
        return self._grades
    
    def gradesForDimension(self, dimension: Length) -> ISO2768LengthGrades:
        '''
        Returns the known tolerance grades for a given dimension.

        Parameters
        ----------
        dimension : Length
            Dimension

        Returns
        -------
        ISO2768LengthGrades
            List of tolerance grades
        '''

        for d,v in self._dataByDimension.items():
            if dimension>d[0] and dimension<=d[1]:
                return list(v.keys())
        return []
    
    def dimensionsForGrade(self, grade: str) -> ISO2768LengthDimension:
        '''
        Returns the known dimension range for a given tolerance grade.

        Parameters
        ----------
        grade : str
            Tolerance grade

        Returns
        -------
        ISO2768LengthDimension
            Dimension range as a tuple(Length, Length)
        '''
        
        for g,v in self._dataByGrade.items():
            if g==grade:
                l = list(map(list, zip(*list(v.keys()))))
                return((min(l[0]), max(l[1])))
        return (np.nan, np.nan)

    def tolerance(self, dimension: Length, grade: str) -> ISO2768LengthTolerance:
        '''
        Returns the tolerance window for a given dimension and
        tolerance grade.

        Parameters
        ----------
        dimension : Length
            Dimension
        grade : str
            Tolerance grade

        Returns
        -------
        ISO2768LengthTolerance
            Tolerance window in as a Length

        '''
        
        for d,v in self._dataByDimension.items():
            if dimension>d[0] and dimension<=d[1]:
                if grade in v.keys():
                    return v[grade]
        return np.nan

    def toleranceAsFloat(self, dimension: Length, grade: str) -> (float, float):
        '''
        Returns the tolerance window for a given dimension and
        tolerance grade in um

        Parameters
        ----------
        dimension : Length
            Dimension
        grade : str
            Tolerance grade

        Returns
        -------
        (float,float)
            Tolerance window in millimeter as a tuple(float, float)

        '''
        
        t = self.tolerance(dimension, grade)
        return t.asFloat('mm')

if __name__=='__main__':
    iso2768length = ISO2768Length()
    #iso2768length.setLogLevel(logging.DEBUG)
    
    print(iso2768length.grades())
    print()

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
    print()
    