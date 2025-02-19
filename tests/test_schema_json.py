import pytest
from dataframe_quality_checker import Schema

@pytest.mark.parametrize('text',[
    '{"version":1,"version":1,"columns":{"x":{"type":"number"}}}',
    '{"version":1,"columns":{"x":{"type":"number","max_missing":NaN}}}',
])
def test_bad_json(tmp_path,text):
    path=tmp_path/'schema.json';path.write_text(text)
    with pytest.raises(ValueError):Schema.load(path)
