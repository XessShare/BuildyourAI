"""
J-Jeco AI Agents Package

Spezialisierte Agenten für:
- Project Management
- Content Creation
- Research & Analysis
- Verification & QA
- Communication Optimization
- Deployment Orchestration
- Code Generation (NEW)
- Resource Management (NEW)
"""

from .base_agent import BaseAgent
from .project_manager_agent import ProjectManagerAgent
from .communicator_agent import CommunicatorAgent
from .content_creator_agent import ContentCreatorAgent
from .researcher_agent import ResearcherAgent
from .verifier_agent import VerifierAgent
from .analyst_agent import AnalystAgent
from .deployment_orchestrator import DeploymentOrchestratorAgent
from .webhook_handler import WebhookHandlerAgent
from .code_generation_agent import CodeGenerationAgent
from .resource_manager import ResourceManager

__all__ = [
    'BaseAgent',
    'ProjectManagerAgent',
    'CommunicatorAgent',
    'ContentCreatorAgent',
    'ResearcherAgent',
    'VerifierAgent',
    'AnalystAgent',
    'DeploymentOrchestratorAgent',
    'WebhookHandlerAgent',
    'CodeGenerationAgent',
    'ResourceManager',
]

__version__ = '0.4.0'
