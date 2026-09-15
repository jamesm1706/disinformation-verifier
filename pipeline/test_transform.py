import pandas as pd
 
from transform import build_dataframe, clean_list_value, clean_text_value, filter_tags, clean_bool_value


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
 
 
def test_clean_list_value_keeps_a_list_as_is():
    assert clean_list_value(["a", "b"]) == ["a", "b"]
 
 
def test_clean_list_value_converts_none_to_empty_list():
    assert clean_list_value(None) == []
 
 
def test_clean_list_value_converts_non_list_to_empty_list():
    assert clean_list_value("not a list") == []
 
 
def test_clean_text_value_strips_whitespace():
    assert clean_text_value("  hello  ") == "hello"
 
 
def test_clean_text_value_converts_none_to_empty_string():
    assert clean_text_value(None) == ""
 
 
def test_clean_text_value_converts_non_string_to_empty_string():
    assert clean_text_value(123) == ""


def test_filter_tags_removes_excluded_tags():
    tags = ["fact-checking", "economy", "inflation"]
 
    result = filter_tags(tags, exclude=["fact-checking"])
 
    assert result == ["economy", "inflation"]
 
 
def test_filter_tags_limits_to_five():
    tags = ["a", "b", "c", "d", "e", "f", "g"]
 
    result = filter_tags(tags, exclude=[])
 
    assert result == ["a", "b", "c", "d", "e"]
 
 
def test_filter_tags_is_case_insensitive_for_exclusions():
    tags = ["Fact-Checking", "economy"]
 
    result = filter_tags(tags, exclude=["fact-checking"])
 
    assert result == ["economy"]
 
 
def test_filter_tags_accepts_custom_exclude_list():
    tags = ["news", "economy", "inflation"]
 
    result = filter_tags(tags, exclude=["news"])
 
    assert result == ["economy", "inflation"]
 
 
def test_filter_tags_handles_empty_list():
    assert filter_tags([], exclude=[]) == []
 
 
def test_filter_tags_defaults_to_no_exclusions():
    tags = ["economy", "inflation"]
 
    result = filter_tags(tags)
 
    assert result == ["economy", "inflation"]

def test_clean_bool_value_keeps_true_as_true():
    assert clean_bool_value(True) is True
 
 
def test_clean_bool_value_keeps_false_as_false():
    assert clean_bool_value(False) is False
 
 
def test_clean_bool_value_converts_none_to_false():
    assert clean_bool_value(None) is False
 
 
def test_clean_bool_value_converts_non_bool_to_false():
    assert clean_bool_value("true") is False