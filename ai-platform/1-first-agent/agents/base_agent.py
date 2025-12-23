"""
Base Agent Framework
Alle spezialisierten Agenten erben von dieser Klasse
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging
from pathlib import Path

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate

import sys
sys.path.append(str(Path(__file__).parent.parent))
from config import AGENT_CONFIG, LOGS_DIR, OPENAI_API_KEY, ANTHROPIC_API_KEY


class BaseAgent(ABC):
    """
    Basis-Klasse für alle AI-Agenten im J-Jeco System

    Features:
    - Standardisierte LLM-Integration
    - Logging & Monitoring
    - Memory Management
    - Error Handling
    """

    def __init__(self, agent_type: str, custom_config: Optional[Dict] = None):
        """
        Initialisiert einen neuen Agenten

        Args:
            agent_type: Type aus AGENT_CONFIG (z.B. "project_manager")
            custom_config: Optional custom settings
        """
        self.agent_type = agent_type
        self.config = AGENT_CONFIG.get(agent_type, {})

        if custom_config:
            self.config.update(custom_config)

        # Setup Logging
        self.logger = self._setup_logging()

        # Initialize LLM
        self.llm = self._initialize_llm()

        # Memory for conversation history
        self.memory: List[Dict[str, Any]] = []

        # Metrics
        self.metrics = {
            "tasks_completed": 0,
            "tokens_used": 0,
            "errors": 0,
            "created_at": datetime.now().isoformat()
        }

        self.logger.info(f"{self.agent_type} agent initialized")

    def _setup_logging(self) -> logging.Logger:
        """Setup dedicated logger for this agent"""
        logger = logging.getLogger(f"agent.{self.agent_type}")
        logger.setLevel(logging.INFO)

        # File handler
        log_file = LOGS_DIR / f"{self.agent_type}.log"
        handler = logging.FileHandler(log_file)
        handler.setFormatter(
            logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )
        logger.addHandler(handler)

        return logger

    def _initialize_llm(self):
        """Initialize the appropriate LLM based on model config"""
        model = self.config.get("model", "gpt-4-turbo-preview")
        temperature = self.config.get("temperature", 0.7)

        if "claude" in model.lower():
            return ChatAnthropic(
                model=model,
                anthropic_api_key=ANTHROPIC_API_KEY,
                temperature=temperature
            )
        else:
            return ChatOpenAI(
                model=model,
                openai_api_key=OPENAI_API_KEY,
                temperature=temperature
            )

    def add_to_memory(self, role: str, content: str):
        """Add message to agent's memory"""
        self.memory.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })

    def get_system_prompt(self) -> str:
        """
        Return the system prompt for this agent
        Override in subclasses for custom behavior
        """
        role = self.config.get("role", "AI Assistant")
        return f"""Du bist ein spezialisierter AI-Agent im J-Jeco System.

Deine Rolle: {role}

Grundprinzipien:
1. Sei präzise und actionable
2. Priorisiere Qualität über Quantität
3. Denke in Systemen und Prozessen
4. Sei proaktiv bei Verbesserungsvorschlägen
5. Kommuniziere klar und strukturiert

Kontext: Du arbeitest in einem parallelen Agenten-System, das Content-Erstellung,
Newsletter-Automation, Research und Projektmanagement kombiniert. Dein Output wird
von anderen Agenten weiterverarbeitet - daher ist Struktur und Konsistenz wichtig.
"""

    @abstractmethod
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main execution method - must be implemented by subclasses

        Args:
            task: Dictionary mit task details

        Returns:
            Dictionary mit results
        """
        pass

    async def think(self, prompt: str, context: Optional[str] = None) -> str:
        """
        Core thinking/reasoning method using LLM

        Args:
            prompt: The main prompt/question
            context: Optional additional context

        Returns:
            LLM response as string
        """
        try:
            messages = [
                SystemMessage(content=self.get_system_prompt())
            ]

            if context:
                messages.append(HumanMessage(content=f"Kontext: {context}"))

            messages.append(HumanMessage(content=prompt))

            response = await self.llm.ainvoke(messages)

            # Update metrics
            self.metrics["tokens_used"] += len(response.content.split())

            # Store in memory
            self.add_to_memory("user", prompt)
            self.add_to_memory("assistant", response.content)

            return response.content

        except Exception as e:
            self.logger.error(f"Error in think(): {str(e)}")
            self.metrics["errors"] += 1
            raise

    def get_metrics(self) -> Dict[str, Any]:
        """Return current agent metrics"""
        return {
            **self.metrics,
            "memory_size": len(self.memory),
            "uptime": (datetime.now() - datetime.fromisoformat(self.metrics["created_at"])).seconds
        }

    def clear_memory(self):
        """Clear agent's conversation memory"""
        self.memory = []
        self.logger.info("Memory cleared")

    def __repr__(self):
        return f"<{self.__class__.__name__}(type={self.agent_type}, tasks={self.metrics['tasks_completed']})>"
