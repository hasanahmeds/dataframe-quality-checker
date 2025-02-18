import numpy as np
import pandas as pd
import pytest
from dataframe_quality_checker.types import matches,type_check

@pytest.mark.parametrize('value,kind,expected',[
    (1,'integer',True),(1.0,'integer',True),(1.5,'integer',False),
    (True,'integer',False),('1','number',False),(np.inf,'number',False),
    (np.int64(2),'integer',True),(None,'string',True),(pd.NA,'integer',True),
    ('true','boolean',False),(np.bool_(True),'boolean',True),
    ('2024-02-29','datetime',True),('2024-02-30','datetime',False),
    (123,'datetime',False),
])
def test_matches(value,kind,expected):
    assert matches(value,kind)==expected

def test_nullable_integer_dtype():
    series=pd.Series([1,pd.NA,2],dtype='Int64',name='x')
    assert type_check(series,'integer',5).failed_count==0
