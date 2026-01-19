"""
DTC AI Agent Capability Assessment Tool - Core Modules

This package contains the core business logic for:
- Research: Open Deep Research integration
- Requirements: Step 1 business requirements generation
- Agent Design: Step 2 agent type assessment
- Capability Mapping: Step 3 CPT mapping
- Export: Document generation utilities
"""

from .data_loader import load_capabilities, load_prompt, load_config
from .research import conduct_research, format_research_for_display, ResearchResult
from .requirements import generate_requirements, format_requirements_for_display, RequirementsResult
from .agent_design import generate_agent_design, format_agent_design_for_display, AgentDesignResult
from .capability_mapping import generate_capability_mapping, format_capability_mapping_for_display, CapabilityMappingResult

__all__ = [
    # Data loading
    'load_capabilities',
    'load_prompt',
    'load_config',
    # Research (Step 0)
    'conduct_research',
    'format_research_for_display',
    'ResearchResult',
    # Requirements (Step 1)
    'generate_requirements',
    'format_requirements_for_display',
    'RequirementsResult',
    # Agent Design (Step 2)
    'generate_agent_design',
    'format_agent_design_for_display',
    'AgentDesignResult',
    # Capability Mapping (Step 3)
    'generate_capability_mapping',
    'format_capability_mapping_for_display',
    'CapabilityMappingResult',
]
