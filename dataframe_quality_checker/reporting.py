import csv
import json
from typing import TextIO

def safe_cell(value):
    if isinstance(value,str) and (value.lstrip().startswith(('=','+','-','@')) or value.startswith(('\t','\r','\n'))):
        return "'"+value
    return value

def write_report(report: dict,stream: TextIO,format: str='json') -> None:
    if format=='json':
        json.dump(report,stream,indent=2,sort_keys=True,allow_nan=False)
        stream.write('\n')
    elif format=='csv':
        fields=['rule','column','severity','passed','failed_count','evaluated_count','sample_positions','message']
        writer=csv.writer(stream)
        writer.writerow(fields)
        for check in report['checks']:
            writer.writerow([safe_cell(json.dumps(check[k]) if k=='sample_positions' else check[k]) for k in fields])
    else:
        raise ValueError('unsupported report format')
