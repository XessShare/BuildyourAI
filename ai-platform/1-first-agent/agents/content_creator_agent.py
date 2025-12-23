"""
Content Creator Agent - Video Scripts, Newsletter & Blog Content

Dieser Agent:
- Erstellt Tutorial-Skripte für AI-Avatar-Videos
- Generiert Newsletter-Content
- Schreibt Blog-Posts
- Optimiert für Non-Tech-Audience
"""

from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent


class ContentCreatorAgent(BaseAgent):
    """
    Spezialisiert auf kreative Content-Erstellung

    Features:
    1. Video Script Generation
    2. Newsletter Writing
    3. Blog Post Creation
    4. Content Optimization for different platforms
    """

    def __init__(self):
        super().__init__(agent_type="content_creator")
        self.content_templates = self._load_templates()

    def _load_templates(self) -> Dict[str, str]:
        """Load content templates for different formats"""
        return {
            "video_script": """
            # Video Title: {title}
            Duration: {duration} minutes

            ## Intro (30s)
            - Hook
            - Problem Statement
            - What viewer will learn

            ## Main Content ({main_duration} min)
            - Section 1
            - Section 2
            - Section 3

            ## Outro (30s)
            - Summary
            - Call to Action
            - Next Steps
            """,

            "newsletter": """
            Subject: {subject}

            ## Opening
            - Personal greeting
            - Week's theme

            ## Main Sections
            {sections}

            ## Closing
            - Key Takeaway
            - Call to Action
            - Sign-off
            """
        }

    def get_system_prompt(self) -> str:
        return """Du bist der Content Creator Agent im J-Jeco System.

Deine Mission: Erstelle hochwertigen, engagierenden Content für ein Non-Tech-Publikum.

CONTENT-PRINZIPIEN:

1. KLARHEIT ÜBER ALLES
   - Kinderleicht erklärt (12-Jährige müssen es verstehen)
   - Keine Fachbegriffe ohne Erklärung
   - Konkrete Beispiele statt Abstraktionen
   - Schritt-für-Schritt, niemals Sprünge

2. STORYTELLING
   - Beginne mit einem Hook (Problem oder Frage)
   - Baue Spannung auf
   - Nutze Metaphern und Analogien
   - Persönlich und authentisch

3. STRUKTUR
   - Klare Gliederung
   - Logischer Fluss
   - Zusammenfassungen nach Abschnitten
   - Actionable Takeaways

4. ENGAGEMENT
   - Direkte Ansprache ("Du"/"Sie")
   - Rhetorische Fragen
   - Humor wo passend
   - Visuelle Sprache (male Bilder mit Worten)

5. VALUE DELIVERY
   - Jeder Abschnitt muss Mehrwert liefern
   - Konkrete, umsetzbare Tipps
   - Keine Filler-Content
   - Quick Wins einbauen

SPEZIAL-FOKUS: AI & Homelab für Nicht-Techniker
- Vermeide: Docker, Container, CLI, API (ohne Erklärung)
- Nutze: "wie Apps auf dem Handy", "wie ein Mietauto", etc.
- Zeige den NUTZEN, nicht die Technik

OUTPUT: Immer publikationsreif, copy-paste-ready, mit klarer Struktur.
"""

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main execution: Create content based on task type

        Args:
            task: {
                "type": "video_script" | "newsletter" | "blog_post",
                "topic": "Main topic",
                "target_duration": 10 (for videos),
                "key_points": ["Point 1", "Point 2"],
                "audience": "beginner" | "intermediate" | "advanced"
            }

        Returns:
            {
                "content": "Generated content",
                "metadata": {...}
            }
        """
        content_type = task.get("type", "video_script")

        if content_type == "video_script":
            return await self.create_video_script(task)
        elif content_type == "newsletter":
            return await self.create_newsletter(task)
        elif content_type == "blog_post":
            return await self.create_blog_post(task)
        else:
            raise ValueError(f"Unknown content type: {content_type}")

    async def create_video_script(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a video script for AI-Avatar presentation

        Args:
            task: {
                "topic": "Video topic",
                "target_duration": 10,  # minutes
                "key_points": ["Point 1", "Point 2"],
                "style": "educational" | "entertaining" | "motivational"
            }

        Returns:
            Complete video script with timing
        """
        topic = task.get("topic", "")
        duration = task.get("target_duration", 10)
        key_points = task.get("key_points", [])
        style = task.get("style", "educational")

        script_prompt = f"""
Erstelle ein {duration}-minütiges Video-Skript für ein Tutorial-Video.

THEMA: {topic}

KEY POINTS ZU COVERN:
{chr(10).join(f"- {point}" for point in key_points)}

STIL: {style}
ZIELGRUPPE: Nicht-technische Anfänger
FORMAT: AI-Avatar-Präsentation (kein Live-Demo)

REQUIREMENTS:
1. Intro (30 Sekunden)
   - Starker Hook (Frage oder überraschende Aussage)
   - Problem-Statement (warum ist das relevant?)
   - Preview (was lernt der Zuschauer?)

2. Main Content ({duration - 1} Minuten)
   - 3-4 Hauptsektionen
   - Jede Sektion max. 2-3 Minuten
   - Klare Überleitungen zwischen Sektionen
   - Konkrete Beispiele und Analogien
   - "Pause-Punkte" für Verständnis

3. Outro (30 Sekunden)
   - Zusammenfassung in 1-2 Sätzen
   - Call-to-Action (Subscribe, Kommentar)
   - Teaser für nächstes Video

FORMAT:
- Timing-Angaben pro Sektion
- Sprechtext (wie Avatar es sagen soll)
- [VISUAL NOTES] für Grafiken/Overlays
- [PAUSE] wo Zuschauer Zeit zum Denken braucht

TONE: Freundlich, enthusiastisch, ermutigend
SPRACHE: Deutsch, Du-Form, einfach

Erstelle das komplette Skript:
"""

        script = await self.think(script_prompt)

        self.metrics["tasks_completed"] += 1

        return {
            "content": script,
            "metadata": {
                "topic": topic,
                "duration": duration,
                "type": "video_script",
                "word_count": len(script.split()),
                "estimated_speaking_time": len(script.split()) / 150  # ~150 words/minute
            }
        }

    async def create_newsletter(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create newsletter content

        Args:
            task: {
                "theme": "Week's main theme",
                "sections": {
                    "ai_updates": "Recent AI news",
                    "homelab_tip": "Weekly tip",
                    "investment_idea": "Trend to watch"
                },
                "target_length": 800  # words
            }

        Returns:
            Newsletter with subject line and structured content
        """
        theme = task.get("theme", "Diese Woche in AI & Homelab")
        sections = task.get("sections", {})
        target_length = task.get("target_length", 800)

        newsletter_prompt = f"""
Erstelle einen wöchentlichen Newsletter für AI & Homelab Enthusiasten.

WOCHENTHEMA: {theme}

SEKTIONEN ZU SCHREIBEN:
{chr(10).join(f"- {section}: {content}" for section, content in sections.items())}

ZIELGRUPPE:
- Interessiert an AI und Self-Hosting
- Nicht unbedingt technisch
- Wollen praktische Tipps, keine Theorie
- 5-10 Minuten Lesezeit

STRUKTUR:

1. SUBJECT LINE
   - Catchy, Neugier weckend
   - Max. 50 Zeichen
   - Emoji optional aber passend

2. OPENING (100 Wörter)
   - Persönlicher Gruß
   - Hook: Warum ist diese Woche spannend?
   - Überblick was kommt

3. MAIN SECTIONS (~{target_length - 250} Wörter)

   A) 🤖 Diese Woche in AI
      - 1-2 wichtige Updates
      - Was bedeutet das für dich?
      - Quick Takeaway

   B) 🏠 Homelab-Hack der Woche
      - Ein konkreter, umsetzbarer Tipp
      - Schritt-für-Schritt oder Tool-Empfehlung
      - Warum es sich lohnt

   C) 💰 Investment-Idee / Tech-Trend
      - Emerging Trend oder Opportunity
      - Warum jetzt relevant?
      - Wie man mehr lernt/einsteigt

4. CLOSING (150 Wörter)
   - Key Takeaway der Woche
   - Call-to-Action (Reply, Share, Join Community)
   - Teaser für nächste Woche
   - Persönlicher Sign-off

TONE: Freundlich, informativ, motivierend
STIL: Conversational, wie an einen Freund
LÄNGE: ~{target_length} Wörter

Schreibe den kompletten Newsletter:
"""

        newsletter = await self.think(newsletter_prompt)

        self.metrics["tasks_completed"] += 1

        return {
            "content": newsletter,
            "metadata": {
                "theme": theme,
                "type": "newsletter",
                "word_count": len(newsletter.split()),
                "estimated_read_time": len(newsletter.split()) / 200  # ~200 words/minute
            }
        }

    async def create_blog_post(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a blog post

        Args:
            task: {
                "title": "Post title",
                "outline": ["Section 1", "Section 2"],
                "seo_keywords": ["keyword1", "keyword2"],
                "target_length": 1500
            }

        Returns:
            SEO-optimized blog post
        """
        title = task.get("title", "")
        outline = task.get("outline", [])
        keywords = task.get("seo_keywords", [])
        target_length = task.get("target_length", 1500)

        blog_prompt = f"""
Schreibe einen ausführlichen Blog-Post:

TITEL: {title}

OUTLINE:
{chr(10).join(f"{i+1}. {section}" for i, section in enumerate(outline))}

SEO KEYWORDS: {", ".join(keywords)}

LÄNGE: ~{target_length} Wörter

STRUKTUR:
1. Einleitung mit Hook
2. Hauptteil nach Outline
3. Fazit mit Takeaways
4. Call-to-Action

FORMAT:
- Markdown formatting
- H2/H3 Headings
- Bullet Points wo passend
- Hervorhebungen **bold**
- Code-Beispiele wenn relevant

STIL: Informativ, zugänglich, praktisch orientiert

Schreibe den Post:
"""

        blog_post = await self.think(blog_prompt)

        self.metrics["tasks_completed"] += 1

        return {
            "content": blog_post,
            "metadata": {
                "title": title,
                "type": "blog_post",
                "word_count": len(blog_post.split()),
                "seo_keywords": keywords
            }
        }

    async def optimize_for_platform(
        self,
        content: str,
        platform: str
    ) -> str:
        """
        Optimize content for specific platform

        Args:
            content: Original content
            platform: "youtube", "linkedin", "twitter", "instagram"

        Returns:
            Platform-optimized version
        """
        platform_specs = {
            "youtube": "YouTube Description mit Timestamps, max 5000 Zeichen",
            "linkedin": "Professional, max 3000 Zeichen, Hashtags",
            "twitter": "Thread-Format, max 280 Zeichen pro Tweet",
            "instagram": "Caption mit Emojis, max 2200 Zeichen, Hashtags"
        }

        spec = platform_specs.get(platform, "General format")

        optimization_prompt = f"""
Optimiere folgenden Content für {platform.upper()}:

ORIGINAL CONTENT:
{content}

PLATFORM REQUIREMENTS: {spec}

Erstelle die optimierte Version:
"""

        return await self.think(optimization_prompt)

    async def generate_content_ideas(
        self,
        theme: str,
        count: int = 10
    ) -> List[str]:
        """
        Generate content ideas based on theme

        Args:
            theme: Content theme/topic
            count: Number of ideas to generate

        Returns:
            List of content ideas
        """
        ideas_prompt = f"""
Generiere {count} konkrete Content-Ideen zum Thema: {theme}

Für jeden Idee:
- Konkreter, catchy Titel
- 1-2 Sätze Beschreibung
- Zielgruppe
- Format-Vorschlag (Video/Newsletter/Blog)

KRITERIEN:
- Actionable (klarer Mehrwert)
- Unique Angle (nicht Standard)
- SEO-freundlich
- Engagement-Potenzial

Liste die Ideen auf:
"""

        ideas_text = await self.think(ideas_prompt)
        return ideas_text.split("\n\n")  # Split by double newline

    async def create_content_series(
        self,
        series_theme: str,
        episodes: int = 4
    ) -> Dict[str, Any]:
        """
        Create outline for a content series

        Args:
            series_theme: Overall theme
            episodes: Number of episodes

        Returns:
            Series outline with episode breakdowns
        """
        series_prompt = f"""
Erstelle eine {episodes}-teilige Content-Serie zum Thema: {series_theme}

Für jede Episode:
1. Titel
2. Hauptthema
3. Key Learnings (3-5)
4. Prerequisites (was muss Zuschauer vorher wissen?)
5. Next Episode Teaser

SERIE SOLLTE:
- Logisch aufbauen (Grundlagen → Advanced)
- Standalone watchable sein
- Gemeinsamen roten Faden haben
- Zum Moonshot-Ziel beitragen (100K Reach)

Format als strukturierte Serie:
"""

        series_outline = await self.think(series_prompt)

        return {
            "series_theme": series_theme,
            "episode_count": episodes,
            "outline": series_outline
        }


# Quick test function
async def test_content_creator():
    """Test the Content Creator Agent"""
    agent = ContentCreatorAgent()

    # Test: Create a video script
    result = await agent.create_video_script({
        "topic": "Homelab für Anfänger: Dein erster Proxmox Server",
        "target_duration": 10,
        "key_points": [
            "Was ist ein Homelab?",
            "Warum Proxmox?",
            "Hardware Requirements",
            "Installation Step-by-Step",
            "Erste VM erstellen"
        ],
        "style": "educational"
    })

    print("=== VIDEO SCRIPT ===")
    print(result["content"][:500])  # First 500 chars
    print(f"\n... ({result['metadata']['word_count']} words total)")
    print(f"Estimated speaking time: {result['metadata']['estimated_speaking_time']:.1f} minutes")

    # Test: Generate content ideas
    ideas = await agent.generate_content_ideas("AI Self-Hosting", count=5)
    print("\n=== CONTENT IDEAS ===")
    for i, idea in enumerate(ideas[:3], 1):
        print(f"{i}. {idea[:100]}...")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_content_creator())
