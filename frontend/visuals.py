"""Analytics visualisations and chart renderers."""

import streamlit as st
import pandas as pd


def render_outlet_analytics_chart():
    """Render verdict breakdown bar chart."""
    chart_data = pd.DataFrame({
        "Publisher": ["Reuters Fact Check", "BBC Verify", "Full Fact"],
        "Supported": [45, 30, 60],
        "Contradicted": [120, 95, 140],
        "Missing Context": [30, 40, 55]
    }).set_index("Publisher")

    st.bar_chart(chart_data)
