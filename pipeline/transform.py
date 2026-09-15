import logging
 
import pandas as pd
 
logger = logging.getLogger(__name__)
 
 
def build_dataframe(records: list[dict]) -> pd.DataFrame:
    """Convert a list of claim/verdict record dicts into a pandas DataFrame."""
    return pd.DataFrame(records)

def clean_list_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Ensure list-valued columns contain clean, consistent lists."""
    df = df.copy()
    for column in columns:
        df[column] = df[column].apply(lambda value: value if isinstance(value, list) else [])
    return df