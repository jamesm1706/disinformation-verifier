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


def clean_categorical_value(value, allowed: list[str]) -> str:
    """Return the lowercased value if it's in allowed, else "unknown"."""
    allowed_lower = {a.lower() for a in allowed}
    if isinstance(value, str) and value.lower() in allowed_lower:
        return value.lower()
    return "unknown"

def dedupe_list(values: list[str]) -> list[str]:
    """Remove case-insensitive duplicates, preserving first-seen order."""
    seen = set()
    result = []
    for value in values:
        key = value.lower()
        if key not in seen:
            seen.add(key)
            result.append(value)
    return result


CLAIM_TYPES = ["factual", "statistical", "opinion", "prediction", "quote"]
VERDICTS = ["verified", "disputed", "unsupported"]
 
 
def transform(records: list[dict]) -> pd.DataFrame:
    """Build a DataFrame from raw records and clean every column."""
    df = build_dataframe(records)
    if df.empty:
        return df
 
    df["text"] = df["text"].apply(clean_text_value)
    df["reasoning"] = df["reasoning"].apply(clean_text_value)
    df["checkable"] = df["checkable"].apply(clean_bool_value)
    df["claim_type"] = df["claim_type"].apply(lambda v: clean_categorical_value(v, CLAIM_TYPES))
    df["verdict"] = df["verdict"].apply(lambda v: clean_categorical_value(v, VERDICTS))
    df["entities"] = df["entities"].apply(clean_list_value).apply(dedupe_list)
    df["verdict_entities"] = df["verdict_entities"].apply(clean_list_value).apply(dedupe_list)
    df["verdict_tags"] = df["verdict_tags"].apply(clean_list_value).apply(
        lambda tags: filter_tags(dedupe_list(tags), exclude=["fact-checking"])
    )
    df["sources"] = df["sources"].apply(clean_list_value)
    return df


if __name__ == "__main__":
    sample_records = [
        {
            "text": "  The UK inflation rate rose to 4% in 2025.  ",
            "claim_type": "Factual",
            "entities": ["UK", "uk"],
            "checkable": True,
            "verdict": "Unsupported",
            "reasoning": "  Some reasoning.  ",
            "verdict_entities": None,
            "verdict_tags": ["fact-checking", "economy", "inflation"],
            "sources": ["https://bbc.com/a"],
        }
    ]
    cleaned = transform(sample_records)
    print(cleaned)