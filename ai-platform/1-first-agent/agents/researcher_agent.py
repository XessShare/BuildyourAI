"""
Researcher Agent - Deep Research on AI, Tech Trends, and Investments

Dieser Agent:
- Nutzt Perplexity für real-time Online-Recherche
- Recherchiert AI-Models, Tech-Trends, Investment-Opportunities
- Verifiziert Fakten und sammelt aktuelle Informationen
- Erstellt Research-Reports
"""

from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent
import requests
import os


class ResearcherAgent(BaseAgent):
    """
    Spezialisiert auf tiefe Recherche mit Online-Zugriff
    
    Features:
    1. Real-time research via Perplexity
    2. AI model comparison & analysis
    3. Tech trend identification
    4. Investment opportunity research
    5. Fact verification
    """
    
    def __init__(self):
        super().__init__(agent_type="researcher")
        self.perplexity_api_key = os.getenv("PERPLEXITY_API_KEY", "")
        self.perplexity_url = "https://api.perplexity.ai/chat/completions"
    
    def get_system_prompt(self) -> str:
        return """Du bist der Researcher Agent im J-Jeco System.

Deine Mission: Tiefe, akkurate Recherche zu AI, Tech-Trends und Investment-Opportunities.

RESEARCH-PRINZIPIEN:

1. AKTUALITÄT
   - Nutze immer die neuesten verfügbaren Informationen
   - Überprüfe Veröffentlichungsdaten
   - Bevorzuge primäre Quellen
   - Markiere veraltete Infos klar

2. GENAUIGKEIT
   - Verifiziere Fakten aus mehreren Quellen
   - Unterscheide zwischen Fakten und Spekulationen
   - Zitiere Quellen wenn möglich
   - Gib Unsicherheiten zu

3. TIEFE
   - Gehe über Oberflächliches hinaus
   - Verstehe technische Details
   - Analysiere Implikationen
   - Identifiziere Zusammenhänge

4. RELEVANZ
   - Fokus auf praktischen Nutzen
   - Was bedeutet das für den User?
   - Welche Handlungsoptionen gibt es?
   - Welche Trends sind wichtig?

5. STRUKTUR
   - Klare Gliederung
   - Executive Summary
   - Detaillierte Findings
   - Actionable Insights

SPEZIAL-FOKUS:
- AI Models & Capabilities
- Self-Hosting & Homelab Tech
- Investment-Opportunities in AI/Tech
- Emerging Trends

OUTPUT: Strukturierte Research-Reports mit Quellen, Insights und Empfehlungen.
"""
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main execution: Research based on task type
        
        Args:
            task: {
                "type": "model_research" | "trend_analysis" | "investment_research",
                "query": "Research question",
                "depth": "quick" | "medium" | "deep",
                "focus_areas": ["area1", "area2"]
            }
            
        Returns:
            Research report with findings and sources
        """
        research_type = task.get("type", "general_research")
        
        if research_type == "model_research":
            return await self.research_ai_model(task)
        elif research_type == "trend_analysis":
            return await self.analyze_tech_trend(task)
        elif research_type == "investment_research":
            return await self.research_investment_opportunity(task)
        else:
            return await self.general_research(task)
    
    async def research_with_perplexity(
        self,
        query: str,
        system_context: str = ""
    ) -> Dict[str, Any]:
        """
        Use Perplexity API for real-time research
        
        Args:
            query: Research question
            system_context: Additional context for the search
            
        Returns:
            Research results with sources
        """
        if not self.perplexity_api_key:
            # Fallback to regular LLM if no Perplexity key
            return await self._fallback_research(query, system_context)
        
        headers = {
            "Authorization": f"Bearer {self.perplexity_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama-3.1-sonar-large-128k-online",
            "messages": [
                {
                    "role": "system",
                    "content": system_context or self.get_system_prompt()
                },
                {
                    "role": "user",
                    "content": query
                }
            ],
            "temperature": 0.2,
            "max_tokens": 4000
        }
        
        try:
            response = requests.post(
                self.perplexity_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            
            return {
                "content": content,
                "sources": data.get("citations", []),
                "model": "perplexity-online"
            }
        except Exception as e:
            self.logger.error(f"Perplexity API error: {e}")
            return await self._fallback_research(query, system_context)
    
    async def _fallback_research(
        self,
        query: str,
        context: str = ""
    ) -> Dict[str, Any]:
        """Fallback to regular LLM when Perplexity is unavailable"""
        prompt = f"{context}\n\n{query}" if context else query
        response = await self.think(prompt)
        
        return {
            "content": response,
            "sources": [],
            "model": "fallback-llm"
        }
    
    async def research_ai_model(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deep research on a specific AI model
        
        Args:
            task: {
                "model_name": "Claude 3.5 Sonnet",
                "aspects": ["capabilities", "pricing", "use_cases"],
                "compare_to": ["GPT-4", "Gemini"]  # optional
            }
        """
        model_name = task.get("model_name", "")
        aspects = task.get("aspects", ["capabilities", "pricing", "use_cases"])
        compare_to = task.get("compare_to", [])
        
        query = f"""
Recherchiere umfassend zum AI Model: {model_name}

FOKUS-BEREICHE:
{chr(10).join(f"- {aspect}" for aspect in aspects)}

BENÖTIGTE INFORMATIONEN:
1. Technische Specs (Parameter, Context-Length, etc.)
2. Capabilities & Limitationen
3. Pricing (Input/Output Tokens)
4. Best Use Cases
5. Aktuelle Performance-Benchmarks
6. API Verfügbarkeit & Features

{"VERGLEICH MIT: " + ", ".join(compare_to) if compare_to else ""}

Erstelle einen detaillierten Research-Report mit:
- Executive Summary
- Detaillierte Findings zu jedem Aspekt
- Praktische Empfehlungen für Einsatz
- Quellen & Veröffentlichungsdatum
"""
        
        result = await self.research_with_perplexity(query)
        
        self.metrics["tasks_completed"] += 1
        
        return {
            "model_researched": model_name,
            "report": result["content"],
            "sources": result["sources"],
            "research_date": self._get_timestamp()
        }
    
    async def analyze_tech_trend(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a tech trend
        
        Args:
            task: {
                "trend": "Local AI / On-Device LLMs",
                "timeframe": "next_6_months" | "next_year" | "next_3_years",
                "focus": ["adoption", "technology", "market"]
            }
        """
        trend = task.get("trend", "")
        timeframe = task.get("timeframe", "next_year")
        focus = task.get("focus", ["adoption", "technology", "market"])
        
        timeframe_map = {
            "next_6_months": "den nächsten 6 Monaten",
            "next_year": "dem nächsten Jahr",
            "next_3_years": "den nächsten 3 Jahren"
        }
        
        query = f"""
Analysiere den Tech-Trend: {trend}

ZEITRAHMEN: {timeframe_map.get(timeframe, timeframe)}

ANALYSE-FOKUS:
{chr(10).join(f"- {f}" for f in focus)}

BENÖTIGTE INSIGHTS:
1. Aktueller Status (wo stehen wir heute?)
2. Key Players & Innovatoren
3. Technologische Entwicklungen
4. Adoption-Rate & Barriers
5. Investment-Activity
6. Predictions & Expert-Meinungen
7. Opportunities für Early Adopters

SPEZIAL-FOKUS:
- Relevanz für Self-Hosting / Homelab
- Accessibility für Non-Tech Users
- Investment-Potenzial

Erstelle einen Trend-Report mit:
- Executive Summary
- Detaillierte Analyse
- Timeline & Milestones
- Actionable Insights
- Quellen
"""
        
        result = await self.research_with_perplexity(query)
        
        self.metrics["tasks_completed"] += 1
        
        return {
            "trend_analyzed": trend,
            "timeframe": timeframe,
            "report": result["content"],
            "sources": result["sources"],
            "analysis_date": self._get_timestamp()
        }
    
    async def research_investment_opportunity(
        self,
        task: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Research investment opportunities in AI/Tech
        
        Args:
            task: {
                "category": "AI_startups" | "tech_stocks" | "crypto_ai",
                "risk_profile": "conservative" | "moderate" | "aggressive",
                "investment_horizon": "short" | "medium" | "long"
            }
        """
        category = task.get("category", "AI_startups")
        risk_profile = task.get("risk_profile", "moderate")
        horizon = task.get("investment_horizon", "medium")
        
        query = f"""
Recherchiere Investment-Opportunities in: {category}

PARAMETER:
- Risikoprofil: {risk_profile}
- Investment-Horizont: {horizon}-term

BENÖTIGTE INFORMATIONEN:
1. Aktuelle Top-Opportunities
2. Market Analysis & Trends
3. Risk-Reward Profile
4. Entry Points & Timing
5. Expert-Meinungen & Predictions
6. Regulatory Considerations
7. Similar erfolgreiche Investments

FOKUS:
- Konkrete, umsetzbare Opportunities
- Für private Investoren zugänglich
- Basierend auf aktuellen Marktdaten

Erstelle einen Investment-Research-Report mit:
- Executive Summary
- Top 3-5 konkrete Opportunities
- Risk-Assessment für jede
- Recommended Actions
- Quellen & Daten-Aktualität

WICHTIG: Dies ist keine Finanzberatung, nur Research!
"""
        
        result = await self.research_with_perplexity(query)
        
        self.metrics["tasks_completed"] += 1
        
        return {
            "category": category,
            "risk_profile": risk_profile,
            "report": result["content"],
            "sources": result["sources"],
            "disclaimer": "This is research only, not financial advice.",
            "research_date": self._get_timestamp()
        }
    
    async def general_research(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        General research query
        
        Args:
            task: {
                "query": "Research question",
                "depth": "quick" | "medium" | "deep"
            }
        """
        query = task.get("query", "")
        depth = task.get("depth", "medium")
        
        depth_instructions = {
            "quick": "Kurze, prägnante Zusammenfassung mit Key Facts.",
            "medium": "Detaillierte Recherche mit Quellen und Insights.",
            "deep": "Umfassende Analyse mit allen Details, Quellen, Implikationen."
        }
        
        enhanced_query = f"""
{query}

TIEFE: {depth_instructions.get(depth, depth_instructions["medium"])}

Strukturiere die Antwort mit:
- Kernaussagen
- Detaillierte Findings
- Quellen
- Praktische Insights
"""
        
        result = await self.research_with_perplexity(enhanced_query)
        
        self.metrics["tasks_completed"] += 1
        
        return {
            "query": query,
            "depth": depth,
            "report": result["content"],
            "sources": result["sources"],
            "research_date": self._get_timestamp()
        }
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()


# Quick test function
async def test_researcher():
    """Test the Researcher Agent"""
    agent = ResearcherAgent()
    
    # Test: Research AI model
    print("=" * 60)
    print("Testing ResearcherAgent")
    print("=" * 60)
    
    result = await agent.research_ai_model({
        "model_name": "Claude 3.5 Sonnet",
        "aspects": ["capabilities", "pricing"],
        "compare_to": ["GPT-4o"]
    })
    
    print(f"\n[RESEARCH] {result['model_researched']}")
    print(f"Date: {result['research_date']}")
    print("\n--- Report Preview (first 500 chars) ---")
    print(result["report"][:500])
    print("...")
    
    if result["sources"]:
        print(f"\nSources: {len(result['sources'])} citations")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_researcher())
