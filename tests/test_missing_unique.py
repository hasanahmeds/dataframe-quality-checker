import pandas as pd
from dataframe_quality_checker import validate

def rules(rule,**options):return {'version':1,'columns':{'x':rule},**options}

def test_missing_limit_inclusive():
    df=pd.DataFrame({'x':[1,None,None,4]})
    result=validate(df,rules({'type':'number','max_missing':0.5}))
    assert result['passed']
    assert not validate(df,rules({'type':'number','max_missing':0.49}))['passed']

def test_duplicate_positions_not_index_labels():
    df=pd.DataFrame({'x':[1,1,None,None]},index=[10,10,2,2])
    result=validate(df,rules({'type':'number','unique':True},sample_limit=1))
    check=next(c for c in result['checks'] if c['rule']=='unique')
    assert check['failed_count']==2 and check['sample_positions']==[0]

def test_unique_rows_counts_all_members():
    df=pd.DataFrame({'x':[1,1,2]})
    result=validate(df,rules({'type':'number'},unique_rows=True))
    assert next(c for c in result['checks'] if c['rule']=='unique_rows')['failed_count']==2
