"""Models that configure LLM output for claim extraction and analysis."""

from pydantic import BaseModel, Field
from typing import Literal


class Claim(BaseModel):
    """A single claim extracted from user-provided text."""
    text: str = Field(
        description="The claim stated in a single, self-contained, checkable sentence")
    claim_type: Literal["event", "statistic", "promise", "opinion", "other"] = Field(
        description=(
            "event: something that happened (a speech, a vote, an action). "
            "statistic: a specific number, set of numbers, or measurable fact - a fact or figure that should be externally verifiable. "
            "promise: a future commitment that cannot yet be true or false. "
            "opinion: a subjective statement reflecting personal beliefs or views that cannot be objectively verified. Eg. 'I think this policy is unfair.' , 'X is an idiot.'"
            "other: vague narrative/editorial framing with no specific verifiable content."
        ))
    verification_method: Literal["external_search", "context_only", "not_verifiable"] = Field(
        description=(
            "external_search: requires checking outside sources."
            "context_only: contextual information that is given in the article itself and can be verified without external sources, and would not need to be fact checked. e.g. 'x gave a speech on Sunday.', 'x raised concerns'"
            "not_verifiable: opinion, future promise, or too vague to check — skip entirely."
        )

    )
    tags: list[str] = Field(
        description="Topic tags for the claim, e.g. 'politics', 'health', 'climate'")


class InputAnalysis(BaseModel):
    """Analysis of the input text, including extracted claims, topic tags, and a summary."""
    claims: list[Claim]
    tags: list[str] = Field(
        description="Topic tags for the article, e.g. 'politics', 'health', 'climate'")
    summary: str = Field(
        description="One-sentence summary of what the article is about")


class VerdictResult(BaseModel):
    """Result of verifying a single claim against an article."""
    claim: str
    verdict: Literal["Supported", "Contradicted",
                     "Missing/Mixed Context", "Unclear"]
    reasoning: str
    entities: list[str] = Field(
        description="People, organizations, or places named in the claim")
    tags: list[str] = Field(
        description="Topic tags for the verdict, e.g. 'politics', 'health', 'climate'")
    sources: list[str] = Field(
        description="Article URL that the verdict is based on.")
