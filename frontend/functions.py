"""Data logic and backend handlers."""

import pandas as pd


def verify_claim(claim_text: str, source_url: str = "") -> dict:
    """Return verification payload for UI presentation."""
    if not claim_text.strip() and not source_url.strip():
        return {}

    return {
        "claim": claim_text if claim_text else source_url,
        "rating": "Contradicted",
        "reasoning": (
            "Medical consensus and formal reporting confirm that while lemon water "
            "contains vitamins, there is zero clinical evidence that it cures or reverses diabetes."
        ),
        "sources": [
            {"name": "Reuters Fact Check", "url": "https://reuters.com",
                "snippet": "No clinical data supports lemon water as an effective diabetes treatment."},
            {"name": "Full Fact UK", "url": "https://fullfact.org",
                "snippet": "Analysis of viral health claims surrounding citrus juices and insulin regulation."}
        ]
    }


def get_breaking_claims() -> list[dict]:
    """Return top breaking feed items."""
    return [
        {"time": "10m ago", "outlet": "BBC Verify",
            "title": "Claim regarding central bank emergency interest rate cuts", "status": "Contradicted"},
        {"time": "45m ago", "outlet": "Full Fact",
            "title": "Statistics on regional hospital waiting times in shared image", "status": "Missing Context"},
        {"time": "2h ago", "outlet": "Reuters",
            "title": "Quote attributed to European Union trade representative", "status": "Supported"}
    ]


def get_filtered_logs(query: str, status: str) -> pd.DataFrame:
    """Return historical log table with unit labels in headers (De-duplication rule)."""
    df = pd.DataFrame([
        {"Timestamp": "2026-09-14 14:30", "Claim Statement": "Lemon water cures diabetes",
            "Verdict": "Contradicted", "Sources Consulted": 2, "Latency (s)": 3.8},
        {"Timestamp": "2026-09-14 12:15", "Claim Statement": "EV tax incentive changes starting next month",
            "Verdict": "Supported", "Sources Consulted": 3, "Latency (s)": 4.1},
        {"Timestamp": "2026-09-13 18:40", "Claim Statement": "Video shows recent protest in central London",
            "Verdict": "Missing Context", "Sources Consulted": 4, "Latency (s)": 5.2},
    ])

    if query:
        df = df[df["Claim Statement"].str.contains(query, case=False)]
    if status != "All":
        df = df[df["Verdict"] == status]

    return df
