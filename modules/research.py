"""
Research module for Open Deep Research integration.

This module provides the research functionality for Step 0 of the DTC workflow,
using LangChain's Open Deep Research framework to conduct comprehensive
industry and regulatory research.
"""

import os
import asyncio
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from pathlib import Path

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage


@dataclass
class ResearchArea:
    """Represents a research area with its findings."""
    name: str
    findings: str = ""
    sources: List[Dict[str, str]] = field(default_factory=list)
    confidence: str = "medium"  # high, medium, low


@dataclass
class ResearchResult:
    """Complete research results for a use case."""
    industry: str
    use_case: str
    jurisdiction: str

    # Research areas
    industry_adoption: ResearchArea = field(default_factory=lambda: ResearchArea("Industry AI Adoption"))
    regulatory_environment: ResearchArea = field(default_factory=lambda: ResearchArea("Regulatory Environment"))
    technical_integration: ResearchArea = field(default_factory=lambda: ResearchArea("Technical Integration"))
    risk_failure_modes: ResearchArea = field(default_factory=lambda: ResearchArea("Risk & Failure Modes"))
    economic_viability: ResearchArea = field(default_factory=lambda: ResearchArea("Economic Viability"))

    # Preliminary assessment
    go_no_go: str = "pending"  # go, caution, no-go, pending
    recommended_type: str = "T2"  # T0-T4
    confidence_level: str = "medium"  # high, medium, low
    key_risks: List[str] = field(default_factory=list)
    critical_success_factors: List[str] = field(default_factory=list)

    # Metadata
    status: str = "pending"  # pending, in_progress, complete, error
    error_message: Optional[str] = None
    all_sources: List[Dict[str, str]] = field(default_factory=list)


def load_research_template() -> str:
    """Load the enhanced Step 0 research brief template."""
    template_path = Path(__file__).parent.parent / "prompts" / "step_0_research_brief.md"

    with open(template_path, 'r') as f:
        return f.read()


def build_research_prompt(
    industry: str,
    use_case: str,
    jurisdiction: str,
    organization_size: str = "Enterprise",
    timeline: str = "Pilot Project"
) -> str:
    """Build the complete research prompt from the template.

    Args:
        industry: Industry sector
        use_case: Use case description
        jurisdiction: Primary regulatory jurisdiction
        organization_size: Organization size category
        timeline: Implementation timeline

    Returns:
        Formatted research prompt
    """
    template = load_research_template()

    # Replace placeholders
    prompt = template.replace("{industry}", industry)
    prompt = prompt.replace("{use_case}", use_case)
    prompt = prompt.replace("{jurisdiction}", jurisdiction)
    prompt = prompt.replace("{organization_size}", organization_size)
    prompt = prompt.replace("{timeline}", timeline)

    return prompt


def get_anthropic_client(model: str = "claude-sonnet-4-20250514") -> ChatAnthropic:
    """Get an Anthropic Claude client.

    Args:
        model: Model name to use

    Returns:
        ChatAnthropic client instance
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")

    return ChatAnthropic(
        model=model,
        api_key=api_key,
        max_tokens=8192,
    )


async def conduct_research_async(
    industry: str,
    use_case: str,
    jurisdiction: str,
    organization_size: str = "Enterprise",
    timeline: str = "Pilot Project",
    model: str = "claude-sonnet-4-20250514"
) -> ResearchResult:
    """Conduct comprehensive research asynchronously.

    This is the main research function that integrates with Claude
    to conduct the DTC-specific research across all 5 areas.

    Args:
        industry: Industry sector
        use_case: Use case description
        jurisdiction: Primary regulatory jurisdiction
        organization_size: Organization size
        timeline: Implementation timeline
        model: Claude model to use

    Returns:
        ResearchResult with findings
    """
    result = ResearchResult(
        industry=industry,
        use_case=use_case,
        jurisdiction=jurisdiction,
        status="in_progress"
    )

    try:
        client = get_anthropic_client(model)

        # Build the research prompt
        research_prompt = build_research_prompt(
            industry=industry,
            use_case=use_case,
            jurisdiction=jurisdiction,
            organization_size=organization_size,
            timeline=timeline
        )

        # System message for research context
        system_message = SystemMessage(content="""You are a senior research analyst specializing in industrial AI implementations and digital twin technologies.

Your task is to conduct comprehensive research for an AI agent capability assessment following the Digital Twin Consortium methodology.

Guidelines:
1. Provide specific, actionable intelligence grounded in current industry knowledge
2. Cite specific sources, standards, and regulations where applicable
3. Be honest about areas of uncertainty or where information is limited
4. Focus on practical implications for implementation
5. Consider both technical and organizational factors

When recommending an agent type (T0-T4), consider:
- T0: Simple rule-based automation (deterministic, no learning)
- T1: Conversational interfaces (NLP, basic context)
- T2: Procedural workflows (multi-step, tool integration)
- T3: Cognitive autonomy (planning, learning, adaptation)
- T4: Multi-agent systems (distributed, collaborative)

Provide your research in a structured format with clear sections for each research area.""")

        # Execute research query
        response = await client.ainvoke([
            system_message,
            HumanMessage(content=research_prompt)
        ])

        # Parse response into research result
        research_content = response.content

        # Update result with findings
        result.status = "complete"

        # Extract preliminary assessment from response
        # In a full implementation, this would parse the structured response
        # For now, we store the full response and extract key indicators
        result.industry_adoption.findings = extract_section(research_content, "Industry AI Adoption")
        result.regulatory_environment.findings = extract_section(research_content, "Regulatory Environment")
        result.technical_integration.findings = extract_section(research_content, "Technical Integration")
        result.risk_failure_modes.findings = extract_section(research_content, "Risk & Failure Modes")
        result.economic_viability.findings = extract_section(research_content, "Economic Viability")

        # Extract recommendations
        result.go_no_go = extract_go_no_go(research_content)
        result.recommended_type = extract_agent_type(research_content)
        result.confidence_level = extract_confidence(research_content)

        return result

    except Exception as e:
        result.status = "error"
        result.error_message = str(e)
        return result


def conduct_research(
    industry: str,
    use_case: str,
    jurisdiction: str,
    organization_size: str = "Enterprise",
    timeline: str = "Pilot Project",
    model: str = "claude-sonnet-4-20250514"
) -> ResearchResult:
    """Synchronous wrapper for research function.

    Args:
        industry: Industry sector
        use_case: Use case description
        jurisdiction: Primary regulatory jurisdiction
        organization_size: Organization size
        timeline: Implementation timeline
        model: Claude model to use

    Returns:
        ResearchResult with findings
    """
    return asyncio.run(conduct_research_async(
        industry=industry,
        use_case=use_case,
        jurisdiction=jurisdiction,
        organization_size=organization_size,
        timeline=timeline,
        model=model
    ))


def extract_section(content: str, section_name: str) -> str:
    """Extract a section from the research content.

    Args:
        content: Full research content
        section_name: Name of section to extract

    Returns:
        Section content or empty string
    """
    # Simple extraction - look for section header and get content until next header
    import re

    # Try to find the section
    pattern = rf"(?:##?\s*\d*\.?\s*)?{re.escape(section_name)}.*?\n(.*?)(?=\n##|\n#|\Z)"
    match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)

    if match:
        return match.group(1).strip()

    return ""


def extract_go_no_go(content: str) -> str:
    """Extract go/no-go recommendation from content."""
    content_lower = content.lower()

    if "no-go" in content_lower or "not recommended" in content_lower:
        return "no-go"
    elif "caution" in content_lower or "proceed with caution" in content_lower:
        return "caution"
    elif "go" in content_lower or "recommended" in content_lower:
        return "go"

    return "caution"  # Default to caution


def extract_agent_type(content: str) -> str:
    """Extract recommended agent type from content."""
    import re

    # Look for explicit T0-T4 mentions
    match = re.search(r'\b(T[0-4])\b', content)
    if match:
        return match.group(1)

    # Try to infer from keywords
    content_lower = content.lower()

    if "multi-agent" in content_lower or "mags" in content_lower or "distributed" in content_lower:
        return "T4"
    elif "cognitive" in content_lower or "autonomous" in content_lower or "learning" in content_lower:
        return "T3"
    elif "workflow" in content_lower or "procedural" in content_lower or "tool" in content_lower:
        return "T2"
    elif "conversational" in content_lower or "chatbot" in content_lower:
        return "T1"
    elif "rule-based" in content_lower or "static" in content_lower:
        return "T0"

    return "T2"  # Default to procedural workflow


def extract_confidence(content: str) -> str:
    """Extract confidence level from content."""
    content_lower = content.lower()

    if "high confidence" in content_lower or "strongly recommend" in content_lower:
        return "high"
    elif "low confidence" in content_lower or "limited information" in content_lower:
        return "low"

    return "medium"


def format_research_for_display(result: ResearchResult) -> Dict[str, Any]:
    """Format research results for Streamlit display.

    Args:
        result: ResearchResult object

    Returns:
        Dictionary formatted for UI display
    """
    return {
        "summary": {
            "industry": result.industry,
            "use_case": result.use_case,
            "jurisdiction": result.jurisdiction,
            "status": result.status,
        },
        "preliminary_assessment": {
            "go_no_go": result.go_no_go,
            "recommended_type": result.recommended_type,
            "confidence_level": result.confidence_level,
            "key_risks": result.key_risks,
            "critical_success_factors": result.critical_success_factors,
        },
        "research_areas": {
            "industry_adoption": {
                "name": result.industry_adoption.name,
                "findings": result.industry_adoption.findings,
                "confidence": result.industry_adoption.confidence,
            },
            "regulatory_environment": {
                "name": result.regulatory_environment.name,
                "findings": result.regulatory_environment.findings,
                "confidence": result.regulatory_environment.confidence,
            },
            "technical_integration": {
                "name": result.technical_integration.name,
                "findings": result.technical_integration.findings,
                "confidence": result.technical_integration.confidence,
            },
            "risk_failure_modes": {
                "name": result.risk_failure_modes.name,
                "findings": result.risk_failure_modes.findings,
                "confidence": result.risk_failure_modes.confidence,
            },
            "economic_viability": {
                "name": result.economic_viability.name,
                "findings": result.economic_viability.findings,
                "confidence": result.economic_viability.confidence,
            },
        },
        "sources": result.all_sources,
        "error": result.error_message,
    }
