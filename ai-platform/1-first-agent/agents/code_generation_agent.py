"""
Code Generation Agent
Nutzt OpenCode/Code-X für Code-Generierung mit LLM-Fallback
"""

import subprocess
import logging
from typing import Dict, Any, Optional
from pathlib import Path
import tempfile
import json

from .base_agent import BaseAgent

import sys
sys.path.append(str(Path(__file__).parent.parent))
from config import (
    CODE_GENERATION_AGENT_CONFIG,
    OPENCODE_PATH,
    CODEX_PATH,
    DEFAULT_MODEL
)


class CodeGenerationAgent(BaseAgent):
    """
    Agent für Code-Generierung mit lokalen Tools (OpenCode/Code-X)
    Fallback zu LLM wenn Tools nicht verfügbar
    """

    def __init__(self, custom_config: Optional[Dict] = None):
        super().__init__("code_generation", custom_config or CODE_GENERATION_AGENT_CONFIG)
        self.opencode_path = OPENCODE_PATH
        self.codex_path = CODEX_PATH
        self.preferred_tool = self.config.get("preferred_tool", "opencode")
        self.fallback_to_llm = self.config.get("fallback_to_llm", True)
        self.timeout = self.config.get("timeout_seconds", 30)
        self.max_retries = self.config.get("max_retries", 2)
        
    def get_system_prompt(self) -> str:
        return """Du bist der Code Generation Agent im J-Jeco System.

Deine Spezialaufgaben:
1. CODE GENERATION - Erstelle sauberen, dokumentierten Code
2. REFACTORING - Verbessere bestehenden Code
3. BUG FIXES - Behebe Fehler effizient
4. CODE REVIEW - Prüfe Code auf Qualität

PRINZIPIEN:
- Sauberer, lesbarer Code
- Dokumentation und Kommentare
- Best Practices befolgen
- Testbarkeit sicherstellen
- Performance optimieren

Du nutzt primär lokale Tools (OpenCode/Code-X) für Code-Generierung,
fallback zu LLM wenn Tools nicht verfügbar sind.
"""

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main execution: Code-Generierung basierend auf Task-Type
        
        Args:
            task: {
                "type": "generate_code" | "refactor_code" | "review_code" | "fix_bugs",
                "description": "Was soll generiert werden",
                "language": "python" | "javascript" | etc.,
                "context": "Zusätzlicher Kontext",
                "file_path": "Optional: Pfad zu bestehender Datei"
            }
            
        Returns:
            Dict mit generiertem Code und Metadaten
        """
        task_type = task.get("type", "generate_code")
        
        if task_type == "generate_code":
            return await self.generate_code(task)
        elif task_type == "refactor_code":
            return await self.refactor_code(task)
        elif task_type == "review_code":
            return await self.review_code(task)
        elif task_type == "fix_bugs":
            return await self.fix_bugs(task)
        else:
            return await self.generate_code(task)
    
    async def generate_code(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generiert Code via OpenCode/Code-X oder LLM
        
        Args:
            task: Task-Dictionary mit description, language, etc.
            
        Returns:
            Dict mit generiertem Code
        """
        description = task.get("description", "")
        language = task.get("language", "python")
        context = task.get("context", "")
        
        # Versuche lokale Tools
        if self.preferred_tool == "opencode" and self.opencode_path:
            result = await self._use_opencode(description, language, context)
            if result.get("success"):
                return result
        
        if self.codex_path:
            result = await self._use_codex(description, language, context)
            if result.get("success"):
                return result
        
        # Fallback zu LLM
        if self.fallback_to_llm:
            return await self._generate_with_llm(description, language, context)
        
        return {
            "success": False,
            "error": "No code generation tools available and LLM fallback disabled",
            "code": ""
        }
    
    async def refactor_code(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Refactoriert bestehenden Code
        
        Args:
            task: Task mit file_path oder code_content
            
        Returns:
            Dict mit refactoriertem Code
        """
        file_path = task.get("file_path")
        code_content = task.get("code_content", "")
        improvements = task.get("improvements", "Improve code quality and readability")
        
        # Lade Code wenn file_path gegeben
        if file_path:
            try:
                code_content = Path(file_path).read_text()
            except Exception as e:
                return {
                    "success": False,
                    "error": f"Could not read file: {e}",
                    "code": ""
                }
        
        if not code_content:
            return {
                "success": False,
                "error": "No code content provided",
                "code": ""
            }
        
        # Versuche lokale Tools
        if self.opencode_path:
            result = await self._use_opencode(
                f"Refactor this code: {improvements}\n\n{code_content}",
                task.get("language", "python"),
                ""
            )
            if result.get("success"):
                return result
        
        # Fallback zu LLM
        if self.fallback_to_llm:
            prompt = f"""Refactor the following code with these improvements: {improvements}

Original Code:
```{task.get("language", "python")}
{code_content}
```

Provide the refactored code with explanations of changes."""
            
            refactored = await self.think(prompt)
            return {
                "success": True,
                "code": refactored,
                "method": "llm",
                "original_length": len(code_content),
                "refactored_length": len(refactored)
            }
        
        return {
            "success": False,
            "error": "Refactoring failed",
            "code": ""
        }
    
    async def review_code(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Reviewt Code auf Qualität und Probleme
        
        Args:
            task: Task mit code_content oder file_path
            
        Returns:
            Dict mit Review-Ergebnissen
        """
        file_path = task.get("file_path")
        code_content = task.get("code_content", "")
        
        if file_path:
            try:
                code_content = Path(file_path).read_text()
            except Exception as e:
                return {
                    "success": False,
                    "error": f"Could not read file: {e}"
                }
        
        if not code_content:
            return {
                "success": False,
                "error": "No code content provided"
            }
        
        # Nutze LLM für Code-Review (lokale Tools sind primär für Generation)
        prompt = f"""Review the following code for:
1. Code quality and readability
2. Potential bugs or issues
3. Performance improvements
4. Best practices
5. Security concerns

Code:
```{task.get("language", "python")}
{code_content}
```

Provide a structured review with specific recommendations."""
        
        review = await self.think(prompt)
        
        return {
            "success": True,
            "review": review,
            "code_length": len(code_content),
            "method": "llm"
        }
    
    async def fix_bugs(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Behebt Bugs im Code
        
        Args:
            task: Task mit code_content, error_message, etc.
            
        Returns:
            Dict mit gefixtem Code
        """
        code_content = task.get("code_content", "")
        error_message = task.get("error_message", "")
        file_path = task.get("file_path")
        
        if file_path:
            try:
                code_content = Path(file_path).read_text()
            except Exception as e:
                return {
                    "success": False,
                    "error": f"Could not read file: {e}"
                }
        
        if not code_content:
            return {
                "success": False,
                "error": "No code content provided"
            }
        
        # Versuche lokale Tools
        if self.opencode_path:
            prompt_text = f"Fix the following bug in this code:\n\nError: {error_message}\n\nCode:\n{code_content}"
            result = await self._use_opencode(
                prompt_text,
                task.get("language", "python"),
                ""
            )
            if result.get("success"):
                return result
        
        # Fallback zu LLM
        if self.fallback_to_llm:
            prompt = f"""Fix the following bug in the code:

Error Message:
{error_message}

Code:
```{task.get("language", "python")}
{code_content}
```

Provide the fixed code with explanation of the fix."""
            
            fixed = await self.think(prompt)
            return {
                "success": True,
                "code": fixed,
                "method": "llm",
                "original_code": code_content
            }
        
        return {
            "success": False,
            "error": "Bug fixing failed",
            "code": ""
        }
    
    async def _use_opencode(self, description: str, language: str, context: str) -> Dict[str, Any]:
        """Nutzt OpenCode CLI-Tool"""
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp:
                prompt = f"Language: {language}\n\nDescription: {description}\n\nContext: {context}"
                tmp.write(prompt)
                tmp_path = tmp.name
            
            cmd = [self.opencode_path, tmp_path]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            
            Path(tmp_path).unlink()
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "code": result.stdout,
                    "method": "opencode"
                }
            else:
                return {
                    "success": False,
                    "error": result.stderr,
                    "method": "opencode"
                }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "OpenCode timeout",
                "method": "opencode"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "method": "opencode"
            }
    
    async def _use_codex(self, description: str, language: str, context: str) -> Dict[str, Any]:
        """Nutzt Code-X CLI-Tool"""
        try:
            cmd = [self.codex_path, "generate", "--language", language, "--description", description]
            if context:
                cmd.extend(["--context", context])
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "code": result.stdout,
                    "method": "codex"
                }
            else:
                return {
                    "success": False,
                    "error": result.stderr,
                    "method": "codex"
                }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Code-X timeout",
                "method": "codex"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "method": "codex"
            }
    
    async def _generate_with_llm(self, description: str, language: str, context: str) -> Dict[str, Any]:
        """Generiert Code mit LLM (Fallback)"""
        prompt = f"""Generate {language} code based on the following description:

Description: {description}

{f'Context: {context}' if context else ''}

Provide clean, well-documented code that follows best practices."""
        
        code = await self.think(prompt)
        
        return {
            "success": True,
            "code": code,
            "method": "llm",
            "language": language
        }

