from datetime import date,datetime
import math
import numbers
import numpy as np
import pandas as pd
from .results import row_check

def missing(value) -> bool:
    flag=pd.isna(value)
    if not isinstance(flag,(bool,np.bool_)):
        raise ValueError('DataFrame cells must be scalar values, not lists or arrays')
    return bool(flag)

def matches(value,kind: str) -> bool:
    if missing(value):
        return True
    if kind=='string':
        return isinstance(value,str)
    if kind=='boolean':
        return isinstance(value,(bool,np.bool_))
    if kind in {'number','integer'}:
        if isinstance(value,(bool,np.bool_)) or not isinstance(value,numbers.Real):
            return False
        if not math.isfinite(value):
            return False
        return kind=='number' or float(value).is_integer()
    if kind=='datetime':
        if not isinstance(value,(str,date,datetime,pd.Timestamp,np.datetime64)):
            return False
        try:
            stamp=pd.Timestamp(value)
            return not pd.isna(stamp)
        except (ValueError,TypeError,OverflowError):
            return False
    raise ValueError('unknown column type')

def type_check(series: pd.Series,kind: str,limit: int):
    mask=[not matches(value,kind) for value in series]
    return row_check('type',series.name,mask,limit,f'nonmissing values must be {kind}')

def numeric_values(series: pd.Series) -> np.ndarray:
    return np.array([float(v) if not missing(v) and matches(v,'number') else np.nan
                     for v in series],dtype=float)
