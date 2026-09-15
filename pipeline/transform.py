import logging
 
import pandas as pd
 
logger = logging.getLogger(__name__)
 
DEFAULT_EXCLUDED_TAGS = ["fact-checking"]

 
def build_dataframe(records: list[dict]) -> pd.DataFrame:
    """Convert a list of dicts into a DataFrame."""
    return pd.DataFrame(records)
 
 
def clean_list_value(value):
    """Return value if it's a list, else an empty list."""
    return value if isinstance(value, list) else []
 
 
def clean_text_value(value):
    """Return a stripped string, or "" if not a string."""
    return value.strip() if isinstance(value, str) else ""
 

def filter_tags(tags: list[str], exclude: list[str] = None, max_tags: int = 5) -> list[str]:
    """Remove excluded tags and cap the result at max_tags."""
    exclude = exclude if exclude is not None else []
    excluded_lower = {e.lower() for e in exclude}
    filtered = [tag for tag in tags if tag.lower() not in excluded_lower]
    return filtered[:max_tags]
 

def clean_bool_value(value):
    """Return value if it's a bool, else False."""
    return value if isinstance(value, bool) else False
