import pandas as pd
from .constraints import constraints
from .missingness import check_missing
from .outliers import detect
from .patterns import pattern_check
from .schema import Schema
from .structure import check_structure
from .types import type_check,missing
from .uniqueness import unique_column,unique_rows

def validate(frame: pd.DataFrame,schema: Schema | dict) -> dict:
    schema=Schema.from_dict(schema) if isinstance(schema,dict) else schema
    if not isinstance(schema,Schema):
        raise ValueError('schema must be a Schema or dict')
    checks=check_structure(frame,schema)
    for column in frame:
        for value in frame[column]:
            missing(value)
    for column,rule in schema.columns.items():
        if column not in frame:
            continue
        series=frame[column]
        checks.append(type_check(series,rule['type'],schema.sample_limit))
        checks.extend(check_missing(series,rule,schema.sample_limit))
        if rule.get('unique',False):
            checks.append(unique_column(series,schema.sample_limit))
        checks.extend(constraints(series,rule,schema.sample_limit))
        if 'regex' in rule:
            checks.append(pattern_check(series,rule['regex'],schema.sample_limit))
        if 'outlier' in rule:
            checks.append(detect(series,rule['outlier'],schema.sample_limit))
    if schema.unique_rows:
        checks.append(unique_rows(frame,schema.sample_limit))
    errors=sum(c.severity=='error' and c.failed_count>0 for c in checks)
    warnings=sum(c.severity=='warning' and c.failed_count>0 for c in checks)
    return {'schema_version':1,'rows':len(frame),'columns':len(frame.columns),
            'passed':errors==0,'failed_error_checks':errors,'failed_warning_checks':warnings,
            'checks':[c.to_dict() for c in checks]}
