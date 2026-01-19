"""
Input form component for collecting use case information.
"""

import streamlit as st
from typing import Dict, Any, Optional, Tuple


# Common industries for suggestions
INDUSTRIES = [
    "Energy & Utilities",
    "Manufacturing",
    "Healthcare",
    "Transportation & Logistics",
    "Agriculture",
    "Construction",
    "Mining & Resources",
    "Oil & Gas",
    "Water Management",
    "Smart Cities",
    "Aerospace & Defense",
    "Financial Services",
    "Telecommunications",
    "Retail & Supply Chain",
    "Other"
]

# Common jurisdictions
JURISDICTIONS = [
    "United States",
    "European Union",
    "United Kingdom",
    "Canada",
    "Australia",
    "Germany",
    "Japan",
    "Singapore",
    "China",
    "India",
    "Brazil",
    "Multi-jurisdictional",
    "Other"
]


def render_input_form() -> Tuple[bool, Dict[str, Any]]:
    """Render the input form for collecting use case information.

    Returns:
        Tuple of (form_submitted, form_data)
    """
    st.markdown("### Define Your Use Case")
    st.markdown(
        "Provide information about your AI agent implementation to enable "
        "targeted research and accurate capability assessment."
    )

    with st.form("use_case_form"):
        # Industry selection
        col1, col2 = st.columns(2)

        with col1:
            industry_select = st.selectbox(
                "Industry Sector",
                options=INDUSTRIES,
                help="Select the primary industry for your AI agent deployment"
            )

        with col2:
            if industry_select == "Other":
                industry = st.text_input(
                    "Specify Industry",
                    placeholder="Enter your industry"
                )
            else:
                industry = industry_select

        # Use case description
        use_case = st.text_area(
            "Use Case Description",
            placeholder=(
                "Describe what you want your AI agent to do. Include:\n"
                "- Primary function or task\n"
                "- Key interactions (with humans, systems, physical equipment)\n"
                "- Expected outcomes or decisions\n"
                "- Any specific constraints or requirements"
            ),
            height=150,
            help="Be specific about the AI agent's role and responsibilities"
        )

        # Jurisdiction
        col3, col4 = st.columns(2)

        with col3:
            jurisdiction_select = st.selectbox(
                "Primary Jurisdiction",
                options=JURISDICTIONS,
                help="Select the primary regulatory jurisdiction"
            )

        with col4:
            if jurisdiction_select == "Other":
                jurisdiction = st.text_input(
                    "Specify Jurisdiction",
                    placeholder="Enter jurisdiction"
                )
            else:
                jurisdiction = jurisdiction_select

        # Additional context
        with st.expander("Additional Context (Optional)", expanded=False):
            organization_size = st.selectbox(
                "Organization Size",
                options=["Startup (<50)", "SMB (50-500)", "Enterprise (500-5000)", "Large Enterprise (5000+)"],
                index=2
            )

            timeline = st.selectbox(
                "Implementation Timeline",
                options=["Proof of Concept", "Pilot Project", "Production Deployment", "Scaling Existing"],
                index=1
            )

            existing_systems = st.text_area(
                "Existing Systems (if any)",
                placeholder="List any existing systems the AI agent needs to integrate with",
                height=80
            )

            safety_requirements = st.text_area(
                "Safety Requirements (if any)",
                placeholder="Describe any specific safety or compliance requirements",
                height=80
            )

        # Submit button
        submitted = st.form_submit_button("Start Assessment", type="primary", use_container_width=True)

        if submitted:
            # Validate required fields
            if not industry or industry == "Other":
                st.error("Please specify an industry.")
                return False, {}

            if not use_case or len(use_case.strip()) < 20:
                st.error("Please provide a more detailed use case description (at least 20 characters).")
                return False, {}

            if not jurisdiction or jurisdiction == "Other":
                st.error("Please specify a jurisdiction.")
                return False, {}

            # Return form data
            form_data = {
                "industry": industry,
                "use_case": use_case.strip(),
                "jurisdiction": jurisdiction,
                "organization_size": organization_size,
                "timeline": timeline,
                "existing_systems": existing_systems.strip() if existing_systems else None,
                "safety_requirements": safety_requirements.strip() if safety_requirements else None,
            }

            return True, form_data

    return False, {}


def render_input_summary(form_data: Dict[str, Any]) -> None:
    """Render a summary of the submitted input data.

    Args:
        form_data: Dictionary containing the form data
    """
    st.markdown("### Assessment Context")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Industry", form_data.get("industry", "N/A"))

    with col2:
        st.metric("Jurisdiction", form_data.get("jurisdiction", "N/A"))

    with col3:
        st.metric("Timeline", form_data.get("timeline", "N/A"))

    with st.expander("Use Case Details", expanded=True):
        st.markdown(form_data.get("use_case", "N/A"))

        if form_data.get("existing_systems"):
            st.markdown("**Existing Systems:**")
            st.markdown(form_data["existing_systems"])

        if form_data.get("safety_requirements"):
            st.markdown("**Safety Requirements:**")
            st.markdown(form_data["safety_requirements"])
