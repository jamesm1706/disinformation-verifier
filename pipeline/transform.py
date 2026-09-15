import logging
 
import pandas as pd
 
logger = logging.getLogger(__name__)
 
 
def build_dataframe(records: list[dict]) -> pd.DataFrame:
    """Convert a list of dicts into a DataFrame."""
    return pd.DataFrame(records)
 
 
def clean_list_value(value):
    """Return value if it's a list, else an empty list."""
    return value if isinstance(value, list) else []
 
 
def clean_text_value(value):
    """Return a stripped string, or "" if not a string."""
    return value.strip() if isinstance(value, str) else ""
 