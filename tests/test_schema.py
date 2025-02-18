import pytest
from dataframe_quality_checker import Schema

BASE={'version':1,'columns':{'x':{'type':'number'}}}

@pytest.mark.parametrize('rule',[
    {'type':'unknown'},{'type':'number','nullable':'yes'}, {'type':'number','max_missing':2},
    {'type':'number','min':3,'max':2}, {'type':'number','min':True},
    {'type':'string','regex':'['}, {'type':'integer','regex':'x'},
    {'type':'number','allowed':[]}, {'type':'number','mystery':1},
    {'type':'number','outlier':{'method':'bad'}},
    {'type':'number','outlier':{'method':'iqr','threshold':0}},
    {'type':'number','outlier':{'method':'zscore','min_samples':1}},
])
def test_invalid_rules(rule):
    with pytest.raises(ValueError):Schema.from_dict({'version':1,'columns':{'x':rule}})

@pytest.mark.parametrize('extra',[{'version':True},{'min_rows':-1},{'sample_limit':101},{'allow_extra':1},{'columns':{}},{'unknown':1}])
def test_invalid_top_level(extra):
    with pytest.raises(ValueError):Schema.from_dict({**BASE,**extra})

def test_schema_copies_input():
    source={'version':1,'columns':{'x':{'type':'number'}}}
    schema=Schema.from_dict(source)
    source['columns']['x']['type']='string'
    assert schema.columns['x']['type']=='number'
