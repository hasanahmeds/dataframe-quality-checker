import pandas as pd
from .results import Check,row_check

def check_missing(series: pd.Series,rule: dict,limit: int) -> list[Check]:
    mask=series.isna().to_numpy()
    checks=[]
    if not rule.get('nullable',True):
        checks.append(row_check('nullable',series.name,mask,limit,'null values are not allowed'))
    if 'max_missing' in rule:
        ratio=float(mask.mean()) if len(mask) else 0.0
        failed=ratio>rule['max_missing']
        checks.append(Check('max_missing',series.name,'error',int(mask.sum()) if failed else 0,
                            len(series),[int(i) for i,v in enumerate(mask) if v][:limit] if failed else [],
                            f"missing_fraction={ratio:.6g}; limit={rule['max_missing']}"))
    return checks
