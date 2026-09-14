"""UI layout views and visual components."""
import streamlit as st
import theme
import functions as fn
import visuals as vis


def render_page_header(title: str, description: str):
    """Render consistent, non-redundant section headers."""
    st.markdown(f"<h1>{title}</h1>", unsafe_allow_html=True)
    st.markdown(
        f"<p style='margin-bottom: 24px;'>{description}</p>", unsafe_allow_html=True)


def render_verdict_badge(rating: str):
    """Render status indicators pairing color with text and icons (Accessibility rule)."""
    badge_styles = {
        "Contradicted": (theme.COLOUR_DANGER_BG, theme.COLOUR_DANGER_FG, "❌"),
        "Supported": (theme.COLOUR_SUCCESS_BG, theme.COLOUR_SUCCESS_FG, "✅"),
        "Missing Context": (theme.COLOUR_WARNING_BG, theme.COLOUR_WARNING_FG, "⚠️"),
        "Unclear": (theme.COLOUR_APP_BG, theme.COLOUR_TEXT_MAIN, "❓")
    }

    bg, fg, icon = badge_styles.get(
        rating, (theme.COLOUR_APP_BG, theme.COLOUR_TEXT_MAIN, "ℹ️"))

    badge_html = f"""
    <div style="
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background-color: {bg};
        color: {fg};
        padding: 6px 12px;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 14px;
        margin-bottom: 12px;
    ">
        <span>{icon}</span>
        <span>VERDICT: {rating.upper()}</span>
    </div>
    """
    st.markdown(badge_html, unsafe_allow_html=True)


def render_claim_verification_view():
    """View 1: Main Verification Form & Results Layout."""
    render_page_header(
        "Claim Verification Workspace",
        "Submit headlines, quotes, or social media statements to check against primary fact-checking records."
    )

    # Use native Streamlit containers wrapped inside a single custom card div
    st.markdown('<div class="ui-card">', unsafe_allow_html=True)

    with st.form("claim_input_form", clear_on_submit=False):
        claim_input = st.text_area(
            "Statement or Headline Text",
            placeholder="e.g., 'Viral post claims drinking lemon water completely reverses diabetes...'",
            height=120
        )
        url_input = st.text_input(
            "Source Link (Optional)", placeholder="https://example.com/news/article")

        submit = st.form_submit_button("Verify Claim")

    st.markdown('</div>', unsafe_allow_html=True)

    if submit:
        result = fn.verify_claim(claim_input, url_input)
        if not result:
            st.warning("Please provide a statement or URL to verify.")
            return

        st.markdown('<div class="ui-card">', unsafe_allow_html=True)
        st.markdown("### Verification Summary")

        render_verdict_badge(result["rating"])

        st.markdown("**Reasoning Explanation:**")
        st.markdown(result["reasoning"])

        st.markdown("---")
        st.markdown("**Retrieved Source Evidence:**")

        for src in result["sources"]:
            st.markdown(f"""
            <div style="background-color: {theme.COLOUR_APP_BG}; border-left: 3px solid {theme.COLOUR_PRIMARY}; padding: 12px 16px; margin-bottom: 12px; border-radius: 0 8px 8px 0;">
                <strong style="color: {theme.COLOUR_TEXT_MAIN};">{src['name']}</strong><br>
                <span style="font-size: 14px; color: {theme.COLOUR_TEXT_MUTED};">"{src['snippet']}"</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)


def render_breaking_stories_view():
    """View 2: Clean Breaking News Feed."""
    render_page_header("Top Breaking Claims",
                       "Recent claims indexed from primary fact-checking outlets.")

    items = fn.get_breaking_claims()
    for item in items:
        st.markdown(
            '<div class="ui-card" style="padding: 16px 24px;">', unsafe_allow_html=True)
        col_content, col_badge = st.columns([4, 1.5])

        with col_content:
            st.markdown(
                f"<span style='font-size: 12px; color: {theme.COLOUR_TEXT_MUTED};'>{item['time']} • {item['outlet']}</span>", unsafe_allow_html=True)
            st.markdown(
                f"<strong style='font-size: 16px; color: {theme.COLOUR_TEXT_MAIN};'>{item['title']}</strong>", unsafe_allow_html=True)

        with col_badge:
            render_verdict_badge(item["status"])

        st.markdown('</div>', unsafe_allow_html=True)


def render_verification_logs_view():
    """View 3: Filterable Data Table."""
    render_page_header("Verification History Logs",
                       "Search and review past newsroom claim checks.")

    st.markdown('<div class="ui-card">', unsafe_allow_html=True)
    c1, c2 = st.columns([3, 1])
    with c1:
        query = st.text_input("Filter by Keyword",
                              placeholder="Search claim keywords...")
    with c2:
        status = st.selectbox("Verdict Filter", [
                              "All", "Supported", "Contradicted", "Missing Context", "Unclear"])
    st.markdown('</div>', unsafe_allow_html=True)

    df = fn.get_filtered_logs(query, status)

    st.markdown('<div class="ui-card">', unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)


def render_outlet_credibility_view():
    """View 4: Metric Cards & Data Analytics."""
    render_page_header("Outlet Source Analytics",
                       "Distribution metrics across ingested fact-checking partners.")

    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(
            '<div class="ui-card" style="text-align: center;">', unsafe_allow_html=True)
        st.caption("Total Claims Checked")
        st.markdown(
            f"<h2 style='margin: 0 !important; color: {theme.COLOUR_PRIMARY} !important;'>1,248</h2>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with m2:
        st.markdown(
            '<div class="ui-card" style="text-align: center;">', unsafe_allow_html=True)
        st.caption("Primary Source")
        st.markdown(
            f"<h2 style='margin: 0 !important; color: {theme.COLOUR_TEXT_MAIN} !important;'>Full Fact</h2>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with m3:
        st.markdown(
            '<div class="ui-card" style="text-align: center;">', unsafe_allow_html=True)
        st.caption("Avg System Latency")
        st.markdown(
            "<h2 style='margin: 0 !important; color: #16A34A !important;'>4.2s</h2>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="ui-card">', unsafe_allow_html=True)
    st.markdown("### Verifications by Publisher")
    vis.render_outlet_analytics_chart()
    st.markdown('</div>', unsafe_allow_html=True)


def render_sidebar_logo():
    """Render the Data Pulse SVG logo inside the Streamlit sidebar."""
    logo_svg = """
    <div style="padding: 4px 0px 16px 0px;">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 80" width="100%">
            <g transform="translate(0, 5)">
                <!-- Document Container -->
                <rect x="4" y="6" width="44" height="56" rx="6" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="2.5"/>
                <!-- Document Lines -->
                <line x1="12" y1="18" x2="30" y2="18" stroke="#4A6E91" stroke-width="2.5" stroke-linecap="round"/>
                <line x1="12" y1="26" x2="40" y2="26" stroke="#E2E8F0" stroke-width="2.5" stroke-linecap="round"/>
                <line x1="12" y1="34" x2="36" y2="34" stroke="#E2E8F0" stroke-width="2.5" stroke-linecap="round"/>
                <!-- Pulse Check Badge -->
                <circle cx="38" cy="46" r="14" fill="#6A8EAE"/>
                <path d="M 33 46 L 36 49 L 43 42" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
            </g>
            <!-- Brand Text -->
            <text x="64" y="32" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-weight="700" font-size="15" fill="#0F172A" letter-spacing="0.5">DISINFORMATION</text>
            <text x="64" y="48" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-weight="700" font-size="15" fill="#6A8EAE" letter-spacing="0.5">VERIFIER</text>
            <text x="64" y="62" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-weight="500" font-size="8.5" fill="#64748B" letter-spacing="1.2">FAST CLAIM AUDIT</text>
        </svg>
    </div>
    """
    st.sidebar.markdown(logo_svg, unsafe_allow_html=True)
