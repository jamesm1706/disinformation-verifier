"""Main Application Routing."""

import streamlit as st
import theme
import components

# Page Config
st.set_page_config(
    page_title="Disinformation Verifier",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Custom Theme Rules
theme.inject_custom_theme()

components.render_sidebar_logo()
components.render_system_status()

view = st.sidebar.radio(
    "Navigation",
    ["Claim Verification", "Top / New Stories",
        "Verification Logs", "Outlet Analytics"],
    label_visibility="collapsed"
)

# Routing Logic
if view == "Claim Verification":
    components.render_claim_verification_view()
elif view == "Top / New Stories":
    components.render_breaking_stories_view()
elif view == "Verification Logs":
    components.render_verification_logs_view()
elif view == "Outlet Analytics":
    components.render_outlet_credibility_view()
