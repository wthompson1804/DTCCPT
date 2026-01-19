"""
Research display component for showing research results with citations.
"""

import streamlit as st
from typing import Dict, Any, Optional


def render_research_results(results: Dict[str, Any]) -> None:
    """Render the complete research results.

    Args:
        results: Formatted research results from format_research_for_display()
    """
    if results.get("error"):
        st.error(f"Research Error: {results['error']}")
        return

    # Preliminary Assessment Card
    render_preliminary_assessment(results.get("preliminary_assessment", {}))

    st.divider()

    # Research Areas
    st.markdown("### Research Findings")

    research_areas = results.get("research_areas", {})

    # Create tabs for each research area
    tabs = st.tabs([
        "Industry Adoption",
        "Regulatory",
        "Technical",
        "Risk & Failure",
        "Economic"
    ])

    with tabs[0]:
        render_research_area(research_areas.get("industry_adoption", {}))

    with tabs[1]:
        render_research_area(research_areas.get("regulatory_environment", {}))

    with tabs[2]:
        render_research_area(research_areas.get("technical_integration", {}))

    with tabs[3]:
        render_research_area(research_areas.get("risk_failure_modes", {}))

    with tabs[4]:
        render_research_area(research_areas.get("economic_viability", {}))

    # Sources section
    if results.get("sources"):
        render_sources(results["sources"])


def render_preliminary_assessment(assessment: Dict[str, Any]) -> None:
    """Render the preliminary assessment card.

    Args:
        assessment: Preliminary assessment data
    """
    st.markdown("### Preliminary Assessment")

    col1, col2, col3 = st.columns(3)

    with col1:
        go_no_go = assessment.get("go_no_go", "pending")
        go_colors = {
            "go": ("green", ":white_check_mark:"),
            "caution": ("orange", ":warning:"),
            "no-go": ("red", ":x:"),
            "pending": ("gray", ":hourglass:")
        }
        color, icon = go_colors.get(go_no_go, ("gray", ":question:"))

        st.markdown(f"""
        <div style="
            background-color: {color}20;
            border: 2px solid {color};
            border-radius: 8px;
            padding: 16px;
            text-align: center;
        ">
            <div style="font-size: 2rem;">{icon}</div>
            <div style="font-weight: bold; text-transform: uppercase;">{go_no_go}</div>
            <div style="font-size: 0.8rem; color: #666;">Recommendation</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        agent_type = assessment.get("recommended_type", "TBD")
        type_names = {
            "T0": "Static Automation",
            "T1": "Conversational Agent",
            "T2": "Procedural Workflow",
            "T3": "Cognitive Autonomous",
            "T4": "Multi-Agent System"
        }
        type_name = type_names.get(agent_type, "Unknown")

        st.markdown(f"""
        <div style="
            background-color: #3B82F620;
            border: 2px solid #3B82F6;
            border-radius: 8px;
            padding: 16px;
            text-align: center;
        ">
            <div style="font-size: 2rem; font-weight: bold;">{agent_type}</div>
            <div style="font-weight: bold;">{type_name}</div>
            <div style="font-size: 0.8rem; color: #666;">Recommended Type</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        confidence = assessment.get("confidence_level", "medium")
        conf_colors = {
            "high": "green",
            "medium": "orange",
            "low": "red"
        }
        conf_color = conf_colors.get(confidence, "gray")

        st.markdown(f"""
        <div style="
            background-color: {conf_color}20;
            border: 2px solid {conf_color};
            border-radius: 8px;
            padding: 16px;
            text-align: center;
        ">
            <div style="font-size: 2rem; text-transform: uppercase;">{confidence}</div>
            <div style="font-weight: bold;">Confidence</div>
            <div style="font-size: 0.8rem; color: #666;">Research Quality</div>
        </div>
        """, unsafe_allow_html=True)

    # Key risks and success factors
    col1, col2 = st.columns(2)

    with col1:
        if assessment.get("key_risks"):
            st.markdown("**Key Risk Factors:**")
            for risk in assessment["key_risks"]:
                st.markdown(f"- :warning: {risk}")
        else:
            st.info("Risk factors will be identified during detailed research.")

    with col2:
        if assessment.get("critical_success_factors"):
            st.markdown("**Critical Success Factors:**")
            for factor in assessment["critical_success_factors"]:
                st.markdown(f"- :white_check_mark: {factor}")
        else:
            st.info("Success factors will be identified during detailed research.")


def render_research_area(area: Dict[str, Any]) -> None:
    """Render a single research area.

    Args:
        area: Research area data
    """
    name = area.get("name", "Research Area")
    findings = area.get("findings", "")
    confidence = area.get("confidence", "medium")

    # Confidence indicator
    conf_colors = {"high": "green", "medium": "orange", "low": "red"}
    conf_color = conf_colors.get(confidence, "gray")

    st.markdown(f"""
    <div style="display: flex; align-items: center; margin-bottom: 8px;">
        <span style="
            background-color: {conf_color};
            color: white;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.75rem;
            margin-right: 8px;
        ">{confidence.upper()} CONFIDENCE</span>
    </div>
    """, unsafe_allow_html=True)

    if findings:
        st.markdown(findings)
    else:
        st.info(f"No findings available for {name}. Run deep research to populate this section.")


def render_sources(sources: list) -> None:
    """Render the sources section.

    Args:
        sources: List of source dictionaries with 'title' and 'url' keys
    """
    with st.expander("Sources & Citations", expanded=False):
        if sources:
            for source in sources:
                title = source.get("title", "Untitled")
                url = source.get("url", "")
                date = source.get("date", "")

                if url:
                    st.markdown(f"- [{title}]({url}) {f'({date})' if date else ''}")
                else:
                    st.markdown(f"- {title} {f'({date})' if date else ''}")
        else:
            st.info("Sources will be listed here after research is complete.")


def render_research_loading() -> None:
    """Render a loading state for research in progress."""
    st.markdown("### Conducting Deep Research")

    progress_text = st.empty()
    progress_bar = st.progress(0)

    research_steps = [
        "Analyzing industry AI adoption patterns...",
        "Reviewing regulatory environment...",
        "Evaluating technical integration requirements...",
        "Identifying risk and failure modes...",
        "Assessing economic viability...",
        "Synthesizing findings..."
    ]

    for i, step in enumerate(research_steps):
        progress_text.markdown(f"*{step}*")
        progress_bar.progress((i + 1) / len(research_steps))

    return progress_text, progress_bar


def render_research_error(error_message: str) -> None:
    """Render an error state for failed research.

    Args:
        error_message: Error message to display
    """
    st.error("Research Failed")

    st.markdown(f"""
    <div style="
        background-color: #FEE2E2;
        border: 1px solid #EF4444;
        border-radius: 8px;
        padding: 16px;
        margin: 16px 0;
    ">
        <strong>Error:</strong> {error_message}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    **Possible causes:**
    - API key not configured or invalid
    - Network connectivity issues
    - Rate limiting

    **Suggested actions:**
    1. Check your ANTHROPIC_API_KEY environment variable
    2. Verify network connectivity
    3. Try again in a few moments
    """)

    if st.button("Retry Research"):
        st.session_state.research_results = None
        st.rerun()
