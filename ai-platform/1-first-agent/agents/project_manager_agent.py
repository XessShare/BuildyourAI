"""
Project Manager Agent - Orchestrates all other agents

Koordiniert:
- Parallel laufende Agenten
- Task-Distribution
- Progress Tracking
- Quality Gates
"""

from typing import Dict, Any, List
import asyncio
from datetime import datetime
from .base_agent import BaseAgent


class ProjectManagerAgent(BaseAgent):
    """
    Der Dirigent des Agent-Orchesters

    Verantwortlich für:
    - Task-Priorisierung
    - Agent-Koordination
    - Milestone-Tracking
    - Risk Management
    """

    def __init__(self):
        super().__init__(agent_type="project_manager")
        self.active_tasks: List[Dict[str, Any]] = []
        self.completed_tasks: List[Dict[str, Any]] = []
        self.moonshot_progress = {
            "current_phase": "MVP",
            "milestones_completed": 0,
            "blockers": [],
            "kpis": {}
        }

    def get_system_prompt(self) -> str:
        return """Du bist der Project Manager Agent im J-Jeco System.

Du orchestrierst ein Netzwerk von spezialisierten AI-Agenten:
- Content Creator (Video-Skripte, Newsletter)
- Researcher (AI-Trends, Investments)
- Verifier (Qualitätssicherung)
- Communicator (Prompt-Optimization)

Deine Aufgaben:

1. TASK ORCHESTRATION
   - Zerlege komplexe Projekte in parallele Tasks
   - Weise Tasks den richtigen Agenten zu
   - Koordiniere Dependencies
   - Überwache Progress

2. PRIORITIZATION
   - Bewerte Tasks nach Impact
   - Berücksichtige das Moonshot-Ziel (100K Reach in 18 Monaten)
   - Optimiere für schnellen ROI
   - Identifiziere Critical Path

3. QUALITY GATES
   - Definiere Acceptance Criteria
   - Trigger Verification wo nötig
   - Eskaliere bei Qualitätsproblemen

4. RISK MANAGEMENT
   - Identifiziere Blocker frühzeitig
   - Schlage Mitigation Strategies vor
   - Track Technical Debt

5. REPORTING
   - Wöchentliche Progress Updates
   - Moonshot-Milestone-Tracking
   - KPI-Dashboards

OUTPUT: Strukturierte Action Plans mit klaren Owner, Deadlines, Dependencies.
"""

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main execution: Create action plan for a project

        Args:
            task: {
                "project": "Project description",
                "goals": ["Goal 1", "Goal 2"],
                "deadline": "Optional deadline",
                "constraints": ["Constraint 1"]
            }

        Returns:
            Detailed action plan with task distribution
        """
        project = task.get("project", "")
        goals = task.get("goals", [])
        deadline = task.get("deadline", "")
        constraints = task.get("constraints", [])

        planning_prompt = f"""
Erstelle einen detaillierten Action Plan:

PROJECT: {project}

GOALS:
{chr(10).join(f"- {g}" for g in goals)}

{f"DEADLINE: {deadline}" if deadline else ""}

{f"CONSTRAINTS: {chr(10).join(f'- {c}' for c in constraints)}" if constraints else ""}

Erstelle einen Action Plan mit:

1. TASK BREAKDOWN
   - Zerlege in parallele, unabhängige Tasks
   - Identifiziere Dependencies
   - Schätze Effort (S/M/L)

2. AGENT ASSIGNMENT
   - Weise jeden Task dem richtigen Agenten zu:
     * content_creator: Content-Erstellung
     * researcher: Research & Analysis
     * verifier: Quality Check
     * communicator: Prompt/Communication Optimization

3. EXECUTION STRATEGY
   - Parallel vs. Sequential
   - Critical Path
   - Quick Wins zuerst

4. SUCCESS METRICS
   - Wie messen wir Erfolg?
   - KPIs pro Task

5. RISK MITIGATION
   - Was könnte schiefgehen?
   - Backup-Pläne

Format als strukturiertes JSON:
{{
    "phases": [
        {{
            "name": "Phase 1",
            "tasks": [
                {{
                    "id": "task_1",
                    "description": "...",
                    "assigned_agent": "...",
                    "effort": "S/M/L",
                    "dependencies": [],
                    "success_criteria": "..."
                }}
            ]
        }}
    ],
    "critical_path": ["task_1", "task_3"],
    "risks": ["risk 1", "risk 2"],
    "estimated_completion": "X weeks"
}}
"""

        response = await self.think(planning_prompt)

        self.metrics["tasks_completed"] += 1
        self.active_tasks.append({
            "project": project,
            "plan": response,
            "created_at": datetime.now().isoformat()
        })

        return {
            "action_plan": response,
            "project": project,
            "status": "planned"
        }

    async def coordinate_agents(self, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Coordinate multiple agents working in parallel

        Args:
            tasks: List of tasks with agent assignments

        Returns:
            Coordination results
        """
        coordination_prompt = f"""
Koordiniere folgende parallele Tasks:

{chr(10).join(f"{i+1}. {t.get('description', '')} → {t.get('assigned_agent', 'unknown')}" for i, t in enumerate(tasks))}

Erstelle einen Koordinations-Plan:
1. Execution Order (was kann parallel, was sequential?)
2. Sync Points (wann müssen Agenten kommunizieren?)
3. Data Handoffs (welche Outputs werden zu Inputs?)
4. Timeline (realistische Zeitschätzung)

Format als actionable Roadmap.
"""

        response = await self.think(coordination_prompt)
        return {"coordination_plan": response}

    async def track_moonshot_progress(self) -> Dict[str, Any]:
        """
        Track progress towards the 18-month moonshot goal

        Returns:
            Progress report with recommendations
        """
        tracking_prompt = """
MOONSHOT GOAL: 100K Reach in 18 Monaten

AKTUELLER STATUS:
- Videos produziert: 0
- Newsletter versendet: 0
- Subscriber: 0
- Revenue: 0€

TARGETS:
- Monat 3: 100 Subscriber, 2 Videos
- Monat 6: 1K Subscriber, 6 Videos
- Monat 12: 10K Subscriber, 12 Videos
- Monat 18: 100K Subscriber, 18 Videos

Erstelle einen Progress Report:
1. Current Status (wo stehen wir?)
2. On Track? (sind wir im Plan?)
3. Gaps (was fehlt?)
4. Acceleration Opportunities (wo können wir beschleunigen?)
5. Next 30 Days (kritische Fokus-Bereiche)

Sei ehrlich und actionable.
"""

        response = await self.think(tracking_prompt)

        self.moonshot_progress.update({
            "last_check": datetime.now().isoformat(),
            "report": response
        })

        return self.moonshot_progress

    async def identify_blockers(self, context: str = "") -> List[str]:
        """
        Identify potential blockers in the current workflow

        Args:
            context: Current situation description

        Returns:
            List of identified blockers
        """
        blocker_prompt = f"""
Analysiere potenzielle Blocker:

{f"CONTEXT: {context}" if context else "CONTEXT: Starting J-Jeco AI Platform from scratch"}

Identifiziere:
1. Technical Blockers (Infrastruktur, APIs, Skills)
2. Resource Blockers (Zeit, Budget, Tools)
3. Knowledge Blockers (fehlende Expertise)
4. Process Blockers (unklare Workflows)
5. Strategic Blockers (falsche Priorisierung)

Für jeden Blocker:
- Severity (1-10)
- Impact auf Moonshot
- Vorgeschlagene Lösung

Format als Liste.
"""

        response = await self.think(blocker_prompt)
        blockers = response.split("\n")

        self.moonshot_progress["blockers"] = blockers
        return blockers

    async def weekly_standup(self) -> str:
        """
        Generate weekly progress report

        Returns:
            Formatted standup report
        """
        standup_prompt = """
Erstelle einen Weekly Standup Report:

COMPLETED THIS WEEK:
[Liste abgeschlossene Tasks]

IN PROGRESS:
[Aktuelle Tasks]

PLANNED NEXT WEEK:
[Nächste Prioritäten]

BLOCKERS:
[Aktuelle Hindernisse]

WINS:
[Erfolge & Learnings]

MOONSHOT PROGRESS:
[Status zum 18-Monats-Ziel]

Format als knappe, action-orientierte Updates.
"""

        return await self.think(standup_prompt)

    def get_active_tasks_summary(self) -> Dict[str, Any]:
        """Return summary of all active tasks"""
        return {
            "total_active": len(self.active_tasks),
            "total_completed": len(self.completed_tasks),
            "completion_rate": len(self.completed_tasks) / max(1, len(self.active_tasks) + len(self.completed_tasks)),
            "tasks": self.active_tasks[-5:]  # Last 5 tasks
        }
    
    async def delegate_code_generation(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Delegiert Code-Generierung an Code-Generation-Agent
        
        Nutzt Resource-Manager für intelligentes Routing:
        - OpenCode/Code-X für Standard-Code
        - Claude nur für Architektur-Entscheidungen
        
        Args:
            task: Task-Dictionary mit type, description, language, etc.
            
        Returns:
            Dict mit generiertem Code
        """
        # Prüfe ob Code-Generierung benötigt wird
        routing = self.route_task(task)
        
        if routing["tool"] in ["opencode", "codex"]:
            # Nutze lokale Tools
            return await self.use_local_tool(task)
        elif routing["tool"] == "claude":
            # Nutze Claude für komplexe/architektonische Tasks
            # Project Manager nutzt bereits Claude, daher kann er direkt denken
            prompt = f"""Generate {task.get('language', 'python')} code based on:

Description: {task.get('description', '')}
Context: {task.get('context', '')}

Provide clean, well-documented, production-ready code."""
            code = await self.think(prompt)
            return {
                "success": True,
                "code": code,
                "method": "claude",
                "priority": routing["priority"]
            }
        else:
            # Fallback zu lokalen Tools oder LLM
            return await self.use_local_tool(task)


# Quick test
async def test_project_manager():
    """Test the Project Manager Agent"""
    pm = ProjectManagerAgent()

    # Test: Plan the first tutorial video
    result = await pm.execute({
        "project": "Erstelle erstes Tutorial-Video: 'Homelab für Anfänger'",
        "goals": [
            "10-minütiges Erklärvideo",
            "Script für AI-Avatar",
            "Kinderleicht erklärt",
            "Publikationsreif"
        ],
        "deadline": "7 Tage",
        "constraints": [
            "Kein Budget für Tools",
            "Self-hosted preferred",
            "Deutsch"
        ]
    })

    print("=== ACTION PLAN ===")
    print(result["action_plan"])
    print("\n=== METRICS ===")
    print(pm.get_metrics())


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_project_manager())
