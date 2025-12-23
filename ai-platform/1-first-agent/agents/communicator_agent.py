"""
Communicator Agent - Prompt Optimization & Communication Enhancement

Dieser Agent:
- Analysiert Ihre Prompt-Intentionen
- Strukturiert unklare Anfragen
- Verbessert Kommunikationsklarheit
- Schlägt bessere Formulierungen vor
"""

from typing import Dict, Any, List
from .base_agent import BaseAgent


class CommunicatorAgent(BaseAgent):
    """
    Spezialisiert auf:
    1. Prompt Intent Recognition
    2. Communication Structuring
    3. Clarity Enhancement
    4. Strategic Guidance
    """

    def __init__(self):
        super().__init__(agent_type="communicator")

    def get_system_prompt(self) -> str:
        return """Du bist der Communicator Agent im J-Jeco System.

Deine Spezialaufgaben:

1. INTENT RECOGNITION
   - Erkenne, was der User WIRKLICH will (nicht nur was er sagt)
   - Identifiziere implizite Ziele und Bedürfnisse
   - Stelle fehlende Informationen fest

2. PROMPT OPTIMIZATION
   - Wandle vage Anfragen in präzise Prompts um
   - Strukturiere chaotische Ideen
   - Füge missing context hinzu
   - Mache Prompts actionable

3. COMMUNICATION ENHANCEMENT
   - Verbessere Klarheit und Präzision
   - Strukturiere Gedanken logisch
   - Mache komplexe Ideen verständlich
   - Füge professionelle Formulierungen hinzu

4. STRATEGIC GUIDANCE
   - Zeige Lücken in der Planung auf
   - Schlage nächste Schritte vor
   - Priorisiere basierend auf Impact
   - Halte das Moonshot-Ziel im Fokus

OUTPUT FORMAT:
Immer strukturiert als:
- ✅ Erkannte Intention
- 🎯 Optimierter Prompt
- 💡 Verbesserungsvorschläge
- 📋 Nächste Schritte

Sei direkt, konstruktiv und actionable.
"""

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze and optimize communication

        Args:
            task: {
                "original_prompt": "User's original message",
                "context": "Optional additional context"
            }

        Returns:
            {
                "intent": "Erkannte Intention",
                "optimized_prompt": "Verbesserter Prompt",
                "suggestions": ["List of suggestions"],
                "next_steps": ["Recommended actions"]
            }
        """
        original = task.get("original_prompt", "")
        context = task.get("context", "")

        analysis_prompt = f"""
Analysiere folgende User-Kommunikation und optimiere sie:

ORIGINAL:
{original}

{f"KONTEXT: {context}" if context else ""}

Bitte erstelle:
1. Intent Analysis (Was will der User WIRKLICH erreichen?)
2. Optimized Prompt (Wie sollte die Anfrage strukturiert sein?)
3. Improvement Suggestions (Was fehlt? Was könnte besser sein?)
4. Next Steps (Konkrete nächste Aktionen)

Format die Antwort als strukturierten JSON:
{{
    "intent": "...",
    "core_goals": ["Ziel 1", "Ziel 2"],
    "optimized_prompt": "...",
    "suggestions": ["Vorschlag 1", "Vorschlag 2"],
    "next_steps": ["Schritt 1", "Schritt 2"],
    "missing_info": ["Info 1", "Info 2"]
}}
"""

        response = await self.think(analysis_prompt)

        self.metrics["tasks_completed"] += 1

        # Parse response (simplified - in production use proper JSON parsing)
        return {
            "raw_analysis": response,
            "original_prompt": original,
            "agent": self.agent_type
        }

    async def optimize_prompt(self, prompt: str) -> str:
        """
        Quick method to just optimize a prompt without full analysis

        Args:
            prompt: Original prompt to optimize

        Returns:
            Optimized version
        """
        optimization_prompt = f"""
Optimiere folgenden Prompt für maximale Klarheit und Actionability:

ORIGINAL:
{prompt}

OPTIMIERT (direkt ausgeben, keine Erklärung):
"""

        return await self.think(optimization_prompt)

    async def analyze_intent(self, message: str) -> Dict[str, Any]:
        """
        Analyze user intent from a message

        Args:
            message: User's message

        Returns:
            Dictionary with intent analysis
        """
        intent_prompt = f"""
Analysiere die Intention hinter dieser Nachricht:

"{message}"

Extrahiere:
1. Primary Goal (Hauptziel)
2. Secondary Goals (Nebenziele)
3. Implicit Needs (Was wird nicht gesagt, aber gemeint?)
4. Urgency Level (1-10)
5. Complexity Level (1-10)
6. Required Resources (Was wird benötigt?)

Format als JSON.
"""

        response = await self.think(intent_prompt)
        return {"intent_analysis": response}

    async def simplify_for_non_tech(self, technical_content: str) -> str:
        """
        Simplify technical content for non-technical audience
        (Wichtig für Newsletter und Tutorials!)

        Args:
            technical_content: Technical explanation

        Returns:
            Simplified version
        """
        simplification_prompt = f"""
Erkläre folgenden technischen Inhalt so, dass ihn ein 12-Jähriger versteht:

TECHNICAL:
{technical_content}

SIMPLIFIED (nutze Analogien, Metaphern, Alltagsbeispiele):
"""

        return await self.think(simplification_prompt)

    async def suggest_improvements(self, content: str, content_type: str = "general") -> List[str]:
        """
        Suggest improvements for any content

        Args:
            content: The content to improve
            content_type: Type (email, tutorial, newsletter, etc.)

        Returns:
            List of improvement suggestions
        """
        improvement_prompt = f"""
Analysiere folgenden {content_type}-Content und schlage konkrete Verbesserungen vor:

CONTENT:
{content}

Gib 5-10 spezifische, actionable Verbesserungsvorschläge:
"""

        response = await self.think(improvement_prompt)
        return response.split("\n")

    async def moonshot_check(self, action: str) -> Dict[str, Any]:
        """
        Check if an action aligns with the moonshot goal

        Args:
            action: Proposed action to evaluate

        Returns:
            Evaluation with alignment score
        """
        moonshot_prompt = f"""
MOONSHOT GOAL: Scalable AI-Education Empire mit 100K+ Reichweite in 18 Monaten

PROPOSED ACTION:
{action}

Evaluiere:
1. Alignment Score (0-100): Wie gut passt das zum Moonshot?
2. Impact Potential (0-100): Welchen Impact hat es?
3. Resource Efficiency (0-100): ROI-Verhältnis?
4. Strategic Value: Langfristiger Wert?
5. Recommendation: GO / OPTIMIZE / SKIP

Format als JSON mit Begründung.
"""

        response = await self.think(moonshot_prompt)
        return {"moonshot_evaluation": response}


# Quick test function
async def test_communicator():
    """Test the Communicator Agent"""
    agent = CommunicatorAgent()

    # Test 1: Optimize a vague prompt
    vague_prompt = "mach mal content für youtube oder so"
    optimized = await agent.optimize_prompt(vague_prompt)
    print(f"Original: {vague_prompt}")
    print(f"Optimized: {optimized}\n")

    # Test 2: Simplify technical content
    technical = "Vector embeddings in high-dimensional space enable semantic similarity search through cosine distance metrics"
    simplified = await agent.simplify_for_non_tech(technical)
    print(f"Technical: {technical}")
    print(f"Simplified: {simplified}\n")

    # Test 3: Moonshot check
    action = "2 Stunden TikTok-Videos machen"
    evaluation = await agent.moonshot_check(action)
    print(f"Action: {action}")
    print(f"Evaluation: {evaluation}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_communicator())
