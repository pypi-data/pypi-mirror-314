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

ISO286Grades: TypeAlias = list[str]
ISO286Dimension: TypeAlias = tuple[Length, Length]
ISO286Tolerance: TypeAlias = tuple[Length, Length]

class ISO286():
    def __init__(self):
        logging.basicConfig(format="{asctime} [{levelname}:{name}]: {message}",
                        style="{",
                        datefmt="%Y-%m-%d %H:%M",
                        level=logging.INFO)
        self._logger = logging.getLogger('ISO286')
        self._grades = []
        self._dataByDimension = {}
        self._dataByGrade = {}
        
    def _delocalizeFloats(self, row):
        return [
            str(el).replace(',', '.') if isinstance(el, str) else el 
            for el in row
        ]

    def _readData(self, filename):
        csvfilename = pkg_resources.files('physeng.data').joinpath(filename)
        self._logger.debug(f'readData: {csvfilename}')
        
        with open(csvfilename, mode ='r') as file:
            rawrows = list(csv.reader(file, delimiter=';'))
            rows = []
            for r in rawrows:
                rows.append(self._delocalizeFloats(r))
            
            for g in rows[0][2::2]:
                self._grades.append(g)
                #print(g)
        
            for row in rows[2:]:
                #dimension = (float(row[0]),float(row[1]))
                dimension = (Length(float(row[0]), 'mm'), Length(float(row[1]), 'mm'))
                self._dataByDimension[dimension] = {}
                #print((float(row[0]),float(row[1]))) 
        
                it = iter(row[2:])
                values = zip(it, it)
                for i,v in enumerate(values):
                    if v[0]=='' or v[1]=='': continue
                    value = (Length(float(v[0]), 'um'), Length(float(v[1]), 'um'))
                
                    if self._grades[i] not in self._dataByGrade:
                        self._dataByGrade[self._grades[i]] = {}
                    
                    self._dataByGrade[self._grades[i]][dimension] = value
                    self._dataByDimension[dimension][self._grades[i]] = value

    def grades(self) -> ISO286Grades:
        '''
        Returns the known tolerance grades.

        Returns
        -------
        ISO286Grades
            List of tolerance grades
        '''
        
        return self._grades

    def gradesForDimension(self, dimension: Length) -> ISO286Grades:
        '''
        Returns the known tolerance grades for a given dimension.

        Parameters
        ----------
        dimension : Length
            Dimension

        Returns
        -------
        ISO286Grades
            List of tolerance grades
        '''

        for d,v in self._dataByDimension.items():
            if dimension>d[0] and dimension<=d[1]:
                return list(v.keys())
        return []

    def dimensionsForGrade(self, grade: str) -> ISO286Dimension:
        '''
        Returns the known dimension range for a given tolerance grade.

        Parameters
        ----------
        grade : str
            Tolerance grade

        Returns
        -------
        ISO286Dimension
            Dimension range as a tuple(Length, Length)
        '''
        
        for g,v in self._dataByGrade.items():
            if g==grade:
                l = list(map(list, zip(*list(v.keys()))))
                return((min(l[0]), max(l[1])))
        return (np.nan, np.nan)
    
    def tolerance(self, dimension: Length, grade: str) -> ISO286Tolerance:
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
        ISO286Tolerance
            Tolerance window as a tuple(Length, Length)

        '''
        
        for d,v in self._dataByDimension.items():
            if dimension>d[0] and dimension<=d[1]:
                if grade in v.keys():
                    return(v[grade])
        return (np.nan, np.nan)
    
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
            Tolerance window in micrometer as a tuple(float, float)

        '''
        
        (t1,t2) = self.tolerance(dimension, grade)
        return (t1.asFloat('um'), t2.asFloat('um'))

@Singleton
class ISO286Hole(ISO286):
    def __init__(self):
        super().__init__()
        self._logger.name = 'ISO286Hole'
        self._readData('ISO286Hole.csv')

@Singleton
class ISO286Shaft(ISO286):
    def __init__(self):
        super().__init__()
        self._logger.name = 'ISO286Shaft'
        self._readData('ISO286Shaft.csv')
