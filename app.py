"""
DTC AI Agent Capability Assessment Tool

A Streamlit application for assessing AI agent capabilities using the
Digital Twin Consortium's Capabilities Periodic Table (CPT) framework.

This tool:
1. Conducts deep research on industry/regulatory context (Enhanced Step 0)
2. Generates business requirements (Step 1)
3. Assesses agent type (T0-T4) and designs architecture (Step 2)
4. Maps capabilities to the 45-capability CPT (Step 3)
"""

import streamlit as st
from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import modules
from modules.data_loader import load_config, load_capabilities, load_prompt
from modules.research import conduct_research, format_research_for_display
from modules.requirements import generate_requirements, format_requirements_for_display
from modules.agent_design import generate_agent_design, format_agent_design_for_display, AGENT_TYPE_CRITERIA
from modules.capability_mapping import generate_capability_mapping, format_capability_mapping_for_display

# Import components
from components.sidebar import render_sidebar
from components.progress import (
    render_progress_indicator,
    render_step_header,
    render_step_navigation
)
from components.input_form import render_input_form, render_input_summary
from components.research_display import render_research_results, render_research_error


# Page configuration
st.set_page_config(
    page_title="DTC AI Agent Capability Assessment",
    page_icon=":robot_face:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #6B7280;
        margin-bottom: 2rem;
    }
    .capability-card {
        border: 1px solid #E5E7EB;
        border-radius: 8px;
        padding: 16px;
        margin: 8px 0;
    }
    .step-container {
        background-color: #F9FAFB;
        border-radius: 12px;
        padding: 24px;
        margin: 16px 0;
    }
    .citation {
        font-size: 0.85rem;
        color: #6B7280;
        border-left: 3px solid #3B82F6;
        padding-left: 12px;
        margin: 8px 0;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables."""
    defaults = {
        'current_step': 0,
        'form_data': None,
        'research_results': None,
        'requirements_output': None,
        'agent_design_output': None,
        'capability_mapping': None,
        'assessment_complete': False,
        'show_export': False,
    }

    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value


def check_api_key() -> bool:
    """Check if the Anthropic API key is configured."""
    api_key = os.getenv('ANTHROPIC_API_KEY', '')
    return api_key.startswith('sk-ant-')


def render_step_0_research():
    """Render Step 0: Research phase."""
    render_step_header(
        0,
        "Industry & Regulatory Research",
        "Conduct comprehensive research to ground the assessment in current, cited intelligence"
    )

    if st.session_state.form_data is None:
        # Show input form
        submitted, form_data = render_input_form()

        if submitted:
            st.session_state.form_data = form_data
            st.rerun()
    else:
        # Show input summary and research controls
        render_input_summary(st.session_state.form_data)

        st.divider()

        if st.session_state.research_results is None:
            # Research not yet started
            st.markdown("### Ready to Research")
            st.markdown(
                "Click below to conduct deep research on your use case. "
                "This will analyze 5 key areas:"
            )

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                - **Industry AI Adoption** - Current deployment rates, case studies
                - **Regulatory Environment** - Relevant standards and requirements
                - **Technical Integration** - Common stacks, patterns, challenges
                """)
            with col2:
                st.markdown("""
                - **Risk & Failure Modes** - Documented failures, root causes
                - **Economic Viability** - ROI data, cost structures
                """)

            if not check_api_key():
                st.warning("Anthropic API key required for research. Please configure ANTHROPIC_API_KEY.")
                if st.button("Skip Research (Demo Mode)", use_container_width=True):
                    st.session_state.research_results = {
                        'status': 'demo',
                        'summary': {
                            'industry': st.session_state.form_data.get('industry'),
                            'use_case': st.session_state.form_data.get('use_case'),
                            'jurisdiction': st.session_state.form_data.get('jurisdiction'),
                        },
                        'preliminary_assessment': {
                            'go_no_go': 'caution',
                            'recommended_type': 'T2',
                            'confidence_level': 'medium',
                            'key_risks': ['Demo mode - no actual research conducted'],
                            'critical_success_factors': ['Configure API key for real research'],
                        },
                        'research_areas': {
                            'industry_adoption': {'name': 'Industry AI Adoption', 'findings': 'Demo mode - configure API for actual research', 'confidence': 'low'},
                            'regulatory_environment': {'name': 'Regulatory Environment', 'findings': 'Demo mode - configure API for actual research', 'confidence': 'low'},
                            'technical_integration': {'name': 'Technical Integration', 'findings': 'Demo mode - configure API for actual research', 'confidence': 'low'},
                            'risk_failure_modes': {'name': 'Risk & Failure Modes', 'findings': 'Demo mode - configure API for actual research', 'confidence': 'low'},
                            'economic_viability': {'name': 'Economic Viability', 'findings': 'Demo mode - configure API for actual research', 'confidence': 'low'},
                        },
                        'sources': [],
                    }
                    st.rerun()
            else:
                if st.button("Start Deep Research", type="primary", use_container_width=True):
                    with st.spinner("Conducting deep research... This may take 1-2 minutes."):
                        try:
                            result = conduct_research(
                                industry=st.session_state.form_data.get('industry', ''),
                                use_case=st.session_state.form_data.get('use_case', ''),
                                jurisdiction=st.session_state.form_data.get('jurisdiction', ''),
                                organization_size=st.session_state.form_data.get('organization_size', 'Enterprise'),
                                timeline=st.session_state.form_data.get('timeline', 'Pilot Project'),
                            )
                            st.session_state.research_results = format_research_for_display(result)
                        except Exception as e:
                            st.session_state.research_results = {
                                'status': 'error',
                                'error': str(e),
                            }
                        st.rerun()
        else:
            # Show research results
            st.markdown("### Research Results")

            if st.session_state.research_results.get('error'):
                render_research_error(st.session_state.research_results['error'])
            elif st.session_state.research_results.get('status') == 'demo':
                st.warning("Running in demo mode. Configure ANTHROPIC_API_KEY for actual research.")
                render_research_results(st.session_state.research_results)
            else:
                render_research_results(st.session_state.research_results)

            # Navigation
            render_step_navigation(
                current_step=0,
                can_proceed=True,
                show_confirmation=True
            )


def render_step_1_requirements():
    """Render Step 1: Business Requirements Generation."""
    render_step_header(
        1,
        "Business Requirements",
        "Extract comprehensive business requirements based on research and use case context"
    )

    render_input_summary(st.session_state.form_data)

    st.divider()

    if st.session_state.requirements_output is None:
        st.markdown("### Generate Requirements")
        st.markdown(
            "This step will analyze your use case and research findings to generate "
            "detailed business requirements following the DTC methodology."
        )

        # Show the DTC prompt being used (collapsed)
        with st.expander("View DTC Prompt Template", expanded=False):
            try:
                prompt = load_prompt(1)
                st.code(prompt[:2000] + "..." if len(prompt) > 2000 else prompt, language="markdown")
            except FileNotFoundError:
                st.warning("Prompt template not found")

        if not check_api_key():
            st.warning("Anthropic API key required. Please configure ANTHROPIC_API_KEY.")
            if st.button("Skip Requirements (Demo Mode)", use_container_width=True):
                st.session_state.requirements_output = {
                    'status': 'demo',
                    'full_text': '## Demo Mode\n\nConfigure ANTHROPIC_API_KEY to generate actual requirements.\n\n### Sample Requirements\n- REQ-01: System shall provide AI agent capabilities\n- REQ-02: System shall integrate with existing infrastructure',
                    'sections': {},
                }
                st.rerun()
        else:
            if st.button("Generate Requirements", type="primary", use_container_width=True):
                with st.spinner("Generating business requirements..."):
                    try:
                        result = generate_requirements(
                            form_data=st.session_state.form_data,
                            research_results=st.session_state.research_results or {},
                        )
                        st.session_state.requirements_output = format_requirements_for_display(result)
                    except Exception as e:
                        st.session_state.requirements_output = {
                            'status': 'error',
                            'error': str(e),
                        }
                    st.rerun()
    else:
        # Show requirements output
        st.markdown("### Generated Requirements")

        if st.session_state.requirements_output.get('error'):
            st.error(f"Error: {st.session_state.requirements_output['error']}")
        elif st.session_state.requirements_output.get('status') == 'demo':
            st.warning("Running in demo mode. Configure ANTHROPIC_API_KEY for actual requirements.")
            st.markdown(st.session_state.requirements_output.get('full_text', ''))
        else:
            # Display requirements
            st.markdown(st.session_state.requirements_output.get('full_text', ''))

        render_step_navigation(
            current_step=1,
            can_proceed=True,
            show_confirmation=True
        )


def render_step_2_agent_design():
    """Render Step 2: Agent Type Assessment and Design."""
    render_step_header(
        2,
        "Agent Type Assessment",
        "Assess the appropriate agent type (T0-T4) and design the agent architecture"
    )

    # Display agent type reference
    with st.expander("Agent Type Reference (T0-T4)", expanded=True):
        for type_id, type_info in AGENT_TYPE_CRITERIA.items():
            st.markdown(f"**{type_id}: {type_info.get('name', '')}** - {type_info.get('description', '')}")

    st.divider()

    if st.session_state.agent_design_output is None:
        st.markdown("### Assess Agent Type")

        # Show the DTC prompt being used (collapsed)
        with st.expander("View DTC Prompt Template", expanded=False):
            try:
                prompt = load_prompt(2)
                st.code(prompt[:2000] + "..." if len(prompt) > 2000 else prompt, language="markdown")
            except FileNotFoundError:
                st.warning("Prompt template not found")

        if not check_api_key():
            st.warning("Anthropic API key required. Please configure ANTHROPIC_API_KEY.")
            if st.button("Skip Assessment (Demo Mode)", use_container_width=True):
                st.session_state.agent_design_output = {
                    'status': 'demo',
                    'recommended_type': 'T2',
                    'confirmed_type': None,
                    'type_info': AGENT_TYPE_CRITERIA.get('T2', {}),
                    'justification': 'Demo mode - configure API for actual assessment',
                    'architecture_summary': 'Demo mode - configure API for actual architecture',
                    'full_document': '## Demo Mode\n\nConfigure ANTHROPIC_API_KEY for actual agent design.',
                }
                st.rerun()
        else:
            if st.button("Assess Agent Type", type="primary", use_container_width=True):
                with st.spinner("Assessing agent type and generating design..."):
                    try:
                        result = generate_agent_design(
                            form_data=st.session_state.form_data,
                            research_results=st.session_state.research_results or {},
                            requirements_output=st.session_state.requirements_output or {},
                        )
                        st.session_state.agent_design_output = format_agent_design_for_display(result)
                    except Exception as e:
                        st.session_state.agent_design_output = {
                            'status': 'error',
                            'error': str(e),
                        }
                    st.rerun()
    else:
        # Show agent design output
        st.markdown("### Agent Type Assessment")

        if st.session_state.agent_design_output.get('error'):
            st.error(f"Error: {st.session_state.agent_design_output['error']}")
        else:
            recommended = st.session_state.agent_design_output.get('recommended_type', 'T2')
            type_info = st.session_state.agent_design_output.get('type_info', {})

            col1, col2 = st.columns([1, 2])

            with col1:
                st.markdown(f"""
                <div style="
                    background-color: #3B82F620;
                    border: 3px solid #3B82F6;
                    border-radius: 12px;
                    padding: 24px;
                    text-align: center;
                ">
                    <div style="font-size: 3rem; font-weight: bold; color: #3B82F6;">{recommended}</div>
                    <div style="font-size: 1.1rem; font-weight: bold;">{type_info.get('name', '')}</div>
                    <div style="font-size: 0.9rem; color: #6B7280; margin-top: 8px;">Recommended Type</div>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"**Description:** {type_info.get('description', '')}")

                if st.session_state.agent_design_output.get('justification'):
                    st.markdown("**Justification:**")
                    st.markdown(st.session_state.agent_design_output['justification'])

            # Human-in-the-loop confirmation
            st.divider()
            st.markdown("### Confirm Agent Type")
            st.markdown("Review the recommendation and confirm or adjust the agent type before proceeding.")

            confirmed_type = st.selectbox(
                "Select or confirm the agent type for capability mapping:",
                options=['T0', 'T1', 'T2', 'T3', 'T4'],
                index=['T0', 'T1', 'T2', 'T3', 'T4'].index(recommended),
                key="agent_type_selector"
            )
            st.session_state.agent_design_output['confirmed_type'] = confirmed_type

            # Show full design document
            with st.expander("View Full Design Document", expanded=False):
                st.markdown(st.session_state.agent_design_output.get('full_document', ''))

        render_step_navigation(
            current_step=2,
            can_proceed=True,
            show_confirmation=True
        )


def render_step_3_capability_mapping():
    """Render Step 3: Capability Mapping."""
    render_step_header(
        3,
        "Capability Mapping",
        "Map requirements to the 45-capability CPT and generate visualization"
    )

    # Load capabilities
    try:
        capabilities = load_capabilities()
        cap_count = sum(
            len(cat.get('capabilities', {}))
            for cat in capabilities.get('capabilities', {}).values()
        )
        st.info(f"Loaded {cap_count} capabilities from DTC CPT framework")
    except Exception as e:
        st.error(f"Error loading capabilities: {e}")
        capabilities = None

    st.divider()

    if st.session_state.capability_mapping is None:
        st.markdown("### Generate Capability Mapping")

        # Show the DTC prompt being used (collapsed)
        with st.expander("View DTC Prompt Template", expanded=False):
            try:
                prompt = load_prompt(3)
                st.code(prompt[:2000] + "..." if len(prompt) > 2000 else prompt, language="markdown")
            except FileNotFoundError:
                st.warning("Prompt template not found")

        if not check_api_key():
            st.warning("Anthropic API key required. Please configure ANTHROPIC_API_KEY.")
            if st.button("Skip Mapping (Demo Mode)", use_container_width=True):
                st.session_state.capability_mapping = {
                    'status': 'demo',
                    'agent_type': st.session_state.agent_design_output.get('confirmed_type', 'T2') if st.session_state.agent_design_output else 'T2',
                    'total_mapped': 0,
                    'essential_count': 0,
                    'advanced_count': 0,
                    'optional_count': 0,
                    'mappings': [],
                    'full_document': '## Demo Mode\n\nConfigure ANTHROPIC_API_KEY for actual capability mapping.',
                    'html_visualization': '<html><body><h1>Demo Mode</h1><p>Configure API key for visualization.</p></body></html>',
                }
                st.rerun()
        else:
            if st.button("Generate Capability Mapping", type="primary", use_container_width=True):
                with st.spinner("Mapping capabilities... This may take 1-2 minutes."):
                    try:
                        result = generate_capability_mapping(
                            form_data=st.session_state.form_data,
                            research_results=st.session_state.research_results or {},
                            requirements_output=st.session_state.requirements_output or {},
                            agent_design_output=st.session_state.agent_design_output or {},
                        )
                        st.session_state.capability_mapping = format_capability_mapping_for_display(result)
                    except Exception as e:
                        st.session_state.capability_mapping = {
                            'status': 'error',
                            'error': str(e),
                        }
                    st.rerun()
    else:
        # Show capability mapping
        st.markdown("### Capability Mapping Results")

        if st.session_state.capability_mapping.get('error'):
            st.error(f"Error: {st.session_state.capability_mapping['error']}")
        else:
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "Total Mapped",
                    st.session_state.capability_mapping.get('total_mapped', 0)
                )
            with col2:
                st.metric(
                    "Essential",
                    st.session_state.capability_mapping.get('essential_count', 0)
                )
            with col3:
                st.metric(
                    "Advanced",
                    st.session_state.capability_mapping.get('advanced_count', 0)
                )
            with col4:
                st.metric(
                    "Optional",
                    st.session_state.capability_mapping.get('optional_count', 0)
                )

            st.divider()

            # Capability categories visualization
            st.markdown("#### Capability Categories")
            try:
                config = load_config()
                categories = config.get('categories', {})

                cols = st.columns(3)
                for i, (cat_id, cat_info) in enumerate(categories.items()):
                    with cols[i % 3]:
                        color = cat_info.get('color', '#6B7280')
                        st.markdown(
                            f"""<div style="
                                background-color: {color}20;
                                border-left: 4px solid {color};
                                padding: 12px;
                                margin: 8px 0;
                                border-radius: 4px;
                            ">
                            <strong>{cat_id}</strong>: {cat_info.get('name', '')}
                            </div>""",
                            unsafe_allow_html=True
                        )
            except Exception:
                pass

            # Mapped capabilities list
            if st.session_state.capability_mapping.get('mappings'):
                st.markdown("#### Mapped Capabilities")

                for mapping in st.session_state.capability_mapping['mappings'][:20]:  # Show first 20
                    priority_colors = {
                        'essential': '#10B981',
                        'high': '#3B82F6',
                        'medium': '#F59E0B',
                        'optional': '#9CA3AF',
                    }
                    color = priority_colors.get(mapping.get('priority', 'medium'), '#6B7280')

                    st.markdown(
                        f"""<div style="
                            display: flex;
                            align-items: center;
                            padding: 8px 12px;
                            margin: 4px 0;
                            background: #F9FAFB;
                            border-radius: 6px;
                        ">
                            <span style="
                                background: {color};
                                color: white;
                                padding: 2px 8px;
                                border-radius: 4px;
                                font-size: 0.75rem;
                                margin-right: 12px;
                            ">{mapping.get('priority', 'medium').upper()}</span>
                            <strong>{mapping.get('id', '')}</strong>: {mapping.get('name', '')}
                        </div>""",
                        unsafe_allow_html=True
                    )

            # Full document
            with st.expander("View Full Mapping Document", expanded=False):
                st.markdown(st.session_state.capability_mapping.get('full_document', ''))

            # HTML Preview
            if st.session_state.capability_mapping.get('html_visualization'):
                with st.expander("Preview HTML Visualization", expanded=False):
                    st.components.v1.html(
                        st.session_state.capability_mapping['html_visualization'],
                        height=600,
                        scrolling=True
                    )

        render_step_navigation(
            current_step=3,
            can_proceed=True,
            show_confirmation=True,
            next_label="Complete Assessment"
        )


def render_completion():
    """Render the assessment completion screen."""
    st.balloons()

    st.markdown("## Assessment Complete!")
    st.success("Your AI Agent Capability Assessment has been generated.")

    # Summary
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Industry", st.session_state.form_data.get('industry', 'N/A'))

    with col2:
        agent_type = 'N/A'
        if st.session_state.agent_design_output:
            agent_type = st.session_state.agent_design_output.get(
                'confirmed_type',
                st.session_state.agent_design_output.get('recommended_type', 'N/A')
            )
        st.metric("Agent Type", agent_type)

    with col3:
        cap_count = 0
        if st.session_state.capability_mapping:
            cap_count = st.session_state.capability_mapping.get('total_mapped', 0)
        st.metric("Capabilities Mapped", cap_count)

    st.divider()

    st.markdown("### Export Options")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.session_state.capability_mapping and st.session_state.capability_mapping.get('full_document'):
            st.download_button(
                "Download Mapping (MD)",
                data=st.session_state.capability_mapping['full_document'],
                file_name="capability_mapping.md",
                mime="text/markdown",
                use_container_width=True
            )
        else:
            st.button("Download Mapping (MD)", disabled=True, use_container_width=True)

    with col2:
        if st.session_state.capability_mapping and st.session_state.capability_mapping.get('html_visualization'):
            st.download_button(
                "Download HTML Visualization",
                data=st.session_state.capability_mapping['html_visualization'],
                file_name="cpt_visualization.html",
                mime="text/html",
                use_container_width=True
            )
        else:
            st.button("Download HTML Visualization", disabled=True, use_container_width=True)

    with col3:
        # Complete package
        if st.session_state.capability_mapping:
            package = f"""# DTC AI Agent Capability Assessment

## Use Case
**Industry:** {st.session_state.form_data.get('industry', 'N/A')}
**Jurisdiction:** {st.session_state.form_data.get('jurisdiction', 'N/A')}

### Description
{st.session_state.form_data.get('use_case', 'N/A')}

---

## Research Findings
{st.session_state.research_results.get('research_areas', {}).get('industry_adoption', {}).get('findings', 'N/A') if st.session_state.research_results else 'N/A'}

---

## Requirements
{st.session_state.requirements_output.get('full_text', 'N/A') if st.session_state.requirements_output else 'N/A'}

---

## Agent Design
**Recommended Type:** {agent_type}

{st.session_state.agent_design_output.get('full_document', 'N/A') if st.session_state.agent_design_output else 'N/A'}

---

## Capability Mapping
{st.session_state.capability_mapping.get('full_document', 'N/A')}
"""
            st.download_button(
                "Download Complete Package",
                data=package,
                file_name="dtc_assessment_complete.md",
                mime="text/markdown",
                use_container_width=True,
                type="primary"
            )
        else:
            st.button("Download Complete Package", disabled=True, use_container_width=True)

    st.divider()

    if st.button("Start New Assessment", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


def main():
    """Main application entry point."""
    # Initialize
    initialize_session_state()

    # Load configuration
    try:
        config = load_config()
    except Exception as e:
        st.error(f"Error loading configuration: {e}")
        config = {}

    # Render sidebar
    render_sidebar(config)

    # Main content area
    st.markdown('<div class="main-header">DTC AI Agent Capability Assessment</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">Ground your AI agent planning in current research using the Digital Twin Consortium methodology</div>',
        unsafe_allow_html=True
    )

    # Check API key
    if not check_api_key():
        st.warning(
            "Anthropic API key not configured. Please set ANTHROPIC_API_KEY in your environment. "
            "Demo mode available with limited functionality."
        )

    # Progress indicator
    render_progress_indicator(st.session_state.current_step)

    st.divider()

    # Render current step
    if st.session_state.assessment_complete:
        render_completion()
    elif st.session_state.current_step == 0:
        render_step_0_research()
    elif st.session_state.current_step == 1:
        render_step_1_requirements()
    elif st.session_state.current_step == 2:
        render_step_2_agent_design()
    elif st.session_state.current_step == 3:
        render_step_3_capability_mapping()


if __name__ == "__main__":
    main()
