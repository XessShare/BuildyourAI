"""
J-Jeco AI Platform Configuration
Zentrale Konfiguration für alle AI-Agenten und Services
"""

import os
import shutil
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project Paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
OUTPUT_DIR = BASE_DIR / "output"

# Create directories if they don't exist
for dir_path in [DATA_DIR, LOGS_DIR, OUTPUT_DIR]:
    dir_path.mkdir(exist_ok=True)

# AI Model Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY", "")

# Optional AI Providers
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
COHERE_API_KEY = os.getenv("COHERE_API_KEY", "")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY", "")

# Default LLM Settings
DEFAULT_MODEL = "gpt-4o-mini"  # Current OpenAI model
CLAUDE_MODEL = "claude-3-5-sonnet-20241022"
GEMINI_MODEL = "gemini-2.0-flash-exp"
PERPLEXITY_MODEL = "llama-3.1-sonar-large-128k-online"
TEMPERATURE = 0.7
MAX_TOKENS = 4000

# Content Generation API Keys
HEYGEN_API_KEY = os.getenv("HEYGEN_API_KEY", "")
DID_API_KEY = os.getenv("DID_API_KEY", "")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY", "")

# Agent Configuration
# Note: Models can be: gpt-4-turbo-preview, claude-3-5-sonnet-20241022, gemini-2.0-flash-exp, etc.
AGENT_CONFIG = {
    "project_manager": {
        "model": CLAUDE_MODEL,
        "temperature": 0.3,
        "role": "Strategic project coordinator and task orchestrator"
    },
    "content_creator": {
        "model": DEFAULT_MODEL,
        "temperature": 0.8,
        "role": "Creative content generator for tutorials and newsletters",
        "specialties": ["video_scripts", "newsletter_content", "blog_posts"]
    },
    "researcher": {
        "model": DEFAULT_MODEL,  # Fallback model when Perplexity unavailable
        "temperature": 0.4,
        "role": "Deep research on AI models, tech trends, and investments",
        "use_perplexity": True,  # Flag for online search capability
        "perplexity_model": PERPLEXITY_MODEL  # Actual Perplexity model to use
    },
    "verifier": {
        "model": DEFAULT_MODEL,
        "temperature": 0.2,
        "role": "Fact-checking and quality assurance"
    },
    "communicator": {
        "model": CLAUDE_MODEL,
        "temperature": 0.5,
        "role": "Prompt optimization and communication enhancement"
    },
    "analyst": {
        "model": DEFAULT_MODEL,  # Using GPT-4o-mini for reliable analysis
        "temperature": 0.3,
        "role": "Data analysis and insights extraction"
    },
    # CD/CI Deployment Agents
    "deployment_orchestrator": {
        "model": CLAUDE_MODEL,
        "temperature": 0.3,
        "role": "CD/CI Deployment Orchestrator",
        "systems": ["vps", "thinkpad", "rtx1080"],
        "location": "multi-system"
    },
    "webhook_handler": {
        "model": DEFAULT_MODEL,
        "temperature": 0.2,
        "role": "Webhook reception and routing",
        "location": "vps"
    },
    "testing_agent": {
        "model": DEFAULT_MODEL,
        "temperature": 0.3,
        "role": "Automated testing and validation",
        "location": "thinkpad"
    }
}

# Vector Database Configuration
CHROMA_DB_PATH = str(DATA_DIR / "chroma_db")
COLLECTION_NAME = "j_jeco_knowledge"

# Content Generation Settings
VIDEO_SCRIPTS = {
    "target_duration_minutes": 10,
    "language": "de",
    "style": "educational_friendly",
    "audience": "non_technical"
}

NEWSLETTER_CONFIG = {
    "frequency": "weekly",
    "sections": [
        "ai_updates",
        "homelab_tips",
        "investment_ideas",
        "community_spotlight"
    ],
    "max_length_words": 800
}

# Self-Hosted Services
PROXMOX_HOST = "192.168.17.1"
SERVICES = {
    "portainer": f"http://{PROXMOX_HOST}:9000",
    "grafana": f"http://{PROXMOX_HOST}:3000",
    "prometheus": f"http://{PROXMOX_HOST}:9090"
}

# Notification Settings
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# Verification Thresholds
QUALITY_THRESHOLDS = {
    "factual_accuracy": 0.85,
    "actuality_score": 0.80,
    "simplification_score": 0.75,
    "value_score": 0.80
}

# Moonshot Metrics
KPI_TARGETS = {
    "month_3": {"subscribers": 100, "videos": 2, "newsletters": 4},
    "month_6": {"subscribers": 1000, "videos": 6, "newsletters": 12},
    "month_12": {"subscribers": 10000, "videos": 12, "newsletters": 24},
    "month_18": {"subscribers": 100000, "videos": 18, "newsletters": 36}
}

# Code Generation Tools Configuration
# OpenCode and Code-X are local CLI tools for code generation
OPENCODE_PATH = os.getenv("OPENCODE_PATH", shutil.which("opencode") or "")
CODEX_PATH = os.getenv("CODEX_PATH", shutil.which("codex") or shutil.which("code-x") or "")

# Claude Resource Management Policy
# Claude is reserved for privileged tasks only
CLAUDE_RESOURCE_POLICY = {
    "enabled": True,
    "privileged_task_types": [
        "architectural_decisions",
        "complex_problem_solving",
        "strategic_planning",
        "system_design",
        "critical_reasoning"
    ],
    "daily_quota": int(os.getenv("CLAUDE_DAILY_QUOTA", "50")),  # Max requests per day
    "hourly_quota": int(os.getenv("CLAUDE_HOURLY_QUOTA", "10")),  # Max requests per hour
    "fallback_model": DEFAULT_MODEL,  # Fallback if quota exceeded
    "require_approval": False  # Set to True for manual approval of Claude usage
}

# Code Generation Agent Configuration
CODE_GENERATION_AGENT_CONFIG = {
    "model": DEFAULT_MODEL,  # Fallback model
    "temperature": 0.3,
    "role": "Code generation and refactoring using local tools",
    "preferred_tool": "opencode",  # Preferred tool: opencode, codex, or llm
    "fallback_to_llm": True,  # Fallback to LLM if tools unavailable
    "timeout_seconds": 30,  # Timeout for CLI tool execution
    "max_retries": 2
}

# Task Classification Rules
TASK_CLASSIFICATION = {
    "PRIVILEGED": {
        "keywords": ["architecture", "design", "strategic", "complex", "critical", "system"],
        "use_claude": True,
        "priority": 1
    },
    "STANDARD": {
        "keywords": ["code", "generate", "refactor", "implement", "create"],
        "use_opencode": True,
        "priority": 2
    },
    "SIMPLE": {
        "keywords": ["fix", "review", "simple", "quick", "minor"],
        "use_gpt_mini": True,
        "priority": 3
    }
}

