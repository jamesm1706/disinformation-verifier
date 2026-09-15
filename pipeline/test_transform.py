import pandas as pd
 
from transform import build_dataframe, clean_list_columns


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
 

def test_clean_list_columns_keeps_lists_as_lists():
    df = pd.DataFrame({
        "id": [1, 2],
        "tags": [["a", "b"], ["c"]],
    })
 
    cleaned = clean_list_columns(df, columns=["tags"])
 
    assert cleaned["tags"].tolist() == [["a", "b"], ["c"]]
 
 
def test_clean_list_columns_converts_missing_values_to_empty_list():
    df = pd.DataFrame({
        "id": [1, 2],
        "tags": [["a"], None],
    })
 
    cleaned = clean_list_columns(df, columns=["tags"])
 
    assert cleaned["tags"].tolist() == [["a"], []]
 
 
def test_clean_list_columns_leaves_other_columns_untouched():
    df = pd.DataFrame({
        "id": [1],
        "tags": [["a"]],
    })
 
    cleaned = clean_list_columns(df, columns=["tags"])
 
    assert cleaned["id"].tolist() == [1]