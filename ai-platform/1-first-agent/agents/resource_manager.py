"""
Resource Manager
Verwaltet AI-Resource-Nutzung und Routing-Logik

Klassifiziert Tasks und entscheidet über Tool-Auswahl:
- Claude: Nur für privilegierte Aufgaben (Architektur, komplexe Probleme)
- OpenCode/Code-X: Für Standard Code-Generierung
- GPT-4o-mini: Für einfache Tasks und Fallback
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path

import sys
sys.path.append(str(Path(__file__).parent.parent))
from config import (
    CLAUDE_RESOURCE_POLICY,
    TASK_CLASSIFICATION,
    CODE_GENERATION_AGENT_CONFIG,
    OPENCODE_PATH,
    CODEX_PATH
)

logger = logging.getLogger(__name__)


class TaskPriority:
    """Task-Prioritäts-Level"""
    PRIVILEGED = "PRIVILEGED"
    STANDARD = "STANDARD"
    SIMPLE = "SIMPLE"


class ResourceManager:
    """
    Verwaltet AI-Resource-Nutzung und Task-Routing
    """

    def __init__(self):
        self.policy = CLAUDE_RESOURCE_POLICY
        self.classification = TASK_CLASSIFICATION
        self.claude_usage = defaultdict(list)  # Track Claude usage by hour/day
        self.logger = logging.getLogger(f"{__name__}.ResourceManager")
        
    def classify_task(self, task: Dict[str, Any]) -> str:
        """
        Klassifiziert Task nach Komplexität und Priorität
        
        Args:
            task: Task-Dictionary mit 'type', 'description', 'complexity', etc.
            
        Returns:
            Task-Priorität: PRIVILEGED, STANDARD, oder SIMPLE
        """
        task_type = task.get("type", "").lower()
        description = task.get("description", "").lower()
        complexity = task.get("complexity", "standard").lower()
        
        # Prüfe explizite Komplexität
        if complexity in ["complex", "critical", "architectural"]:
            return TaskPriority.PRIVILEGED
        
        # Prüfe Task-Type
        if task_type in ["architectural_decision", "system_design", "strategic_planning"]:
            return TaskPriority.PRIVILEGED
        
        # Prüfe Keywords in Description
        text = f"{task_type} {description}"
        
        privileged_keywords = self.classification["PRIVILEGED"]["keywords"]
        if any(keyword in text for keyword in privileged_keywords):
            return TaskPriority.PRIVILEGED
        
        simple_keywords = self.classification["SIMPLE"]["keywords"]
        if any(keyword in text for keyword in simple_keywords):
            return TaskPriority.SIMPLE
        
        # Default: STANDARD
        return TaskPriority.STANDARD
    
    def should_use_claude(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Entscheidet ob Claude für diesen Task verwendet werden soll
        
        Args:
            task: Task-Dictionary
            
        Returns:
            Dict mit:
            - use_claude: bool
            - reason: str
            - quota_status: dict
        """
        if not self.policy["enabled"]:
            return {
                "use_claude": False,
                "reason": "Claude resource policy disabled",
                "quota_status": {}
            }
        
        # Klassifiziere Task
        priority = self.classify_task(task)
        
        # Prüfe ob Task-Type privilegiert ist
        task_type = task.get("type", "")
        is_privileged_type = task_type in self.policy["privileged_task_types"]
        
        if priority != TaskPriority.PRIVILEGED and not is_privileged_type:
            return {
                "use_claude": False,
                "reason": f"Task is {priority}, not privileged",
                "quota_status": {}
            }
        
        # Prüfe Quotas
        quota_status = self.check_claude_quota()
        
        if not quota_status["available"]:
            return {
                "use_claude": False,
                "reason": f"Claude quota exceeded: {quota_status['reason']}",
                "quota_status": quota_status,
                "fallback_model": self.policy["fallback_model"]
            }
        
        # Prüfe ob Approval benötigt wird
        if self.policy["require_approval"]:
            return {
                "use_claude": True,
                "reason": "Claude approved for privileged task",
                "quota_status": quota_status,
                "requires_approval": True
            }
        
        return {
            "use_claude": True,
            "reason": f"Task is {priority} and within quota",
            "quota_status": quota_status
        }
    
    def check_claude_quota(self) -> Dict[str, Any]:
        """
        Prüft ob Claude-Quota verfügbar ist
        
        Returns:
            Dict mit:
            - available: bool
            - reason: str
            - hourly_usage: int
            - daily_usage: int
        """
        now = datetime.now()
        today = now.date()
        current_hour = now.replace(minute=0, second=0, microsecond=0)
        
        # Zähle heutige Nutzung
        daily_usage = sum(
            1 for timestamp in self.claude_usage.get("daily", [])
            if datetime.fromisoformat(timestamp).date() == today
        )
        
        # Zähle stündliche Nutzung
        hourly_usage = sum(
            1 for timestamp in self.claude_usage.get("hourly", [])
            if datetime.fromisoformat(timestamp) >= current_hour
        )
        
        # Prüfe Limits
        if daily_usage >= self.policy["daily_quota"]:
            return {
                "available": False,
                "reason": f"Daily quota exceeded ({daily_usage}/{self.policy['daily_quota']})",
                "hourly_usage": hourly_usage,
                "daily_usage": daily_usage
            }
        
        if hourly_usage >= self.policy["hourly_quota"]:
            return {
                "available": False,
                "reason": f"Hourly quota exceeded ({hourly_usage}/{self.policy['hourly_quota']})",
                "hourly_usage": hourly_usage,
                "daily_usage": daily_usage
            }
        
        return {
            "available": True,
            "reason": "Quota available",
            "hourly_usage": hourly_usage,
            "daily_usage": daily_usage,
            "hourly_remaining": self.policy["hourly_quota"] - hourly_usage,
            "daily_remaining": self.policy["daily_quota"] - daily_usage
        }
    
    def record_claude_usage(self):
        """Zeichnet Claude-Nutzung auf"""
        now = datetime.now().isoformat()
        self.claude_usage["daily"].append(now)
        self.claude_usage["hourly"].append(now)
        
        # Cleanup alte Einträge (älter als 24h)
        cutoff = datetime.now() - timedelta(days=1)
        self.claude_usage["daily"] = [
            ts for ts in self.claude_usage["daily"]
            if datetime.fromisoformat(ts) >= cutoff
        ]
        
        # Cleanup alte stündliche Einträge (älter als 1h)
        cutoff_hour = datetime.now() - timedelta(hours=1)
        self.claude_usage["hourly"] = [
            ts for ts in self.claude_usage["hourly"]
            if datetime.fromisoformat(ts) >= cutoff_hour
        ]
    
    def route_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Routet Task zu passendem Tool
        
        Args:
            task: Task-Dictionary
            
        Returns:
            Dict mit:
            - tool: str (claude, opencode, codex, gpt-mini)
            - priority: str
            - reason: str
        """
        priority = self.classify_task(task)
        task_type = task.get("type", "").lower()
        
        # Prüfe Claude-Nutzung
        claude_decision = self.should_use_claude(task)
        
        if claude_decision["use_claude"]:
            self.record_claude_usage()
            return {
                "tool": "claude",
                "priority": priority,
                "reason": claude_decision["reason"],
                "quota_status": claude_decision.get("quota_status", {})
            }
        
        # Prüfe ob Code-Generierung
        if task_type in ["code_generation", "refactor", "implement"]:
            # Prüfe OpenCode/Code-X Verfügbarkeit
            if OPENCODE_PATH:
                return {
                    "tool": "opencode",
                    "priority": priority,
                    "reason": "OpenCode available for code generation"
                }
            elif CODEX_PATH:
                return {
                    "tool": "codex",
                    "priority": priority,
                    "reason": "Code-X available for code generation"
                }
            else:
                # Fallback zu LLM
                return {
                    "tool": "gpt-mini",
                    "priority": priority,
                    "reason": "No local code tools available, using LLM fallback"
                }
        
        # Standard: GPT-4o-mini
        return {
            "tool": "gpt-mini",
            "priority": priority,
            "reason": f"Standard task, using {CODE_GENERATION_AGENT_CONFIG['model']}"
        }
    
    def get_resource_stats(self) -> Dict[str, Any]:
        """
        Gibt Resource-Nutzungs-Statistiken zurück
        
        Returns:
            Dict mit Statistiken
        """
        quota_status = self.check_claude_quota()
        
        return {
            "claude": {
                "quota_status": quota_status,
                "policy": {
                    "daily_quota": self.policy["daily_quota"],
                    "hourly_quota": self.policy["hourly_quota"],
                    "enabled": self.policy["enabled"]
                }
            },
            "local_tools": {
                "opencode": {
                    "available": bool(OPENCODE_PATH),
                    "path": OPENCODE_PATH
                },
                "codex": {
                    "available": bool(CODEX_PATH),
                    "path": CODEX_PATH
                }
            },
            "classification_rules": self.classification
        }

