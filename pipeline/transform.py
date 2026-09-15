import logging
 
import pandas as pd
 
logger = logging.getLogger(__name__)
 
 
def build_dataframe(records: list[dict]) -> pd.DataFrame:
    """Convert a list of claim/verdict record dicts into a pandas DataFrame."""
    return pd.DataFrame(records)