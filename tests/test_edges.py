import pandas as pd
from dataframe_quality_checker import validate
from dataframe_quality_checker.reader import read_csv
from dataframe_quality_checker.profile import profile

def test_profile():
    p=profile(pd.DataFrame({'x':[1,None]}))
    assert p['rows']==2 and p['columns'][0]['missing']==1

def test_boolean_extension_array():
    df=pd.DataFrame({'x':pd.Series([True,False,pd.NA],dtype='boolean')})
    assert validate(df,{'version':1,'columns':{'x':{'type':'boolean'}}})['passed']

def test_header_only(tmp_path):
    path=tmp_path/'data.csv';path.write_text('x\n')
    frame=read_csv(path)
    assert len(frame)==0
    assert validate(frame,{'version':1,'min_rows':0,'columns':{'x':{'type':'number'}}})['passed']

def test_deterministic_reports():
    df=pd.DataFrame({'x':[1,2,None]})
    schema={'version':1,'columns':{'x':{'type':'number','nullable':False}}}
    assert validate(df,schema)==validate(df,schema)
