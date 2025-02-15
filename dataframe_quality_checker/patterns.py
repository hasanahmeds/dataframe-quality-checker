import re
import pandas as pd
from .results import row_check

def pattern_check(series: pd.Series,pattern: str,limit: int):
    compiled=re.compile(pattern)
    mask=[isinstance(v,str) and compiled.fullmatch(v) is None for v in series]
    return row_check('regex',series.name,mask,limit,'strings must fully match the pattern')
