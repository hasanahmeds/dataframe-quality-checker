import numpy as np
import pandas as pd
from .results import row_check
from .types import numeric_values,missing

def constraints(series: pd.Series,rule: dict,limit: int) -> list:
    checks=[]
    if 'min' in rule or 'max' in rule:
        values=numeric_values(series)
        mask=np.zeros(len(series),dtype=bool)
        if 'min' in rule:
            mask|=values<rule['min']
        if 'max' in rule:
            mask|=values>rule['max']
        checks.append(row_check('range',series.name,mask,limit,'numeric bounds are inclusive'))
    if 'allowed' in rule:
        mask=[not missing(v) and v not in rule['allowed'] for v in series]
        checks.append(row_check('allowed',series.name,mask,limit,'value must be in the allowed set'))
    return checks
