"""Analytics visualisations and chart renderers."""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import theme


def render_outlet_analytics_chart():
    """Render an interactive bar chart of verifications grouped by publisher."""

    data = {
        "Publisher": ["Full Fact", "FactCheck.org", "PolitiFact", "Reuters Fact Check", "AP Fact Check"],
        "Verified Claims": [412, 328, 245, 180, 83],
        "Accuracy Rating": ["98%", "96%", "95%", "99%", "97%"]
    }

    fig = px.bar(
        data,
        x="Publisher",
        y="Verified Claims",
        text="Verified Claims",
        color_discrete_sequence=[theme.COLOUR_PRIMARY]
    )

    fig.update_traces(
        texttemplate='%{text}',
        textposition='outside',
        marker_line_color=theme.COLOUR_TEXT_MAIN,
        marker_line_width=1
    )

    fig.update_layout(
        height=320,
        margin=dict(l=20, r=20, t=30, b=40),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title="",
        yaxis_title="Total Ingested Claims",
        font=dict(color=theme.COLOUR_TEXT_MAIN),
        yaxis=dict(showgrid=True, gridcolor=theme.COLOUR_BORDER)
    )

    return fig


def render_confidence_gauge(confidence_score: float, rating: str):
    """Render an enterprise confidence chart."""

    # Pick indicator color based on verdict rating
    if rating == "Supported":
        bar_color = theme.COLOUR_SUCCESS_FG
    elif rating == "Contradicted":
        bar_color = theme.COLOUR_DANGER_FG
    elif rating == "Missing Context":
        bar_color = theme.COLOUR_WARNING_FG
    else:
        bar_color = theme.COLOUR_PRIMARY

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=confidence_score,
        number={'suffix': "%", 'font': {
            'color': theme.COLOUR_TEXT_MAIN, 'size': 32}},
        title={'text': "Model Confidence", 'font': {
            'color': theme.COLOUR_TEXT_MUTED, 'size': 14}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': theme.COLOUR_BORDER},
            'bar': {'color': bar_color},
            'bgcolor': "#FFFFFF",
            'borderwidth': 1,
            'borderwidth': 1,
            'bordercolor': theme.COLOUR_BORDER,
            'steps': [
                {'range': [0, 50], 'color': "#F8FAFC"},
                {'range': [50, 100], 'color': "#F1F5F9"}
            ],
        }
    ))

    fig.update_layout(
        height=220,
        margin=dict(l=20, r=20, t=50, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig
