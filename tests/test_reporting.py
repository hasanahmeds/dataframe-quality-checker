import csv
from io import StringIO
import json
from pathlib import Path
import pytest
from dataframe_quality_checker.reporting import write_report
from dataframe_quality_checker.output import atomic_output
from dataframe_quality_checker.cli import main

def test_csv_formula_column():
    check={'rule':'type','column':'=1+1','severity':'error','passed':False,'failed_count':1,'evaluated_count':1,'sample_positions':[0],'message':'bad'}
    stream=StringIO();write_report({'checks':[check]},stream,'csv')
    assert list(csv.reader(StringIO(stream.getvalue())))[1][1]=="'=1+1"

def test_atomic_failure(tmp_path):
    path=tmp_path/'report';path.write_text('old')
    with pytest.raises(RuntimeError):
        with atomic_output(path) as stream:
            stream.write('partial')
            raise RuntimeError('abort')
    assert path.read_text()=='old'
    assert list(tmp_path.iterdir())==[path]

def test_warning_policy(tmp_path,capsys):
    path=tmp_path/'data.csv';path.write_text('x\n1\n1\n1\n1\n1\n100\n')
    schema=tmp_path/'schema.json';schema.write_text(json.dumps({'version':1,'columns':{'x':{'type':'number','outlier':{'method':'iqr'}}}}))
    args=[str(path),'--schema',str(schema)]
    assert main(args)==0
    assert json.loads(capsys.readouterr().out)['failed_warning_checks']==1
    assert main(args+['--fail-on-warning'])==1
