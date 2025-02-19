import pandas as pd
import pytest
from dataframe_quality_checker import validate

SCHEMA={'version':1,'columns':{'x':{'type':'number'},'optional':{'type':'string','required':False}}}

def test_missing_extra():
    result=validate(pd.DataFrame({'other':[1]}),SCHEMA)
    assert not result['passed']
    assert result['failed_error_checks']==2

def test_allow_extra():
    assert validate(pd.DataFrame({'x':[1],'extra':[2]}),{**SCHEMA,'allow_extra':True})['passed']

def test_empty():
    data=pd.DataFrame({'x':[]})
    assert not validate(data,SCHEMA)['passed']
    assert validate(data,{**SCHEMA,'min_rows':0})['passed']

def test_not_mutated():
    data=pd.DataFrame({'x':[1,None,3]})
    original=data.copy(deep=True)
    validate(data,SCHEMA)
    pd.testing.assert_frame_equal(data,original)

def test_duplicate_columns():
    with pytest.raises(ValueError):validate(pd.DataFrame([[1,2]],columns=['x','x']),SCHEMA)

def test_non_scalar():
    with pytest.raises(ValueError):validate(pd.DataFrame({'x':[[1,2]]}),SCHEMA)
