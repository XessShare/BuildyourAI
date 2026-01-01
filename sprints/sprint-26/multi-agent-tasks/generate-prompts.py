#!/usr/bin/env python3
"""
Sprint 26 - Automatic Prompt Generator
Generates all 24 focused task prompts from existing agent files using the template
"""

import re
from pathlib import Path

# Paths
SPRINT_DIR = Path("/home/fitna/homelab/sprints/sprint-26")
AGENT_PROMPTS_DIR = SPRINT_DIR / "agent-prompts"
OUTPUT_DIR = SPRINT_DIR / "agent-prompts-optimized"
TEMPLATE_FILE = SPRINT_DIR / "shared-context/task-prompt-template.md"

# Agent configuration
AGENTS = {
    "01-content-creator": {
        "source": "ContentCreatorAgent.md",
        "agent_type": "ContentCreatorAgent",
        "model": "GPT-4o-mini",
        "story_points": 3.0,
        "tasks": [
            {"id": 1, "title": "Landing Page Copy", "output": "/home/fitna/homelab/shared/content/sprint-26/landing-page-copy.md"},
            {"id": 2, "title": "YouTube Video Script", "output": "/home/fitna/homelab/shared/content/sprint-26/youtube-script-01-hexahub-intro.md"},
            {"id": 3, "title": "Social Media Templates", "output": "/home/fitna/homelab/shared/content/sprint-26/social-media-templates.csv"},
            {"id": 4, "title": "Newsletter Setup", "output": "/home/fitna/homelab/shared/content/sprint-26/newsletter-setup-guide.md"},
        ]
    },
    "02-researcher": {
        "source": "ResearcherAgent.md",
        "agent_type": "ResearcherAgent",
        "model": "Perplexity",
        "story_points": 3.5,
        "tasks": [
            {"id": 1, "title": "Competitor Analysis", "output": "/home/fitna/homelab/shared/research/sprint-26/competitor-analysis.md"},
            {"id": 2, "title": "Beta Communities Research", "output": "/home/fitna/homelab/shared/research/sprint-26/beta-communities.csv"},
            {"id": 3, "title": "Trending Topics Report", "output": "/home/fitna/homelab/shared/research/sprint-26/trending-topics-report.md"},
            {"id": 4, "title": "Market Research Report", "output": "/home/fitna/homelab/shared/research/sprint-26/market-research-report.md"},
        ]
    },
    "03-analyst": {
        "source": None,  # Will create from scratch
        "agent_type": "AnalystAgent",
        "model": "GPT-4o-mini",
        "story_points": 2.0,
        "tasks": [
            {"id": 1, "title": "Roadmap Tracker Initialization", "output": "/home/fitna/homelab/shared/dashboards/1m-roadmap-tracker.md"},
            {"id": 2, "title": "Sprint Metrics Dashboard", "output": "/home/fitna/homelab/shared/dashboards/sprint-26-metrics.json"},
            {"id": 3, "title": "KPI Baseline Definition", "output": "/home/fitna/homelab/shared/dashboards/kpi-baseline-sprint-26.md"},
            {"id": 4, "title": "Daily Progress Tracking", "output": "/home/fitna/homelab/shared/dashboards/daily-progress-tracker.sh"},
        ]
    },
    "04-deployment-orchestrator": {
        "source": "DeploymentOrchestrator.md",
        "agent_type": "DeploymentOrchestrator",
        "model": "Claude Sonnet",
        "story_points": 6.0,
        "tasks": [
            {"id": 1, "title": "CI/CD Pipeline Setup", "output": "/home/fitna/homelab/.github/workflows/hexahub-ci-cd.yml"},
            {"id": 2, "title": "Staging Environment", "output": "/home/fitna/homelab/infrastructure/docker-compose.staging.yml"},
            {"id": 3, "title": "Monitoring Setup", "output": "/home/fitna/homelab/infrastructure/monitoring/prometheus.yml"},
            {"id": 4, "title": "K3s Readiness Check", "output": "/home/fitna/homelab/infrastructure/k8s/hexahub-chart/"},
        ]
    },
    "05-verifier": {
        "source": None,  # Will create from scratch
        "agent_type": "VerifierAgent",
        "model": "GPT-4o-mini",
        "story_points": 2.0,
        "tasks": [
            {"id": 1, "title": "Pytest Baseline", "output": "/home/fitna/homelab/tests/test_baseline.py"},
            {"id": 2, "title": "CodeRabbit Integration", "output": "/home/fitna/homelab/.coderabbit.yaml"},
            {"id": 3, "title": "QA Checklist", "output": "/home/fitna/homelab/tests/qa-checklist-mvp.md"},
            {"id": 4, "title": "Security Scan", "output": "/home/fitna/homelab/tests/security-scan-results.md"},
        ]
    },
    "06-project-manager": {
        "source": None,  # Will create from scratch
        "agent_type": "ProjectManagerAgent",
        "model": "Claude Sonnet",
        "story_points": 1.5,
        "tasks": [
            {"id": 1, "title": "Sprint Planning Completion", "output": "/home/fitna/homelab/sprints/sprint-26/SPRINT_PLAN.md"},
            {"id": 2, "title": "Daily Standup Automation", "output": "/home/fitna/homelab/sprints/sprint-26/daily-standup-automation.sh"},
            {"id": 3, "title": "Kanban Board Updates", "output": "/home/fitna/homelab/sprints/sprint-26/SPRINT_BOARD.md"},
            {"id": 4, "title": "Blocker Tracking System", "output": "/home/fitna/homelab/sprints/sprint-26/blockers.md"},
        ]
    },
}


def load_template():
    """Load the universal template"""
    with open(TEMPLATE_FILE, 'r') as f:
        return f.read()


def extract_task_info(source_file, task_num):
    """Extract task information from existing agent file"""
    if not source_file.exists():
        return None

    with open(source_file, 'r') as f:
        content = f.read()

    # Try to find task section (this is a simple extraction, may need refinement)
    task_pattern = rf"###\s+{task_num}\.\s+(.*?)\n(.*?)(?=###|\Z)"
    match = re.search(task_pattern, content, re.DOTALL)

    if match:
        return {
            "title": match.group(1).strip(),
            "content": match.group(2).strip()
        }
    return None


def generate_prompt(agent_dir, agent_config, task):
    """Generate a single task prompt from template"""
    template = load_template()

    # Fill placeholders
    prompt = template.replace("[Agent Name]", agent_config["agent_type"])
    prompt = prompt.replace("[AgentType]", agent_config["agent_type"])
    prompt = prompt.replace("[LLM Model]", agent_config["model"])
    prompt = prompt.replace("[Task N]", str(task["id"]))
    prompt = prompt.replace("[Specific Task Title]", task["title"])
    prompt = prompt.replace("[N]", str(task["id"]))
    prompt = prompt.replace("[Title]", task["title"])
    prompt = prompt.replace("/path/to/specific/file.ext", task["output"])
    prompt = prompt.replace("/path/to/output/file.ext", task["output"])

    # Set story points per task (divide total by 4)
    sp_per_task = agent_config["story_points"] / 4
    prompt = prompt.replace("Story Points: X", f"Story Points: {sp_per_task:.1f}")

    # Set priority based on story points
    if agent_config["story_points"] >= 5:
        priority = "HIGH"
    elif agent_config["story_points"] >= 2:
        priority = "MEDIUM"
    else:
        priority = "LOW"
    prompt = prompt.replace("Priority: HIGH/MEDIUM/LOW", f"Priority: {priority}")

    # Set deadline based on agent type
    if "content" in agent_dir.lower() or "researcher" in agent_dir.lower():
        deadline = "2025-12-30"  # Tag 3
    elif "deployment" in agent_dir.lower():
        deadline = "2025-12-31"  # Tag 5
    else:
        deadline = "2026-01-11"  # Sprint end
    prompt = prompt.replace("Deadline: YYYY-MM-DD", f"Deadline: {deadline}")

    return prompt


def main():
    """Generate all 24 task prompts"""
    print("Sprint 26 Prompt Generator")
    print("=" * 70)

    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)

    total_generated = 0

    for agent_dir, agent_config in AGENTS.items():
        print(f"\nGenerating prompts for: {agent_dir}")
        print("-" * 70)

        # Create agent directory
        agent_output_dir = OUTPUT_DIR / agent_dir
        agent_output_dir.mkdir(exist_ok=True)

        # Generate each task
        for task in agent_config["tasks"]:
            # Sanitize filename
            safe_title = task['title'].lower().replace(' ', '-').replace('/', '-')
            task_file = agent_output_dir / f"task-{task['id']}-{safe_title}.md"

            # Generate prompt
            prompt = generate_prompt(agent_dir, agent_config, task)

            # Save
            with open(task_file, 'w') as f:
                f.write(prompt)

            print(f"  ✓ Generated: {task_file.name}")
            total_generated += 1

    print("\n" + "=" * 70)
    print(f"SUCCESS: Generated {total_generated} task prompts!")
    print(f"Output directory: {OUTPUT_DIR}")
    print("\nNext steps:")
    print("1. Review generated prompts")
    print("2. Customize task-specific requirements")
    print("3. Add deliverable descriptions")
    print("4. Validate success criteria")


if __name__ == "__main__":
    main()
