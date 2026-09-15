from dotenv import load_dotenv
import os
from firecrawl import Firecrawl
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import Literal


def extract(claim: str):
    firecrawl = Firecrawl(api_key=os.environ["API_KEY"])
    results = firecrawl.search(
        query=f'"{claim}" site:bbc.co.uk/news/articles OR site:reuters.com/fact-check OR site:fullfact.org',
        limit=5, scrape_options={"formats": ["markdown"]},
    )
    output = []
    for r in results.web:
        output.append(r.markdown or r.description)
    return "\n".join(output)


class Claim(BaseModel):
    text: str = Field(
        description="The claim stated in a single, self-contained, checkable sentence")
    claim_type: Literal["factual", "statistical", "opinion", "prediction", "quote"] = Field(
        description="Factual/statistical claims are checkable; opinions and predictions usually aren't"
    )
    entities: list[str] = Field(
        description="People, organizations, or places named in the claim")
    checkable: bool = Field(
        description="True if this claim can plausibly be verified against a source")


class InputAnalysis(BaseModel):
    claims: list[Claim]
    tags: list[str] = Field(
        description="Topic tags for the article, e.g. 'politics', 'health', 'climate'")
    summary: str = Field(
        description="One-sentence summary of what the article is about")


def get_claims_from_user(text: str) -> dict:
    """Send text to LLM service using the official OpenAI SDK."""
    # Automatically checks OPENAI_API_KEY (or LUNA_API_KEY fallback)
    api_key = os.environ["OPENAI_API_KEY"]
    base_url = os.environ["OPENAI_BASE_URL"]
    # If base_url is None, the SDK defaults to api.openai.com/v1
    client = OpenAI(
        api_key=api_key,
        base_url=base_url,
    )
    prompt = f"""
    Analyze the following article text:
    1. Extract specific key claims and statements from the article, ensuring each claim is individual and atomic.
    2. Return the extracted claims and statements in a structured JSON format.
    Text:
    {text[:4000]}
    """
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a precise data extraction assistant.",
            },
            {"role": "user", "content": prompt},
        ],
        response_format=InputAnalysis,
    )
    return response.choices[0].message.parsed.model_dump()


class VerdictResult(BaseModel):
    verdict: Literal["verified", "disputed", "unsupported"]
    reasoning: str
    entities: list[str] = Field(
        description="People, organizations, or places named in the claim")
    tags: list[str] = Field(
        description="Topic tags for the verdict, e.g. 'politics', 'health', 'climate'")
    sources: list[str] = Field(
        description="URLs or source names that informed the verdict")


def compare_claims_with_article(user_text: str, article_text: str) -> dict:
    """Send text to LLM service using the official OpenAI SDK."""
    # Automatically checks OPENAI_API_KEY (or LUNA_API_KEY fallback)
    api_key = os.environ["OPENAI_API_KEY"]
    base_url = os.environ["OPENAI_BASE_URL"]
    # If base_url is None, the SDK defaults to api.openai.com/v1
    client = OpenAI(
        api_key=api_key,
        base_url=base_url,
    )
    prompt = f"""
    Analyze the following verified article text in relation to the user's claim:
    1. Compare the article's claims with the user's claim and identify any agreements or discrepancies.
    2. Return whether the user's claim is verified, disputed, or unsupported based on the article's content.
    User Claim:
    {user_text[:4000]}
    Article Highlights:
    {article_text[:4000]}
    """
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a precise text comparison assistant.",
            },
            {"role": "user", "content": prompt},
        ],
        response_format=VerdictResult,
    )
    return response.choices[0].message.parsed.model_dump()


if __name__ == "__main__":
    load_dotenv()
    input_text = input("Enter your claim: ")
    analysis = get_claims_from_user(input_text)
    for claim in analysis["claims"]:
        if not claim["checkable"]:
            continue
        article_text = extract(claim["text"])
        result = compare_claims_with_article(claim["text"], article_text)
        print(result)
"""
Use the tbs parameter to filter results by time. Note that tbs only applies to web source results
— it does not filter news or images results. If you need time-filtered news, consider using a web source with
the site: operator to target specific news domains.
Common tbs values:
qdr:h - Past hour
qdr:d - Past 24 hours
qdr:w - Past week
qdr:m - Past month
qdr:y - Past year
sbd:1 - Sort by date (newest first)
sbd:1,cdr:1,cd_min:12/1/2024,cd_max:12/31/2024
'r.description' = Filtered down into highlights of the top web page content in markdown (sometimes?).
!!!!Results give same output but specifics can change between searches.
scrape_options={"formats": ["markdown"]} AND 'r.markdown' = Full web page content of multiple web pages in markdown.
Contains recommended stories and related content from the web pages.
"""
