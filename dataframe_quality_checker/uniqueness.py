import pandas as pd
from .results import row_check

def unique_column(series: pd.Series,limit: int):
    mask=series.notna() & series.duplicated(keep=False)
    return row_check('unique',series.name,mask,limit,'all nonmissing values must be unique')

def unique_rows(frame: pd.DataFrame,limit: int):
    return row_check('unique_rows',None,frame.duplicated(keep=False),limit,
                     'duplicate groups count every participating row')
