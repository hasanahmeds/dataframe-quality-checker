from dataclasses import dataclass
import json
from pathlib import Path

TYPES={'integer','number','string','boolean','datetime'}

@dataclass(frozen=True)
class Schema:
    columns: dict
    allow_extra: bool = False
    min_rows: int = 1
    unique_rows: bool = False
    sample_limit: int = 5

    @classmethod
    def from_dict(cls,data: dict) -> "Schema":
        if not isinstance(data,dict) or set(data)-{'version','columns','allow_extra','min_rows','unique_rows','sample_limit'}:
            raise ValueError('schema must be an object with known keys')
        if type(data.get('version')) is not int or data['version']!=1:
            raise ValueError('schema version must be 1')
        columns=data.get('columns')
        if not isinstance(columns,dict) or not columns:
            raise ValueError('columns must be a nonempty object')
        for name,rule in columns.items():
            if not isinstance(name,str) or not name or not isinstance(rule,dict):
                raise ValueError('column names must be nonempty strings and rules must be objects')
            validate_rule(rule)
        options={k:data[k] for k in ('allow_extra','min_rows','unique_rows','sample_limit') if k in data}
        result=cls(json.loads(json.dumps(columns)),**options)
        for key in ('allow_extra','unique_rows'):
            if type(getattr(result,key)) is not bool:
                raise ValueError(f'{key} must be boolean')
        for key,maximum in [('min_rows',100000000),('sample_limit',100)]:
            value=getattr(result,key)
            if type(value) is not int or not 0<=value<=maximum:
                raise ValueError(f'invalid {key}')
        return result

    @classmethod
    def load(cls,path: Path) -> "Schema":
        return cls.from_dict(json.loads(path.read_text(encoding='utf-8')))

def validate_rule(rule: dict) -> None:
    if set(rule)-{'type','required','nullable','max_missing','unique'}:
        raise ValueError('unknown column rule')
    if rule.get('type') not in TYPES:
        raise ValueError('unsupported or missing column type')
    for key in ('required','nullable','unique'):
        if key in rule and type(rule[key]) is not bool:
            raise ValueError(f'{key} must be boolean')
    if 'max_missing' in rule:
        value=rule['max_missing']
        if type(value) not in (int,float) or not 0<=value<=1:
            raise ValueError('max_missing must be a fraction in 0..1')
