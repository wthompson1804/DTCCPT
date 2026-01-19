"""
Export module for generating professional documentation.

This module provides export capabilities for:
- Markdown reports
- PDF documents
- DOCX documents
- HTML visualizations
- Complete assessment packages
"""

import io
from typing import Dict, Any, Optional
from datetime import datetime


def generate_markdown_report(
    form_data: Dict[str, Any],
    research_results: Dict[str, Any],
    requirements_output: Dict[str, Any],
    agent_design_output: Dict[str, Any],
    capability_mapping: Dict[str, Any]
) -> str:
    """Generate a complete markdown assessment report.

    Args:
        form_data: User input form data
        research_results: Research findings
        requirements_output: Generated requirements
        agent_design_output: Agent design assessment
        capability_mapping: Capability mappings

    Returns:
        Complete markdown report string
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    agent_type = "N/A"
    if agent_design_output:
        agent_type = agent_design_output.get(
            'confirmed_type',
            agent_design_output.get('recommended_type', 'N/A')
        )

    report = f"""# DTC AI Agent Capability Assessment Report

**Generated:** {timestamp}
**Methodology:** Digital Twin Consortium AI Agent Capabilities Periodic Table (CPT)

---

## Executive Summary

| Parameter | Value |
|-----------|-------|
| Industry | {form_data.get('industry', 'N/A')} |
| Jurisdiction | {form_data.get('jurisdiction', 'N/A')} |
| Agent Type | {agent_type} |
| Capabilities Mapped | {capability_mapping.get('total_mapped', 0) if capability_mapping else 0} |
| Essential Capabilities | {capability_mapping.get('essential_count', 0) if capability_mapping else 0} |

---

## 1. Use Case Definition

### Industry Context
**Industry:** {form_data.get('industry', 'N/A')}
**Jurisdiction:** {form_data.get('jurisdiction', 'N/A')}
**Organization Size:** {form_data.get('organization_size', 'N/A')}
**Timeline:** {form_data.get('timeline', 'N/A')}

### Use Case Description
{form_data.get('use_case', 'No use case provided')}

### Existing Systems
{form_data.get('existing_systems', 'None specified')}

### Safety Requirements
{form_data.get('safety_requirements', 'None specified')}

---

## 2. Research Findings

"""

    if research_results:
        preliminary = research_results.get('preliminary_assessment', {})
        report += f"""### Preliminary Assessment
- **Go/No-Go Recommendation:** {preliminary.get('go_no_go', 'N/A').upper()}
- **Recommended Agent Type:** {preliminary.get('recommended_type', 'N/A')}
- **Confidence Level:** {preliminary.get('confidence_level', 'N/A').upper()}

### Key Risk Factors
"""
        for risk in preliminary.get('key_risks', ['None identified']):
            report += f"- {risk}\n"

        report += "\n### Research Areas\n\n"

        areas = research_results.get('research_areas', {})
        for area_key, area_data in areas.items():
            area_name = area_data.get('name', area_key)
            findings = area_data.get('findings', 'No findings')
            confidence = area_data.get('confidence', 'medium')
            report += f"#### {area_name}\n**Confidence:** {confidence.upper()}\n\n{findings}\n\n"
    else:
        report += "*Research not conducted*\n\n"

    report += """---

## 3. Business Requirements

"""

    if requirements_output:
        report += requirements_output.get('full_text', '*Requirements not generated*')
    else:
        report += "*Requirements not generated*"

    report += f"""

---

## 4. Agent Design

### Recommended Agent Type: {agent_type}

"""

    if agent_design_output:
        type_info = agent_design_output.get('type_info', {})
        report += f"""**Type Name:** {type_info.get('name', 'N/A')}
**Description:** {type_info.get('description', 'N/A')}

### Justification
{agent_design_output.get('justification', 'No justification provided')}

### Architecture Summary
{agent_design_output.get('architecture_summary', 'No architecture summary')}

### Full Design Document
{agent_design_output.get('full_document', '*Design document not available*')}
"""
    else:
        report += "*Agent design not generated*\n"

    report += """
---

## 5. Capability Mapping

"""

    if capability_mapping:
        report += f"""### Summary
- **Total Capabilities Mapped:** {capability_mapping.get('total_mapped', 0)}
- **Essential:** {capability_mapping.get('essential_count', 0)}
- **Advanced:** {capability_mapping.get('advanced_count', 0)}
- **Optional:** {capability_mapping.get('optional_count', 0)}

### Essential Capabilities
"""
        for cap_id in capability_mapping.get('essential_capabilities', []):
            report += f"- {cap_id}\n"

        report += "\n### Advanced Capabilities\n"
        for cap_id in capability_mapping.get('advanced_capabilities', []):
            report += f"- {cap_id}\n"

        report += "\n### Optional Capabilities\n"
        for cap_id in capability_mapping.get('optional_capabilities', []):
            report += f"- {cap_id}\n"

        report += "\n### Detailed Mapping\n"
        report += capability_mapping.get('full_document', '*Mapping document not available*')
    else:
        report += "*Capability mapping not generated*\n"

    report += f"""

---

## Appendix

### Methodology Reference
This assessment follows the Digital Twin Consortium's AI Agent Capabilities Periodic Table (CPT) framework, which organizes 45 capabilities across 6 categories:

1. **PK - Perception & Knowledge:** Environmental awareness and knowledge access
2. **CG - Cognition & Reasoning:** Planning, reasoning, and decision-making
3. **LA - Learning & Adaptation:** Memory, learning, and self-optimization
4. **AE - Action & Execution:** Task execution and tool integration
5. **IC - Interaction & Collaboration:** Communication and coordination
6. **GS - Governance & Safety:** Deployment, monitoring, and compliance

### Agent Types (T0-T4)
- **T0:** Static Automation - Rule-based, no learning
- **T1:** Conversational Agents - NLP interaction, basic context
- **T2:** Procedural Workflow Agents - Multi-step execution, tool integration
- **T3:** Cognitive Autonomous Agents - Self-directed planning, learning
- **T4:** Multi-Agent Generative Systems (MAGS) - Collaborative intelligence

---

*Report generated by DTC AI Agent Capability Assessment Tool*
*Powered by Digital Twin Consortium CPT Framework and Anthropic Claude*
"""

    return report


def generate_executive_summary(
    form_data: Dict[str, Any],
    research_results: Dict[str, Any],
    agent_design_output: Dict[str, Any],
    capability_mapping: Dict[str, Any]
) -> str:
    """Generate a brief executive summary.

    Args:
        form_data: User input form data
        research_results: Research findings
        agent_design_output: Agent design assessment
        capability_mapping: Capability mappings

    Returns:
        Executive summary string
    """
    agent_type = "N/A"
    if agent_design_output:
        agent_type = agent_design_output.get(
            'confirmed_type',
            agent_design_output.get('recommended_type', 'N/A')
        )

    go_no_go = "N/A"
    if research_results:
        go_no_go = research_results.get('preliminary_assessment', {}).get('go_no_go', 'N/A')

    summary = f"""# Executive Summary

## AI Agent Capability Assessment

**Industry:** {form_data.get('industry', 'N/A')}
**Use Case:** {form_data.get('use_case', 'N/A')[:200]}...

### Key Findings

| Metric | Value |
|--------|-------|
| Go/No-Go | {go_no_go.upper()} |
| Recommended Agent Type | {agent_type} |
| Capabilities Required | {capability_mapping.get('total_mapped', 0) if capability_mapping else 0} |
| Essential Capabilities | {capability_mapping.get('essential_count', 0) if capability_mapping else 0} |

### Recommendation

Based on the assessment, we recommend proceeding with a **{agent_type}** agent architecture.

"""

    if agent_design_output and agent_design_output.get('justification'):
        summary += f"**Justification:** {agent_design_output['justification'][:500]}"

    return summary


def export_to_html_package(
    form_data: Dict[str, Any],
    research_results: Dict[str, Any],
    requirements_output: Dict[str, Any],
    agent_design_output: Dict[str, Any],
    capability_mapping: Dict[str, Any]
) -> str:
    """Generate a self-contained HTML package with all assessment data.

    Args:
        form_data: User input form data
        research_results: Research findings
        requirements_output: Generated requirements
        agent_design_output: Agent design assessment
        capability_mapping: Capability mappings

    Returns:
        Self-contained HTML string
    """
    markdown_report = generate_markdown_report(
        form_data,
        research_results,
        requirements_output,
        agent_design_output,
        capability_mapping
    )

    # Convert markdown to basic HTML
    html_content = markdown_report.replace('\n', '<br>\n')
    html_content = html_content.replace('# ', '<h1>').replace('\n<br>', '</h1>\n')
    html_content = html_content.replace('## ', '<h2>').replace('\n<br>', '</h2>\n')
    html_content = html_content.replace('### ', '<h3>').replace('\n<br>', '</h3>\n')

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DTC AI Agent Capability Assessment</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px;
            line-height: 1.6;
            color: #1F2937;
        }}
        h1 {{ color: #1F2937; border-bottom: 3px solid #3B82F6; padding-bottom: 10px; }}
        h2 {{ color: #374151; margin-top: 30px; }}
        h3 {{ color: #4B5563; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #E5E7EB; padding: 12px; text-align: left; }}
        th {{ background: #F3F4F6; }}
        hr {{ border: none; border-top: 1px solid #E5E7EB; margin: 30px 0; }}
        .header {{ text-align: center; margin-bottom: 40px; }}
        .footer {{ text-align: center; margin-top: 40px; color: #6B7280; font-size: 0.9rem; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>DTC AI Agent Capability Assessment</h1>
        <p>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}</p>
    </div>

    <div class="content">
        {html_content}
    </div>

    <div class="footer">
        <p>Powered by Digital Twin Consortium CPT Framework and Anthropic Claude</p>
    </div>
</body>
</html>"""

    return html
