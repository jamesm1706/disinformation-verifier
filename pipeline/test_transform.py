import pandas as pd
 
from transform import build_dataframe


def test_build_dataframe_from_list_of_dicts():
    records = [
        {"a": 1, "b": "x"},
        {"a": 2, "b": "y"},
    ]
 
    df = build_dataframe(records)
 
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert list(df.columns) == ["a", "b"]
 
 
def test_build_dataframe_from_empty_list():
    df = build_dataframe([])
 
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0
 