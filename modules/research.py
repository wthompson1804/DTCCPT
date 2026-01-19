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
    full_content: str = ""  # Store full research response


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


def get_anthropic_client(model: str = "claude-sonnet-4-20250514", api_key: Optional[str] = None) -> ChatAnthropic:
    """Get an Anthropic Claude client.

    Args:
        model: Model name to use
        api_key: Optional API key (falls back to environment variable)

    Returns:
        ChatAnthropic client instance
    """
    # Use provided key or fall back to environment
    key = api_key or os.getenv("ANTHROPIC_API_KEY")

    if not key:
        raise ValueError("ANTHROPIC_API_KEY not provided")

    return ChatAnthropic(
        model=model,
        api_key=key,
        max_tokens=8192,
    )


async def conduct_research_async(
    industry: str,
    use_case: str,
    jurisdiction: str,
    organization_size: str = "Enterprise",
    timeline: str = "Pilot Project",
    model: str = "claude-sonnet-4-20250514",
    api_key: Optional[str] = None
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
        api_key: Optional API key

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
        client = get_anthropic_client(model, api_key)

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

        # Store full content for reference
        result.full_content = research_content

        # Update result with findings
        result.status = "complete"

        # Extract each research section
        result.industry_adoption.findings = extract_section(research_content, "Industry AI Adoption")
        result.regulatory_environment.findings = extract_section(research_content, "Regulatory Environment")
        result.technical_integration.findings = extract_section(research_content, "Technical Integration")
        result.risk_failure_modes.findings = extract_section(research_content, "Risk & Failure Modes")
        result.economic_viability.findings = extract_section(research_content, "Economic Viability")

        # Update confidence for each area based on content quality
        for area in [result.industry_adoption, result.regulatory_environment,
                     result.technical_integration, result.risk_failure_modes,
                     result.economic_viability]:
            if len(area.findings) > 500:
                area.confidence = "high"
            elif len(area.findings) > 100:
                area.confidence = "medium"
            else:
                area.confidence = "low"

        # Extract recommendations
        result.go_no_go = extract_go_no_go(research_content)
        result.recommended_type = extract_agent_type(research_content)
        result.confidence_level = extract_confidence(research_content)

        # Extract key risks and success factors
        result.key_risks = extract_bullet_list(research_content, "Key Risk Factors")
        result.critical_success_factors = extract_bullet_list(research_content, "Critical Success Factors")

        # If no risks extracted, try alternative patterns
        if not result.key_risks:
            result.key_risks = extract_bullet_list(research_content, "Risk Factors")
        if not result.critical_success_factors:
            result.critical_success_factors = extract_bullet_list(research_content, "Success Factors")

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
    model: str = "claude-sonnet-4-20250514",
    api_key: Optional[str] = None
) -> ResearchResult:
    """Synchronous wrapper for research function.

    Args:
        industry: Industry sector
        use_case: Use case description
        jurisdiction: Primary regulatory jurisdiction
        organization_size: Organization size
        timeline: Implementation timeline
        model: Claude model to use
        api_key: Optional API key

    Returns:
        ResearchResult with findings
    """
    return asyncio.run(conduct_research_async(
        industry=industry,
        use_case=use_case,
        jurisdiction=jurisdiction,
        organization_size=organization_size,
        timeline=timeline,
        model=model,
        api_key=api_key
    ))


def extract_section(content: str, section_name: str) -> str:
    """Extract a section from the research content.

    Handles various header formats:
    - ## 1. Industry AI Adoption
    - ## Industry AI Adoption
    - # Industry AI Adoption
    - ### INDUSTRY AI ADOPTION
    - **Industry AI Adoption**

    Args:
        content: Full research content
        section_name: Name of section to extract

    Returns:
        Section content or empty string
    """
    import re

    # Build flexible patterns for the section name
    # Allow for numbering, different header levels, and case variations
    section_words = section_name.split()

    # Pattern variations to try
    patterns = [
        # Numbered markdown header: ## 1. Industry AI Adoption
        rf"#{1,4}\s*\d+\.?\s*{re.escape(section_name)}[^\n]*\n(.*?)(?=\n#{1,4}\s|\Z)",
        # Plain markdown header: ## Industry AI Adoption
        rf"#{1,4}\s*{re.escape(section_name)}[^\n]*\n(.*?)(?=\n#{1,4}\s|\Z)",
        # Bold header: **Industry AI Adoption**
        rf"\*\*{re.escape(section_name)}\*\*[^\n]*\n(.*?)(?=\n\*\*|\n#{1,4}\s|\Z)",
        # Numbered without hash: 1. Industry AI Adoption
        rf"^\d+\.\s*{re.escape(section_name)}[^\n]*\n(.*?)(?=\n\d+\.|\n#{1,4}\s|\Z)",
    ]

    # Also try with partial matches for key words
    if len(section_words) >= 2:
        # Match on key distinctive words (e.g., "Industry" + "Adoption")
        key_word1 = re.escape(section_words[0])
        key_word2 = re.escape(section_words[-1])
        patterns.extend([
            rf"#{1,4}\s*\d*\.?\s*[^\n]*{key_word1}[^\n]*{key_word2}[^\n]*\n(.*?)(?=\n#{1,4}\s|\Z)",
        ])

    for pattern in patterns:
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE | re.MULTILINE)
        if match:
            result = match.group(1).strip()
            # Ensure we got actual content, not just whitespace
            if len(result) > 20:
                return result

    # Last resort: try to find any section that contains the key words
    for word in section_words:
        if len(word) > 4:  # Skip short words like "AI", "&"
            pattern = rf"#{1,4}[^\n]*{re.escape(word)}[^\n]*\n(.*?)(?=\n#{1,4}\s|\Z)"
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            if match and len(match.group(1).strip()) > 50:
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


def extract_bullet_list(content: str, section_name: str) -> List[str]:
    """Extract a bullet list from content following a section header.

    Args:
        content: Full research content
        section_name: Name of section containing the bullet list

    Returns:
        List of bullet items
    """
    import re

    items = []

    # Try to find the section and extract bullets
    patterns = [
        rf"\*\*{re.escape(section_name)}[:\*]*\*\*[^\n]*\n((?:[-*•]\s*[^\n]+\n?)+)",
        rf"{re.escape(section_name)}[:\s]*\n((?:[-*•]\s*[^\n]+\n?)+)",
        rf"#{1,4}\s*{re.escape(section_name)}[^\n]*\n((?:[-*•]\s*[^\n]+\n?)+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, content, re.IGNORECASE | re.MULTILINE)
        if match:
            bullet_text = match.group(1)
            # Extract individual bullet items
            bullet_matches = re.findall(r'[-*•]\s*(.+?)(?=\n[-*•]|\n\n|\Z)', bullet_text, re.DOTALL)
            for item in bullet_matches:
                clean_item = item.strip()
                if clean_item and len(clean_item) > 3:
                    items.append(clean_item)
            if items:
                break

    return items[:5]  # Return max 5 items


def format_research_for_display(result: ResearchResult) -> Dict[str, Any]:
    """Format research results for Streamlit display.

    Args:
        result: ResearchResult object

    Returns:
        Dictionary formatted for UI display
    """
    # Extract sources from full content if not already populated
    sources = result.all_sources
    if not sources and result.full_content:
        sources = extract_sources(result.full_content)

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
        "sources": sources,
        "full_content": result.full_content,
        "error": result.error_message,
    }


def extract_sources(content: str) -> List[Dict[str, str]]:
    """Extract source citations from research content.

    Args:
        content: Full research content

    Returns:
        List of source dictionaries with title and url keys
    """
    import re

    sources = []

    # Look for markdown links: [Title](URL)
    link_pattern = r'\[([^\]]+)\]\((https?://[^\)]+)\)'
    matches = re.findall(link_pattern, content)

    for title, url in matches:
        if not any(s.get('url') == url for s in sources):  # Avoid duplicates
            sources.append({"title": title.strip(), "url": url.strip()})

    # Look for plain URLs with context
    url_pattern = r'(?:^|\s)(https?://[^\s\)]+)'
    url_matches = re.findall(url_pattern, content)

    for url in url_matches:
        if not any(s.get('url') == url for s in sources):
            sources.append({"title": url.split('/')[2], "url": url})

    return sources[:15]  # Limit to 15 sources
