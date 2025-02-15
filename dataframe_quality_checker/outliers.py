import numpy as np
import pandas as pd
from .results import Check,row_check
from .types import numeric_values

def detect(series: pd.Series,option: dict,limit: int) -> Check:
    values=numeric_values(series)
    finite=values[np.isfinite(values)]
    minimum=option.get('min_samples',5)
    method=option['method']
    if len(finite)<minimum:
        return Check('outlier_'+method,series.name,'warning',0,len(finite),[],
                     f'skipped: need {minimum} finite samples, found {len(finite)}')
    k=option.get('threshold',1.5)
    q1,q3=np.quantile(finite,[0.25,0.75])
    spread=q3-q1
    lower,upper=q1-k*spread,q3+k*spread
    mask=(values<lower)|(values>upper)
    return row_check('outlier_'+method,series.name,mask,limit,
                     f'IQR fences [{lower:.6g}, {upper:.6g}]; zero IQR uses equal fences','warning')
