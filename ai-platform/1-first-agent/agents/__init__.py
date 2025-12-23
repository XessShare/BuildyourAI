"""
J-Jeco AI Agents Package

Spezialisierte Agenten für:
- Project Management
- Content Creation
- Research & Analysis
- Verification & QA
- Communication Optimization
"""

from .base_agent import BaseAgent
from .project_manager_agent import ProjectManagerAgent
from .communicator_agent import CommunicatorAgent
from .content_creator_agent import ContentCreatorAgent
from .researcher_agent import ResearcherAgent
from .verifier_agent import VerifierAgent
from .analyst_agent import AnalystAgent

__all__ = [
    'BaseAgent',
    'ProjectManagerAgent',
    'CommunicatorAgent',
    'ContentCreatorAgent',
    'ResearcherAgent',
    'VerifierAgent',
    'AnalystAgent',
]

__version__ = '0.1.0'
