import pandas as pd
from dataframe_quality_checker.outliers import detect

def test_iqr_extreme():
    result=detect(pd.Series([10,11,12,13,14,100],name='x'),{'method':'iqr'},5)
    assert result.sample_positions==[5] and result.severity=='warning'

def test_zero_iqr():
    result=detect(pd.Series([1,1,1,1,1,9],name='x'),{'method':'iqr'},5)
    assert result.sample_positions==[5]

def test_constant():
    for method in ['iqr','zscore']:
        assert detect(pd.Series([2]*10,name='x'),{'method':method},5).failed_count==0

def test_zscore():
    assert detect(pd.Series([0]*20+[100],name='x'),{'method':'zscore'},5).sample_positions==[20]

def test_small_samples():
    result=detect(pd.Series([1,2],name='x'),{'method':'iqr'},5)
    assert result.failed_count==0 and result.message.startswith('skipped:')
