import pandas as pd
from .results import Check
from .schema import Schema

def check_structure(frame: pd.DataFrame,schema: Schema) -> list[Check]:
    if not isinstance(frame,pd.DataFrame):
        raise ValueError('input must be a pandas DataFrame')
    if not all(isinstance(c,str) and c for c in frame.columns) or not frame.columns.is_unique:
        raise ValueError('DataFrame columns must be unique nonempty strings')
    checks=[Check('min_rows',None,'error',int(len(frame)<schema.min_rows),1,[],
                  f'require at least {schema.min_rows} rows')]
    for column,rule in schema.columns.items():
        if rule.get('required',True):
            checks.append(Check('required_column',column,'error',int(column not in frame),1,[],
                                'column must exist'))
    if not schema.allow_extra:
        for column in sorted(set(frame.columns)-set(schema.columns)):
            checks.append(Check('unexpected_column',column,'error',1,1,[],
                                'column is not declared in schema'))
    return checks
