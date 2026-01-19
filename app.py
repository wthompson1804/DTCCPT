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
from components.sidebar import render_sidebar
from components.progress import (
    render_progress_indicator,
    render_step_header,
    render_step_navigation
)
from components.input_form import render_input_form, render_input_summary


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

            if st.button("Start Deep Research", type="primary", use_container_width=True):
                with st.spinner("Conducting deep research... This may take a few minutes."):
                    # TODO: Integrate Open Deep Research in Phase 2
                    # For now, show placeholder
                    st.session_state.research_results = {
                        'status': 'placeholder',
                        'message': 'Deep research integration will be added in Phase 2',
                        'preliminary_type': 'T2'
                    }
                    st.rerun()
        else:
            # Show research results
            st.markdown("### Research Results")

            if st.session_state.research_results.get('status') == 'placeholder':
                st.info(
                    "Research integration pending. In the full implementation, "
                    "this will show cited research across all 5 areas with source URLs."
                )

                st.markdown(f"""
                **Preliminary Agent Type Recommendation:** {st.session_state.research_results.get('preliminary_type', 'TBD')}

                This recommendation will be refined based on deep research findings.
                """)
            else:
                # Display actual research results
                # TODO: Implement in Phase 2
                pass

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

        if st.button("Generate Requirements", type="primary", use_container_width=True):
            with st.spinner("Generating business requirements..."):
                # TODO: Integrate Claude API in Phase 3
                st.session_state.requirements_output = {
                    'status': 'placeholder',
                    'message': 'Requirements generation will be implemented in Phase 3'
                }
                st.rerun()
    else:
        # Show requirements output
        st.markdown("### Generated Requirements")

        if st.session_state.requirements_output.get('status') == 'placeholder':
            st.info(
                "Requirements generation pending. In the full implementation, "
                "this will display structured business requirements."
            )
        else:
            # Display actual requirements
            # TODO: Implement in Phase 3
            pass

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

    # Load agent types from config
    try:
        config = load_config()
        agent_types = config.get('agent_types', {})
    except Exception:
        agent_types = {}

    # Display agent type reference
    with st.expander("Agent Type Reference (T0-T4)", expanded=True):
        for type_id, type_info in agent_types.items():
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

        if st.button("Assess Agent Type", type="primary", use_container_width=True):
            with st.spinner("Assessing agent type and generating design..."):
                # TODO: Integrate Claude API in Phase 3
                st.session_state.agent_design_output = {
                    'status': 'placeholder',
                    'recommended_type': 'T2',
                    'message': 'Agent design will be implemented in Phase 3'
                }
                st.rerun()
    else:
        # Show agent design output
        st.markdown("### Agent Type Assessment")

        if st.session_state.agent_design_output.get('status') == 'placeholder':
            recommended = st.session_state.agent_design_output.get('recommended_type', 'T2')

            st.success(f"**Recommended Agent Type: {recommended}**")
            st.info(
                "Full agent design generation pending. In the full implementation, "
                "this will include detailed architecture recommendations."
            )

            # Human-in-the-loop confirmation
            st.markdown("### Confirm Agent Type")
            confirmed_type = st.selectbox(
                "Select or confirm the agent type for capability mapping:",
                options=['T0', 'T1', 'T2', 'T3', 'T4'],
                index=['T0', 'T1', 'T2', 'T3', 'T4'].index(recommended)
            )
            st.session_state.agent_design_output['confirmed_type'] = confirmed_type
        else:
            # Display actual design
            # TODO: Implement in Phase 3
            pass

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

        if st.button("Generate Capability Mapping", type="primary", use_container_width=True):
            with st.spinner("Mapping capabilities..."):
                # TODO: Integrate Claude API in Phase 3
                st.session_state.capability_mapping = {
                    'status': 'placeholder',
                    'message': 'Capability mapping will be implemented in Phase 3'
                }
                st.rerun()
    else:
        # Show capability mapping
        st.markdown("### Capability Mapping Results")

        if st.session_state.capability_mapping.get('status') == 'placeholder':
            st.info(
                "Capability mapping pending. In the full implementation, "
                "this will display an interactive periodic table visualization."
            )

            # Placeholder for periodic table
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
        else:
            # Display actual mapping
            # TODO: Implement in Phase 3 and Phase 4
            pass

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

    st.markdown("### Export Options")
    st.info("Export functionality will be available in Phase 4.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.button("Download PDF", disabled=True, use_container_width=True)
    with col2:
        st.button("Download DOCX", disabled=True, use_container_width=True)
    with col3:
        st.button("Download HTML Visualization", disabled=True, use_container_width=True)

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
            "Some features will be limited."
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
