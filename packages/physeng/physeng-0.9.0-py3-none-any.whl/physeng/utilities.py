#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Andreas Mussgiller
"""

from datetime import datetime, timedelta

def DateTimeFromDecimalYear(year: float) -> datetime:
    '''
    Returns the datetime from a decimal year

    Parameters
    ----------
    year : float
        Decimal year

    Returns
    -------
    datetime
        Datetime calculated from decimal year

    '''
    y = int(year)
    rem = year - y
    base = datetime(y, 1, 1)
    result = base + timedelta(seconds=(base.replace(year=base.year + 1) - base).total_seconds() * rem)
    return result

def DateTimeToSeconds(dt):
    return dt.hour*60*60 + dt.minute*60 + dt.second
