import json
from pathlib import Path
import pytest
from dataframe_quality_checker.cli import main
from dataframe_quality_checker.reader import read_csv

EXAMPLES=Path(__file__).resolve().parents[1]/'examples'

def test_clean(capsys):
    assert main([str(EXAMPLES/'clean.csv'),'--schema',str(EXAMPLES/'schema.json')])==0
    assert json.loads(capsys.readouterr().out)['passed']

def test_dirty(capsys):
    assert main([str(EXAMPLES/'dirty.csv'),'--schema',str(EXAMPLES/'schema.json')])==1
    result=json.loads(capsys.readouterr().out)
    assert not result['passed'] and result['failed_warning_checks']==1

def test_bad_path(tmp_path):
    assert main([str(tmp_path/'missing'),'--schema',str(EXAMPLES/'schema.json')])==2

def test_duplicate_headers(tmp_path):
    path=tmp_path/'a.csv';path.write_text('x,x\n1,2\n')
    with pytest.raises(ValueError,match='duplicate'):read_csv(path)

def test_row_limit():
    with pytest.raises(ValueError,match='max_rows'):read_csv(EXAMPLES/'clean.csv',2)

def test_input_protected(tmp_path):
    path=tmp_path/'a.csv';path.write_text('x\n1\n')
    assert main([str(path),'--schema',str(EXAMPLES/'schema.json'),'--output',str(path)])==2
    assert path.read_text()=='x\n1\n'
