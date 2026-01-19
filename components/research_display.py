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

    # Full research content (expandable)
    if results.get("full_content"):
        with st.expander("View Complete Research Report", expanded=False):
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
    st.caption("Based on research analysis. Review the detailed findings below for supporting evidence.")

    col1, col2, col3 = st.columns(3)

    with col1:
        go_no_go = assessment.get("go_no_go", "pending")
        go_config = {
            "go": {"color": "#10B981", "icon": "✓", "label": "PROCEED", "desc": "Research supports moving forward"},
            "caution": {"color": "#F59E0B", "icon": "⚠", "label": "CAUTION", "desc": "Proceed with careful planning"},
            "no-go": {"color": "#EF4444", "icon": "✗", "label": "NOT RECOMMENDED", "desc": "Significant concerns identified"},
            "pending": {"color": "#6B7280", "icon": "⏳", "label": "PENDING", "desc": "Awaiting analysis"},
        }
        config = go_config.get(go_no_go, go_config["pending"])

        st.markdown(f"""
        <div style="
            background-color: {config['color']}15;
            border: 2px solid {config['color']};
            border-radius: 8px;
            padding: 16px;
            text-align: center;
        ">
            <div style="font-size: 2.5rem;">{config['icon']}</div>
            <div style="font-weight: bold; color: {config['color']};">{config['label']}</div>
            <div style="font-size: 0.75rem; color: #666; margin-top: 4px;">{config['desc']}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
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

    with col3:
        confidence = assessment.get("confidence_level", "medium")
        conf_config = {
            "high": {"color": "#10B981", "desc": "Strong evidence available"},
            "medium": {"color": "#F59E0B", "desc": "Moderate evidence"},
            "low": {"color": "#EF4444", "desc": "Limited information"},
        }
        config = conf_config.get(confidence, conf_config["medium"])

        st.markdown(f"""
        <div style="
            background-color: {config['color']}15;
            border: 2px solid {config['color']};
            border-radius: 8px;
            padding: 16px;
            text-align: center;
        ">
            <div style="font-size: 1.5rem; font-weight: bold; color: {config['color']}; text-transform: uppercase;">{confidence}</div>
            <div style="font-weight: bold;">Confidence</div>
            <div style="font-size: 0.75rem; color: #666; margin-top: 4px;">{config['desc']}</div>
        </div>
        """, unsafe_allow_html=True)

    # Agent type explanation (expandable)
    if agent_type in AGENT_TYPE_INFO:
        with st.expander(f"What is a {agent_type} ({AGENT_TYPE_INFO[agent_type]['name']})?", expanded=False):
            st.markdown(AGENT_TYPE_INFO[agent_type]['description'])

    # Key risks and success factors
    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**⚠️ Key Risk Factors**")
        if assessment.get("key_risks"):
            for risk in assessment["key_risks"]:
                st.markdown(f"- {risk}")
        else:
            st.caption("_Risk factors identified in detailed findings below_")

    with col2:
        st.markdown("**✓ Critical Success Factors**")
        if assessment.get("critical_success_factors"):
            for factor in assessment["critical_success_factors"]:
                st.markdown(f"- {factor}")
        else:
            st.caption("_Success factors identified in detailed findings below_")


def render_research_area(area: Dict[str, Any], title: str, description: str) -> None:
    """Render a single research area with expandable details.

    Args:
        area: Research area data
        title: Section title
        description: Section description
    """
    findings = area.get("findings", "")
    confidence = area.get("confidence", "medium")

    # Confidence indicator
    conf_colors = {"high": "#10B981", "medium": "#F59E0B", "low": "#EF4444"}
    conf_color = conf_colors.get(confidence, "#6B7280")

    st.markdown(f"""
    <div style="display: flex; align-items: center; margin-bottom: 8px; gap: 8px;">
        <span style="
            background-color: {conf_color};
            color: white;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.7rem;
            font-weight: bold;
        ">{confidence.upper()}</span>
        <span style="font-size: 0.85rem; color: #666;">{description}</span>
    </div>
    """, unsafe_allow_html=True)

    if findings and len(findings) > 50:
        # Show summary (first paragraph or first 300 chars)
        summary = findings.split('\n\n')[0] if '\n\n' in findings else findings[:300]
        if len(findings) > len(summary) + 50:
            st.markdown(summary + "...")
            with st.expander("Read full analysis", expanded=False):
                st.markdown(findings)
        else:
            st.markdown(findings)
    elif findings:
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
