"""
Research display component for showing research results with citations.
"""

import streamlit as st
from typing import Dict, Any, Optional


# Educational descriptions for agent types
AGENT_TYPE_INFO = {
    "T0": {
        "name": "Static Automation",
        "short": "Rule-based, deterministic systems",
        "description": """**What it is:** Pre-programmed automation that follows fixed rules without learning or adaptation.

**Best for:** Simple, repetitive tasks with predictable outcomes where the rules are well-defined.

**Examples:** Scheduled reports, threshold-based alerts, simple data transformations.

**Key characteristics:**
- No learning capability
- Fully deterministic behavior
- Requires manual updates for changes
- Lowest complexity and risk""",
    },
    "T1": {
        "name": "Conversational Agent",
        "short": "Natural language interaction with basic context",
        "description": """**What it is:** AI that can understand and respond to natural language, maintaining basic conversation context.

**Best for:** Customer service, information retrieval, simple Q&A interfaces.

**Examples:** Chatbots, voice assistants, FAQ systems.

**Key characteristics:**
- Natural language understanding
- Session-based context memory
- Limited reasoning capability
- Human-like interaction pattern""",
    },
    "T2": {
        "name": "Procedural Workflow Agent",
        "short": "Multi-step task execution with tool integration",
        "description": """**What it is:** AI that can execute multi-step workflows, use external tools, and coordinate between systems.

**Best for:** Process automation, data pipeline orchestration, system integration tasks.

**Examples:** Automated data processing, multi-system workflows, report generation.

**Key characteristics:**
- Multi-step task execution
- Tool and API integration
- Error handling and recovery
- Structured workflow management""",
    },
    "T3": {
        "name": "Cognitive Autonomous Agent",
        "short": "Self-directed planning with learning and adaptation",
        "description": """**What it is:** AI that can plan its own actions, learn from experience, and adapt to changing conditions autonomously.

**Best for:** Complex decision-making, dynamic environments, situations requiring judgment and learning.

**Examples:** Predictive maintenance, autonomous optimization, adaptive control systems.

**Key characteristics:**
- Self-directed goal planning
- Learning from outcomes
- Adaptive behavior
- Requires careful governance and oversight""",
    },
    "T4": {
        "name": "Multi-Agent System (MAGS)",
        "short": "Collaborative AI with distributed coordination",
        "description": """**What it is:** Multiple AI agents working together, each with specialized roles, coordinating to achieve complex objectives.

**Best for:** Large-scale complex systems, scenarios requiring multiple specialized capabilities working in concert.

**Examples:** Smart grid management, autonomous fleet coordination, complex simulation systems.

**Key characteristics:**
- Multiple specialized agents
- Inter-agent communication
- Emergent collective behavior
- Highest complexity and capability""",
    },
}


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
    st.caption("Click each tab to view detailed findings. Expand sections for more detail.")

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
        render_research_area(
            research_areas.get("industry_adoption", {}),
            "Industry AI Adoption",
            "Current state of AI deployment in this industry, success rates, and adoption patterns."
        )

    with tabs[1]:
        render_research_area(
            research_areas.get("regulatory_environment", {}),
            "Regulatory Environment",
            "Relevant regulations, standards, and compliance requirements for AI systems."
        )

    with tabs[2]:
        render_research_area(
            research_areas.get("technical_integration", {}),
            "Technical Integration",
            "Common technology stacks, integration patterns, and technical challenges."
        )

    with tabs[3]:
        render_research_area(
            research_areas.get("risk_failure_modes", {}),
            "Risk & Failure Modes",
            "Documented failures, root causes, and risk factors to consider."
        )

    with tabs[4]:
        render_research_area(
            research_areas.get("economic_viability", {}),
            "Economic Viability",
            "ROI expectations, cost structures, and economic considerations."
        )

    # Full research report section
    if results.get("full_content"):
        st.divider()
        st.markdown("### 📄 Full Research Report")

        col1, col2 = st.columns([3, 1])
        with col1:
            st.caption("Download the complete research report for offline review or sharing.")
        with col2:
            # Download button
            st.download_button(
                label="⬇️ Download Report",
                data=results["full_content"],
                file_name="dtc_research_report.md",
                mime="text/markdown",
                use_container_width=True
            )

        with st.expander("📋 Preview Full Report", expanded=False):
            st.markdown(results["full_content"])

    # Sources section
    if results.get("sources"):
        render_sources(results["sources"])


def render_preliminary_assessment(assessment: Dict[str, Any]) -> None:
    """Render the preliminary assessment card.

    Args:
        assessment: Preliminary assessment data
    """
    st.markdown("### Preliminary Assessment")

    # Traffic Light Indicator - Large and prominent
    go_no_go = assessment.get("go_no_go", "pending")
    go_config = {
        "go": {"color": "#10B981", "bg": "#10B98130", "icon": "●", "label": "GO", "desc": "Research supports moving forward"},
        "caution": {"color": "#F59E0B", "bg": "#F59E0B30", "icon": "●", "label": "CAUTION", "desc": "Proceed with careful planning"},
        "no-go": {"color": "#EF4444", "bg": "#EF444430", "icon": "●", "label": "NO-GO", "desc": "Significant concerns identified"},
        "pending": {"color": "#6B7280", "bg": "#6B728030", "icon": "○", "label": "PENDING", "desc": "Awaiting analysis"},
    }
    config = go_config.get(go_no_go, go_config["pending"])

    # Traffic light style indicator
    st.markdown(f"""
    <div style="
        display: flex;
        align-items: center;
        gap: 20px;
        background: linear-gradient(135deg, {config['bg']}, transparent);
        border-left: 6px solid {config['color']};
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
    ">
        <div style="
            font-size: 4rem;
            color: {config['color']};
            line-height: 1;
            text-shadow: 0 0 20px {config['color']}40;
        ">{config['icon']}</div>
        <div>
            <div style="font-size: 1.5rem; font-weight: bold; color: {config['color']};">{config['label']}</div>
            <div style="color: #666;">{config['desc']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Three columns for agent type and confidence
    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        agent_type = assessment.get("recommended_type", "TBD")
        type_info = AGENT_TYPE_INFO.get(agent_type, {"name": "Unknown", "short": "Not determined"})

        st.markdown(f"""
        <div style="
            background-color: #3B82F615;
            border: 2px solid #3B82F6;
            border-radius: 8px;
            padding: 16px;
            text-align: center;
        ">
            <div style="font-size: 2rem; font-weight: bold; color: #3B82F6;">{agent_type}</div>
            <div style="font-weight: bold;">{type_info['name']}</div>
            <div style="font-size: 0.75rem; color: #666; margin-top: 4px;">{type_info['short']}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        confidence = assessment.get("confidence_level", "medium")
        conf_config = {
            "high": {"color": "#10B981", "desc": "Strong evidence available"},
            "medium": {"color": "#F59E0B", "desc": "Moderate evidence"},
            "low": {"color": "#EF4444", "desc": "Limited information"},
        }
        conf = conf_config.get(confidence, conf_config["medium"])

        st.markdown(f"""
        <div style="
            background-color: {conf['color']}15;
            border: 2px solid {conf['color']};
            border-radius: 8px;
            padding: 16px;
            text-align: center;
        ">
            <div style="font-size: 1.5rem; font-weight: bold; color: {conf['color']}; text-transform: uppercase;">{confidence}</div>
            <div style="font-weight: bold;">Confidence</div>
            <div style="font-size: 0.75rem; color: #666; margin-top: 4px;">{conf['desc']}</div>
        </div>
        """, unsafe_allow_html=True)

    # Agent type explanation (expandable)
    if agent_type in AGENT_TYPE_INFO:
        with st.expander(f"ℹ️ What is a {agent_type} ({AGENT_TYPE_INFO[agent_type]['name']})?", expanded=False):
            st.markdown(AGENT_TYPE_INFO[agent_type]['description'])

    # Recommendation Rationale - THE WHY
    st.markdown("---")
    st.markdown("#### Why This Recommendation?")

    rationale = assessment.get("recommendation_rationale", "")
    if rationale:
        st.markdown(f"""
        <div style="
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 16px;
            border-left: 4px solid {config['color']};
        ">
            {rationale}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Detailed rationale will be provided based on research findings.")

    # Key risks and success factors - with actual bullets
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##### ⚠️ Key Risk Factors")
        key_risks = assessment.get("key_risks", [])
        if key_risks:
            for risk in key_risks:
                st.markdown(f"""
                <div style="
                    display: flex;
                    align-items: flex-start;
                    gap: 8px;
                    margin-bottom: 8px;
                    padding: 8px;
                    background-color: #FEF2F2;
                    border-radius: 4px;
                ">
                    <span style="color: #EF4444;">✗</span>
                    <span style="color: #374151;">{risk}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.caption("_No specific risk factors extracted. Review detailed findings for risk information._")

    with col2:
        st.markdown("##### ✓ Critical Success Factors")
        success_factors = assessment.get("critical_success_factors", [])
        if success_factors:
            for factor in success_factors:
                st.markdown(f"""
                <div style="
                    display: flex;
                    align-items: flex-start;
                    gap: 8px;
                    margin-bottom: 8px;
                    padding: 8px;
                    background-color: #F0FDF4;
                    border-radius: 4px;
                ">
                    <span style="color: #10B981;">✓</span>
                    <span style="color: #374151;">{factor}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.caption("_No specific success factors extracted. Review detailed findings for guidance._")


def render_research_area(area: Dict[str, Any], title: str, description: str) -> None:
    """Render a single research area with summary and expandable full content.

    Args:
        area: Research area data
        title: Section title
        description: Section description
    """
    findings = area.get("findings", "")
    summary = area.get("summary", "")
    confidence = area.get("confidence", "medium")

    # Confidence indicator
    conf_colors = {"high": "#10B981", "medium": "#F59E0B", "low": "#EF4444"}
    conf_color = conf_colors.get(confidence, "#6B7280")

    st.markdown(f"""
    <div style="display: flex; align-items: center; margin-bottom: 12px; gap: 8px;">
        <span style="
            background-color: {conf_color};
            color: white;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.7rem;
            font-weight: bold;
        ">{confidence.upper()} CONFIDENCE</span>
    </div>
    """, unsafe_allow_html=True)

    st.caption(description)

    if summary or findings:
        # Display the summary prominently
        display_summary = summary if summary else (findings[:300] + "..." if len(findings) > 300 else findings)

        st.markdown(f"""
        <div style="
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 16px;
            margin: 12px 0;
            border-left: 3px solid {conf_color};
        ">
            <div style="font-weight: 500; margin-bottom: 8px; color: #374151;">Summary</div>
            <div style="color: #4B5563; line-height: 1.6;">{display_summary}</div>
        </div>
        """, unsafe_allow_html=True)

        # Show full content in expander if there's more to show
        if findings and len(findings) > len(display_summary) + 50:
            with st.expander("📖 View Full Analysis", expanded=False):
                st.markdown(findings)
    else:
        st.info(f"No detailed findings available for {title}. This section will be populated with research results.")


def render_sources(sources: list) -> None:
    """Render the sources section.

    Args:
        sources: List of source dictionaries with 'title' and 'url' keys
    """
    with st.expander("📚 Sources & Citations", expanded=False):
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
            st.caption("Sources will be listed here when available from research.")


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
    1. Check your Anthropic API key in the sidebar
    2. Verify network connectivity
    3. Try again in a few moments
    """)

    if st.button("Retry Research"):
        st.session_state.research_results = None
        st.rerun()
