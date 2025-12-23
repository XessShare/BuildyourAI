"""
Verifier Agent - Fact-Checking and Content Verification

Dieser Agent:
- Verifiziert Fakten und Claims aus Content
- Prüft Quellen auf Glaubwürdigkeit
- Checked Aktualität von Informationen
- Cross-referenced Informationen über mehrere Quellen
- Bewertet Content-Genauigkeit
- Identifiziert potenzielle Fehlinformationen
"""

from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent
import requests
import os
from datetime import datetime


class VerifierAgent(BaseAgent):
    """
    Spezialisiert auf Fact-Checking und Content-Verification

    Features:
    1. Fact verification with online sources
    2. Source credibility assessment
    3. Actuality/freshness checking
    4. Cross-referencing claims
    5. Accuracy scoring
    6. Misinformation detection
    """

    def __init__(self):
        super().__init__(agent_type="verifier")
        self.perplexity_api_key = os.getenv("PERPLEXITY_API_KEY", "")
        self.perplexity_url = "https://api.perplexity.ai/chat/completions"

    def get_system_prompt(self) -> str:
        return """Du bist der Verifier Agent im J-Jeco System.

Deine Mission: Sicherstellen, dass Content faktisch korrekt, aktuell und vertrauenswürdig ist.

VERIFICATION-PRINZIPIEN:

1. SKEPTISCHES DENKEN
   - Hinterfrage alle Claims
   - Suche nach Beweisen, nicht Bestätigungen
   - Unterscheide Fakten von Meinungen
   - Identifiziere logische Fehlschlüsse

2. QUELLENPRÜFUNG
   - Bewerte Quellen-Glaubwürdigkeit
   - Prüfe Primär- vs. Sekundärquellen
   - Identifiziere Bias und Interessenkonflikte
   - Verifiziere Autorität und Expertise

3. AKTUALITÄT
   - Prüfe Veröffentlichungsdatum
   - Suche nach Updates und Korrekturen
   - Identifiziere veraltete Informationen
   - Markiere zeitkritische Claims

4. CROSS-REFERENCING
   - Vergleiche mit mehreren Quellen
   - Suche nach Konsens und Widersprüchen
   - Identifiziere Original-Quelle
   - Tracke Information-Kette

5. GENAUIGKEIT
   - Bewerte auf Skala 0-100%
   - Dokumentiere Unsicherheiten
   - Identifiziere unverified Claims
   - Schlage Korrekturen vor

VERIFICATION-OUTPUT:
- Clear Verdict (Verified, Partially Verified, Unverified, False)
- Confidence Score (0-100%)
- Supporting Evidence
- Contradicting Evidence
- Sources Quality Assessment
- Recommendations

SPEZIAL-FOKUS:
- AI & Tech Claims
- Statistical Data
- Product Capabilities
- Market Data
- Scientific Claims
"""

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main execution: Verify content based on task type

        Args:
            task: {
                "type": "verify_facts" | "verify_sources" | "verify_content",
                "content": "Content to verify",
                "claims": ["claim1", "claim2"],  # optional
                "sources": ["url1", "url2"]  # optional
            }

        Returns:
            Verification report with verdict and evidence
        """
        verification_type = task.get("type", "verify_content")

        if verification_type == "verify_facts":
            return await self.verify_facts(task)
        elif verification_type == "verify_sources":
            return await self.verify_sources(task)
        elif verification_type == "check_actuality":
            return await self.check_actuality(task)
        elif verification_type == "cross_reference":
            return await self.cross_reference_claims(task)
        else:
            return await self.verify_content(task)

    async def verify_with_perplexity(
        self,
        query: str,
        system_context: str = ""
    ) -> Dict[str, Any]:
        """
        Use Perplexity API for real-time fact verification

        Args:
            query: Verification query
            system_context: Additional context

        Returns:
            Verification results with sources
        """
        if not self.perplexity_api_key:
            # Fallback to regular LLM
            return await self._fallback_verification(query, system_context)

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
            "temperature": 0.1,  # Low temperature for factual accuracy
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
            return await self._fallback_verification(query, system_context)

    async def _fallback_verification(
        self,
        query: str,
        context: str = ""
    ) -> Dict[str, Any]:
        """Fallback to regular LLM when Perplexity unavailable"""
        prompt = f"{context}\n\n{query}" if context else query
        response = await self.think(prompt)

        return {
            "content": response,
            "sources": [],
            "model": "fallback-llm"
        }

    async def verify_facts(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verify specific factual claims

        Args:
            task: {
                "claims": ["claim1", "claim2"],
                "context": "Optional context"
            }

        Returns:
            Verification report for each claim
        """
        claims = task.get("claims", [])
        context = task.get("context", "")

        if not claims:
            return {
                "error": "No claims provided for verification",
                "status": "failed"
            }

        # Verify all claims
        verifications = []

        for claim in claims:
            query = f"""
Verifiziere den folgenden Fact-Claim:

CLAIM: "{claim}"

{f"KONTEXT: {context}" if context else ""}

VERIFICATION-AUFGABE:
1. Ist dieser Claim faktisch korrekt?
2. Welche Beweise gibt es?
3. Gibt es widersprüchliche Informationen?
4. Wie aktuell ist diese Information?
5. Welche verlässlichen Quellen bestätigen/widerlegen dies?

BEWERTE:
- Verdict: VERIFIED / PARTIALLY_VERIFIED / UNVERIFIED / FALSE
- Confidence: 0-100%
- Evidence: Supporting and contradicting evidence
- Sources: Liste der Quellen
- Aktualität: Wann wurde dies zuletzt verifiziert?
- Anmerkungen: Wichtige Nuancen oder Einschränkungen

Strukturiere die Antwort klar und präzise.
"""

            result = await self.verify_with_perplexity(query)

            verifications.append({
                "claim": claim,
                "verification": result["content"],
                "sources": result["sources"],
                "verified_at": self._get_timestamp()
            })

        self.metrics["tasks_completed"] += 1

        return {
            "type": "fact_verification",
            "claims_checked": len(claims),
            "verifications": verifications,
            "report_date": self._get_timestamp()
        }

    async def verify_sources(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verify credibility and quality of sources

        Args:
            task: {
                "sources": ["url1", "source_name", ...],
                "topic": "What topic are these sources about?"
            }

        Returns:
            Source credibility assessment
        """
        sources = task.get("sources", [])
        topic = task.get("topic", "general")

        if not sources:
            return {
                "error": "No sources provided for verification",
                "status": "failed"
            }

        query = f"""
Bewerte die Glaubwürdigkeit und Qualität folgender Quellen zum Thema: {topic}

QUELLEN:
{chr(10).join(f"{i+1}. {source}" for i, source in enumerate(sources))}

FÜR JEDE QUELLE PRÜFE:
1. Reputation & Autorität
   - Wer steht hinter der Quelle?
   - Track Record?
   - Expertise im Themenfeld?

2. Bias & Objektivität
   - Potenzielle Interessenkonflikte?
   - Political/Commercial Bias?
   - Transparent über Limitierungen?

3. Aktualität & Wartung
   - Wie aktuell ist die Quelle?
   - Wird sie regelmäßig aktualisiert?
   - Datum der Informationen?

4. Methodologie
   - Primär- oder Sekundärquelle?
   - Quellenangaben vorhanden?
   - Peer-reviewed oder redaktionell geprüft?

5. Credibility Score
   - Overall Score: 0-100%
   - Recommendation: HIGHLY_CREDIBLE / CREDIBLE / QUESTIONABLE / NOT_CREDIBLE

AUSGABE:
Für jede Quelle: Name, Score, Bewertung, Begründung, Empfehlung
"""

        result = await self.verify_with_perplexity(query)

        self.metrics["tasks_completed"] += 1

        return {
            "type": "source_verification",
            "topic": topic,
            "sources_checked": len(sources),
            "assessment": result["content"],
            "reference_sources": result["sources"],
            "verified_at": self._get_timestamp()
        }

    async def check_actuality(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check if information is current and up-to-date

        Args:
            task: {
                "content": "Content to check for actuality",
                "topic": "AI models" / "tech trends" / etc.
            }

        Returns:
            Actuality assessment
        """
        content = task.get("content", "")
        topic = task.get("topic", "general")

        query = f"""
Prüfe die Aktualität folgenden Contents zum Thema: {topic}

CONTENT:
{content}

AKTUALITÄTS-PRÜFUNG:
1. Zeitkritische Informationen identifizieren
   - Welche Aussagen sind zeitabhängig?
   - Gibt es Daten, Versionen, Preise?

2. Aktuelle Fakten-Lage
   - Was ist der aktuelle Stand (heute)?
   - Welche Informationen sind veraltet?
   - Was hat sich geändert?

3. Updates & Änderungen
   - Gab es wichtige Updates?
   - Breaking Changes?
   - Neue Entwicklungen?

4. Empfohlene Updates
   - Was muss aktualisiert werden?
   - Welche Infos sind noch gültig?
   - Neue Informationen hinzufügen?

BEWERTUNG:
- Actuality Score: 0-100%
- Outdated Elements: Liste
- Current Status: Aktueller Stand
- Recommended Updates: Was updaten?

Strukturiere die Antwort mit konkreten Empfehlungen.
"""

        result = await self.verify_with_perplexity(query)

        self.metrics["tasks_completed"] += 1

        return {
            "type": "actuality_check",
            "topic": topic,
            "assessment": result["content"],
            "sources": result["sources"],
            "checked_at": self._get_timestamp()
        }

    async def cross_reference_claims(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cross-reference claims across multiple sources

        Args:
            task: {
                "claim": "The specific claim to verify",
                "minimum_sources": 3
            }

        Returns:
            Cross-reference analysis
        """
        claim = task.get("claim", "")
        min_sources = task.get("minimum_sources", 3)

        query = f"""
Cross-reference folgenden Claim über mehrere Quellen:

CLAIM: "{claim}"

CROSS-REFERENCE-ANALYSE:
1. Finde mindestens {min_sources} unabhängige Quellen
2. Vergleiche die Darstellung in verschiedenen Quellen
3. Identifiziere Konsens und Widersprüche
4. Bewerte Qualität jeder Quelle
5. Tracke zurück zur Original-Quelle wenn möglich

ANALYSE:
- Konsens: Was bestätigen alle Quellen?
- Widersprüche: Wo gibt es Unterschiede?
- Confidence Level: Wie sicher können wir sein?
- Original Source: Wo kommt die Info her?
- Verdict: CONSENSUS / MIXED / CONFLICTING / UNVERIFIABLE

AUSGABE:
- Zusammenfassung des Claim-Status
- Quellen-Breakdown mit Bewertung
- Empfehlung: Vertrauen oder weitere Prüfung?
"""

        result = await self.verify_with_perplexity(query)

        self.metrics["tasks_completed"] += 1

        return {
            "type": "cross_reference",
            "claim": claim,
            "minimum_sources": min_sources,
            "analysis": result["content"],
            "sources_found": result["sources"],
            "analyzed_at": self._get_timestamp()
        }

    async def verify_content(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Comprehensive content verification

        Args:
            task: {
                "content": "Full content to verify",
                "content_type": "article" / "video_script" / "newsletter",
                "focus_areas": ["accuracy", "sources", "actuality"]
            }

        Returns:
            Complete verification report with accuracy score
        """
        content = task.get("content", "")
        content_type = task.get("content_type", "article")
        focus_areas = task.get("focus_areas", ["accuracy", "sources", "actuality"])

        query = f"""
COMPREHENSIVE CONTENT VERIFICATION

CONTENT-TYPE: {content_type}
FOKUS-BEREICHE: {", ".join(focus_areas)}

CONTENT ZU VERIFIZIEREN:
{content}

VERIFICATION-PROZESS:

1. FACTUAL ACCURACY
   - Identifiziere alle faktischen Claims
   - Verifiziere jeden Claim
   - Bewerte Genauigkeit (0-100%)
   - Liste falsche/ungenaue Aussagen

2. SOURCES & CITATIONS
   - Sind Quellen angegeben?
   - Qualität der Quellen?
   - Fehlende Citations?
   - Empfohlene zusätzliche Quellen

3. ACTUALITY & CURRENCY
   - Sind Informationen aktuell?
   - Veraltete Daten?
   - Neueste Entwicklungen berücksichtigt?

4. COMPLETENESS
   - Wichtige Informationen fehlen?
   - Misleading durch Auslassungen?
   - Context ausreichend?

5. CLARITY & ACCURACY
   - Missverständliche Formulierungen?
   - Übertreibungen oder Untertreibungen?
   - Technische Genauigkeit?

OVERALL ASSESSMENT:
- Accuracy Score: 0-100%
- Trustworthiness: HIGH / MEDIUM / LOW
- Issues Found: Liste mit Priorität
- Recommended Corrections: Konkrete Verbesserungen
- Verdict: APPROVED / NEEDS_REVISION / REJECT

Strukturiere das Feedback actionable und konstruktiv.
"""

        result = await self.verify_with_perplexity(query)

        self.metrics["tasks_completed"] += 1

        return {
            "type": "content_verification",
            "content_type": content_type,
            "focus_areas": focus_areas,
            "report": result["content"],
            "sources": result["sources"],
            "verified_at": self._get_timestamp(),
            "word_count": len(content.split())
        }

    async def rate_accuracy(
        self,
        content: str,
        reference_sources: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Rate the accuracy of content with a numerical score

        Args:
            content: Content to rate
            reference_sources: Optional known good sources

        Returns:
            Accuracy rating and breakdown
        """
        sources_context = ""
        if reference_sources:
            sources_context = f"\nREFERENZ-QUELLEN:\n{chr(10).join(reference_sources)}"

        query = f"""
Bewerte die Genauigkeit folgenden Contents:

CONTENT:
{content}
{sources_context}

ACCURACY RATING (0-100%):
1. Faktische Korrektheit (40%)
2. Quellenqualität (20%)
3. Aktualität (20%)
4. Vollständigkeit (10%)
5. Klarheit/Präzision (10%)

Für jede Kategorie:
- Score
- Begründung
- Verbesserungsvorschläge

OVERALL:
- Total Accuracy Score: X%
- Confidence in Rating: X%
- Key Issues: Liste
- Priority Fixes: Top 3

Sei präzise und objektiv in der Bewertung.
"""

        result = await self.verify_with_perplexity(query)

        return {
            "content_preview": content[:200] + "...",
            "rating_report": result["content"],
            "sources_used": result["sources"],
            "rated_at": self._get_timestamp()
        }

    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        return datetime.now().isoformat()


# Quick test function
async def test_verifier():
    """Test the Verifier Agent"""
    agent = VerifierAgent()

    print("=" * 60)
    print("Testing VerifierAgent")
    print("=" * 60)

    # Test: Verify a factual claim
    result = await agent.verify_facts({
        "claims": [
            "GPT-4 has a context window of 128k tokens",
            "Claude 3.5 Sonnet is faster than GPT-4"
        ],
        "context": "AI model capabilities in 2024"
    })

    print(f"\n[FACT VERIFICATION]")
    print(f"Claims checked: {result['claims_checked']}")
    print(f"\nFirst verification preview:")
    print(result["verifications"][0]["verification"][:400])
    print("...")

    if result["verifications"][0]["sources"]:
        print(f"\nSources: {len(result['verifications'][0]['sources'])} citations")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_verifier())
