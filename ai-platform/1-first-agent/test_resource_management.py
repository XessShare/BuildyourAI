"""
Tests für Resource Management und Routing-Logik
"""

import asyncio
import pytest
from agents.resource_manager import ResourceManager, TaskPriority
from agents.code_generation_agent import CodeGenerationAgent
from agents.base_agent import BaseAgent


class TestResourceManager:
    """Tests für Resource Manager"""
    
    def test_classify_task_privileged(self):
        """Test: Klassifizierung privilegierter Tasks"""
        rm = ResourceManager()
        
        task = {
            "type": "architectural_decision",
            "description": "Design system architecture for microservices",
            "complexity": "complex"
        }
        
        priority = rm.classify_task(task)
        assert priority == TaskPriority.PRIVILEGED
    
    def test_classify_task_standard(self):
        """Test: Klassifizierung Standard-Tasks"""
        rm = ResourceManager()
        
        task = {
            "type": "code_generation",
            "description": "Generate Python function for data processing",
            "complexity": "standard"
        }
        
        priority = rm.classify_task(task)
        assert priority == TaskPriority.STANDARD
    
    def test_classify_task_simple(self):
        """Test: Klassifizierung einfacher Tasks"""
        rm = ResourceManager()
        
        task = {
            "type": "fix_bugs",
            "description": "Fix typo in variable name",
            "complexity": "simple"
        }
        
        priority = rm.classify_task(task)
        assert priority == TaskPriority.SIMPLE
    
    def test_should_use_claude_privileged(self):
        """Test: Claude-Nutzung für privilegierte Tasks"""
        rm = ResourceManager()
        
        task = {
            "type": "architectural_decision",
            "description": "Design system architecture",
            "complexity": "complex"
        }
        
        decision = rm.should_use_claude(task)
        assert decision["use_claude"] is True
        assert "privileged" in decision["reason"].lower() or "quota" in decision["reason"].lower()
    
    def test_should_use_claude_standard(self):
        """Test: Keine Claude-Nutzung für Standard-Tasks"""
        rm = ResourceManager()
        
        task = {
            "type": "code_generation",
            "description": "Generate simple function",
            "complexity": "standard"
        }
        
        decision = rm.should_use_claude(task)
        assert decision["use_claude"] is False
    
    def test_route_task_privileged(self):
        """Test: Routing privilegierter Tasks zu Claude"""
        rm = ResourceManager()
        
        task = {
            "type": "architectural_decision",
            "description": "Design system architecture",
            "complexity": "complex"
        }
        
        routing = rm.route_task(task)
        assert routing["tool"] == "claude"
        assert routing["priority"] == TaskPriority.PRIVILEGED
    
    def test_route_task_standard_code(self):
        """Test: Routing Standard-Code-Generierung"""
        rm = ResourceManager()
        
        task = {
            "type": "code_generation",
            "description": "Generate Python function",
            "language": "python"
        }
        
        routing = rm.route_task(task)
        # Sollte opencode, codex oder gpt-mini sein (je nach Verfügbarkeit)
        assert routing["tool"] in ["opencode", "codex", "gpt-mini"]
    
    def test_quota_tracking(self):
        """Test: Quota-Tracking"""
        rm = ResourceManager()
        
        # Initial: Quota sollte verfügbar sein
        quota = rm.check_claude_quota()
        assert quota["available"] is True
        
        # Simuliere Nutzung
        for _ in range(5):
            rm.record_claude_usage()
        
        quota = rm.check_claude_quota()
        assert quota["daily_usage"] == 5
        assert quota["hourly_usage"] == 5


class TestCodeGenerationAgent:
    """Tests für Code-Generation-Agent"""
    
    @pytest.mark.asyncio
    async def test_generate_code_fallback(self):
        """Test: Code-Generierung mit LLM-Fallback"""
        agent = CodeGenerationAgent()
        
        task = {
            "type": "generate_code",
            "description": "Create a simple hello world function",
            "language": "python"
        }
        
        # Sollte funktionieren auch wenn OpenCode nicht verfügbar
        result = await agent.generate_code(task)
        
        assert "success" in result
        # Wenn LLM-Fallback aktiviert, sollte Code generiert werden
        if result.get("success"):
            assert "code" in result or "error" in result
    
    @pytest.mark.asyncio
    async def test_refactor_code(self):
        """Test: Code-Refactoring"""
        agent = CodeGenerationAgent()
        
        task = {
            "type": "refactor_code",
            "code_content": "def add(a,b): return a+b",
            "language": "python",
            "improvements": "Add type hints and documentation"
        }
        
        result = await agent.refactor_code(task)
        assert "success" in result
    
    @pytest.mark.asyncio
    async def test_review_code(self):
        """Test: Code-Review"""
        agent = CodeGenerationAgent()
        
        task = {
            "type": "review_code",
            "code_content": "def process(data): return data*2",
            "language": "python"
        }
        
        result = await agent.review_code(task)
        assert "success" in result
        if result.get("success"):
            assert "review" in result


class TestBaseAgentIntegration:
    """Tests für BaseAgent Resource-Management-Integration"""
    
    def test_should_use_claude_method(self):
        """Test: BaseAgent.should_use_claude()"""
        # Erstelle einen Test-Agent (nutze ProjectManager als Beispiel)
        from agents.project_manager_agent import ProjectManagerAgent
        
        agent = ProjectManagerAgent()
        
        task = {
            "type": "architectural_decision",
            "description": "Design system architecture",
            "complexity": "complex"
        }
        
        decision = agent.should_use_claude(task)
        assert "use_claude" in decision
        assert "reason" in decision
    
    def test_route_task_method(self):
        """Test: BaseAgent.route_task()"""
        from agents.project_manager_agent import ProjectManagerAgent
        
        agent = ProjectManagerAgent()
        
        task = {
            "type": "code_generation",
            "description": "Generate Python function",
            "language": "python"
        }
        
        routing = agent.route_task(task)
        assert "tool" in routing
        assert "priority" in routing
        assert "reason" in routing
    
    @pytest.mark.asyncio
    async def test_use_local_tool_method(self):
        """Test: BaseAgent.use_local_tool()"""
        from agents.project_manager_agent import ProjectManagerAgent
        
        agent = ProjectManagerAgent()
        
        task = {
            "type": "generate_code",
            "description": "Create a simple function",
            "language": "python"
        }
        
        result = await agent.use_local_tool(task)
        assert "success" in result or "code" in result or "error" in result


class TestIntegration:
    """Integration-Tests"""
    
    @pytest.mark.asyncio
    async def test_end_to_end_routing(self):
        """Test: End-to-End Routing von Task zu Tool"""
        from agents.project_manager_agent import ProjectManagerAgent
        
        agent = ProjectManagerAgent()
        
        # Test 1: Privilegierter Task → Claude
        privileged_task = {
            "type": "architectural_decision",
            "description": "Design microservices architecture",
            "complexity": "complex"
        }
        
        routing = agent.route_task(privileged_task)
        assert routing["tool"] == "claude"
        
        # Test 2: Standard Code-Generation → OpenCode/LLM
        code_task = {
            "type": "code_generation",
            "description": "Generate utility function",
            "language": "python"
        }
        
        routing = agent.route_task(code_task)
        assert routing["tool"] in ["opencode", "codex", "gpt-mini"]
    
    @pytest.mark.asyncio
    async def test_deployment_script_generation(self):
        """Test: Deployment-Script-Generierung"""
        from agents.deployment_orchestrator import DeploymentOrchestratorAgent
        
        agent = DeploymentOrchestratorAgent()
        
        task = {
            "type": "generate_code",
            "description": "Generate Docker Compose deployment script",
            "language": "yaml",
            "context": "Deploy to RTX1080",
            "complexity": "standard"
        }
        
        result = await agent.generate_deployment_script(task)
        assert "success" in result or "script" in result or "error" in result


if __name__ == "__main__":
    # Einfache Tests ohne pytest
    print("Running Resource Manager Tests...")
    
    rm = ResourceManager()
    
    # Test Klassifizierung
    task = {
        "type": "architectural_decision",
        "description": "Design system architecture",
        "complexity": "complex"
    }
    
    priority = rm.classify_task(task)
    print(f"Task Priority: {priority}")
    
    decision = rm.should_use_claude(task)
    print(f"Use Claude: {decision['use_claude']}")
    print(f"Reason: {decision['reason']}")
    
    routing = rm.route_task(task)
    print(f"Routing: {routing}")
    
    stats = rm.get_resource_stats()
    print(f"\nResource Stats:")
    print(f"  Claude Quota: {stats['claude']['quota_status']}")
    print(f"  OpenCode Available: {stats['local_tools']['opencode']['available']}")
    print(f"  CodeX Available: {stats['local_tools']['codex']['available']}")

