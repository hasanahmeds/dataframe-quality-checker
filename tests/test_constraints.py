import pandas as pd
from dataframe_quality_checker import validate

def test_range_and_allowed():
    data=pd.DataFrame({'x':[-1,0,10,11,None],'c':['a','b','z',None,'a']})
    result=validate(data,{'version':1,'columns':{'x':{'type':'number','min':0,'max':10},'c':{'type':'string','allowed':['a','b']}}})
    checks={c['rule']:c for c in result['checks'] if c['rule'] in {'range','allowed'}}
    assert checks['range']['sample_positions']==[0,3]
    assert checks['allowed']['sample_positions']==[2]

def test_fullmatch_and_type_separation():
    data=pd.DataFrame({'x':['ABC','ABCD',123,None]})
    result=validate(data,{'version':1,'columns':{'x':{'type':'string','regex':'[A-Z]{3}'}}})
    checks={c['rule']:c for c in result['checks']}
    assert checks['regex']['sample_positions']==[1]
    assert checks['type']['sample_positions']==[2]
