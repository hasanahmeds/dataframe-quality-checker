import csv
from pathlib import Path
import pandas as pd

def read_csv(path: Path,max_rows: int=1000000) -> pd.DataFrame:
    if type(max_rows) is not int or max_rows<1:
        raise ValueError('max_rows must be positive')
    with path.open(encoding='utf-8-sig',newline='') as stream:
        header=next(csv.reader(stream),None)
    if not header or any(not name.strip() for name in header):
        raise ValueError('CSV needs nonempty column names')
    if len(header)!=len(set(header)):
        raise ValueError('duplicate CSV column names')
    frame=pd.read_csv(path,encoding='utf-8-sig',nrows=max_rows+1)
    if len(frame)>max_rows:
        raise ValueError(f'input exceeds max_rows={max_rows}')
    return frame
