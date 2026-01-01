"""
Parallel Agent Executor
Enables concurrent execution of independent agent tasks for 3-4x speedup
"""

import asyncio
from typing import List, Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class AgentTask:
    """Represents a single agent task with dependencies"""
    task_id: str
    agent_type: str
    method: str
    params: Dict[str, Any]
    dependencies: List[str] = None
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[Any] = None
    error: Optional[str] = None

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


class ParallelAgentExecutor:
    """
    Execute multiple agent tasks in parallel with dependency management

    Example:
        executor = ParallelAgentExecutor(max_workers=4)

        tasks = [
            AgentTask(
                task_id="research_1",
                agent_type="ResearcherAgent",
                method="general_research",
                params={"query": "AI trends"},
                dependencies=[]
            ),
            AgentTask(
                task_id="content_1",
                agent_type="ContentCreatorAgent",
                method="create_video_script",
                params={"topic": "AI"},
                dependencies=["research_1"]  # Waits for research_1
            )
        ]

        results = await executor.execute_batch(tasks)
    """

    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.tasks: Dict[str, AgentTask] = {}

    def _build_dependency_graph(self, tasks: List[AgentTask]) -> List[List[AgentTask]]:
        """Build execution levels based on dependencies"""
        self.tasks = {task.task_id: task for task in tasks}
        levels = []
        completed = set()

        while len(completed) < len(tasks):
            # Find tasks with satisfied dependencies
            current_level = []
            for task in tasks:
                if task.task_id in completed:
                    continue

                deps_satisfied = all(dep in completed for dep in task.dependencies)
                if deps_satisfied:
                    current_level.append(task)

            if not current_level:
                # Circular dependency or error
                remaining = [t.task_id for t in tasks if t.task_id not in completed]
                raise ValueError(f"Circular dependency detected or missing tasks: {remaining}")

            levels.append(current_level)
            completed.update(task.task_id for task in current_level)

        return levels

    async def _execute_task(self, task: AgentTask) -> Dict[str, Any]:
        """Execute a single agent task"""
        try:
            logger.info(f"🚀 Executing {task.task_id}: {task.agent_type}.{task.method}")
            task.status = TaskStatus.RUNNING

            # Import agent dynamically
            module = __import__(f"agents.{task.agent_type.lower()}", fromlist=[task.agent_type])
            AgentClass = getattr(module, task.agent_type)

            # Execute agent method
            agent = AgentClass()
            method = getattr(agent, task.method)
            result = await method(task.params)

            task.status = TaskStatus.COMPLETED
            task.result = result

            logger.info(f"✅ Completed {task.task_id}")
            return {task.task_id: result}

        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            logger.error(f"❌ Failed {task.task_id}: {e}")
            return {task.task_id: {"error": str(e)}}

    async def execute_batch(self, tasks: List[AgentTask]) -> Dict[str, Any]:
        """
        Execute batch of agent tasks with dependency-aware parallelization

        Returns:
            Dict mapping task_id to results
        """
        levels = self._build_dependency_graph(tasks)
        results = {}

        logger.info(f"📊 Execution plan: {len(levels)} levels, {len(tasks)} tasks total")

        for level_idx, level in enumerate(levels, 1):
            logger.info(f"🔄 Level {level_idx}/{len(levels)}: {len(level)} tasks in parallel")

            # Execute all tasks in this level in parallel
            level_results = await asyncio.gather(*[
                self._execute_task(task) for task in level
            ])

            # Merge results
            for result in level_results:
                results.update(result)

        # Summary
        completed = sum(1 for t in tasks if t.status == TaskStatus.COMPLETED)
        failed = sum(1 for t in tasks if t.status == TaskStatus.FAILED)

        logger.info(f"✨ Batch complete: {completed} succeeded, {failed} failed")

        return results


# Example usage
async def main():
    """Example: Execute research and content creation in parallel"""
    executor = ParallelAgentExecutor(max_workers=4)

    tasks = [
        # Level 1: Independent research tasks (run in parallel)
        AgentTask(
            task_id="research_beta_communities",
            agent_type="ResearcherAgent",
            method="general_research",
            params={"query": "beta user communities for AI tools"},
            dependencies=[]
        ),
        AgentTask(
            task_id="research_trends",
            agent_type="ResearcherAgent",
            method="analyze_tech_trend",
            params={"trend": "local AI", "timeframe": "2026_Q1"},
            dependencies=[]
        ),

        # Level 2: Content creation (depends on research)
        AgentTask(
            task_id="create_landing_page",
            agent_type="ContentCreatorAgent",
            method="create_blog_post",
            params={"topic": "HexaHub Launch"},
            dependencies=["research_beta_communities", "research_trends"]
        ),

        # Level 1: Independent analysis
        AgentTask(
            task_id="init_roadmap",
            agent_type="AnalystAgent",
            method="analyze_dataset",
            params={"data": "roadmap_metrics.csv"},
            dependencies=[]
        )
    ]

    results = await executor.execute_batch(tasks)
    print("\n📋 Results:")
    for task_id, result in results.items():
        print(f"  {task_id}: {len(str(result))} chars")


if __name__ == "__main__":
    asyncio.run(main())
