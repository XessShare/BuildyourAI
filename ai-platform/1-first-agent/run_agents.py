"""
J-Jeco AI Platform - Main Runner
Orchestrates multiple agents for complex workflows
"""

import asyncio
import sys
from pathlib import Path
from typing import Dict, Any, List
import json

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from agents.project_manager_agent import ProjectManagerAgent
from agents.content_creator_agent import ContentCreatorAgent
from agents.researcher_agent import ResearcherAgent
from agents.communicator_agent import CommunicatorAgent


class AgentOrchestrator:
    """
    Coordinates multiple agents to complete complex tasks
    """
    
    def __init__(self):
        print("Initializing J-Jeco AI Platform...")
        self.project_manager = ProjectManagerAgent()
        self.content_creator = ContentCreatorAgent()
        self.researcher = ResearcherAgent()
        self.communicator = CommunicatorAgent()
        print("All agents initialized!\n")
    
    async def create_tutorial_video(
        self,
        topic: str,
        duration: int = 10,
        research_first: bool = True
    ) -> Dict[str, Any]:
        """
        Complete workflow: Research → Script → Optimize
        
        Args:
            topic: Video topic
            duration: Target duration in minutes
            research_first: Whether to research the topic first
            
        Returns:
            Complete package with research, script, and optimized content
        """
        print("=" * 70)
        print(f"CREATING TUTORIAL VIDEO: {topic}")
        print("=" * 70)
        
        result = {
            "topic": topic,
            "duration": duration,
            "research": None,
            "script": None,
            "optimized_script": None
        }
        
        # Step 1: Research (if requested)
        if research_first:
            print("\n[1/3] Researching topic...")
            print("-" * 70)
            research_result = await self.researcher.general_research({
                "query": f"Research about {topic} - latest information, key concepts, and important details",
                "depth": "medium"
            })
            result["research"] = research_result["report"]
            print(f"Research completed! ({len(research_result['report'])} chars)")
        
        # Step 2: Create video script
        print("\n[2/3] Creating video script...")
        print("-" * 70)
        
        # Extract key points from research if available
        key_points = []
        if result["research"]:
            # Simple extraction - in production, could use LLM to extract
            key_points = [
                "Introduction to the topic",
                "Key concepts and features",
                "Practical applications",
                "Getting started guide"
            ]
        
        script_result = await self.content_creator.create_video_script({
            "topic": topic,
            "target_duration": duration,
            "key_points": key_points,
            "style": "educational"
        })
        result["script"] = script_result["content"]
        print(f"Script created! ({script_result['metadata']['word_count']} words)")
        
        # Step 3: Optimize for platform
        print("\n[3/3] Optimizing for YouTube...")
        print("-" * 70)
        optimized = await self.content_creator.optimize_for_platform(
            result["script"],
            "youtube"
        )
        result["optimized_script"] = optimized
        print("Optimization complete!")
        
        print("\n" + "=" * 70)
        print("VIDEO CREATION COMPLETED!")
        print("=" * 70)
        
        return result
    
    async def create_newsletter(
        self,
        theme: str,
        research_topics: List[str] = None
    ) -> Dict[str, Any]:
        """
        Complete newsletter workflow: Research → Write → Optimize
        
        Args:
            theme: Newsletter theme
            research_topics: Topics to research before writing
            
        Returns:
            Complete newsletter with research
        """
        print("=" * 70)
        print(f"CREATING NEWSLETTER: {theme}")
        print("=" * 70)
        
        result = {
            "theme": theme,
            "research_results": {},
            "newsletter": None
        }
        
        # Step 1: Research topics
        if research_topics:
            print(f"\n[1/2] Researching {len(research_topics)} topics...")
            print("-" * 70)
            
            for topic in research_topics:
                print(f"  - Researching: {topic}")
                research = await self.researcher.general_research({
                    "query": topic,
                    "depth": "quick"
                })
                result["research_results"][topic] = research["report"][:300]  # Summary
            
            print("Research completed!")
        
        # Step 2: Create newsletter
        print(f"\n[2/2] Writing newsletter...")
        print("-" * 70)
        
        # Build sections from research
        sections = {}
        for i, (topic, summary) in enumerate(result["research_results"].items()):
            sections[f"section_{i+1}"] = summary
        
        newsletter_result = await self.content_creator.create_newsletter({
            "theme": theme,
            "sections": sections or {"main": "General AI & Homelab updates"},
            "target_length": 800
        })
        result["newsletter"] = newsletter_result["content"]
        print(f"Newsletter created! ({newsletter_result['metadata']['word_count']} words)")
        
        print("\n" + "=" * 70)
        print("NEWSLETTER COMPLETED!")
        print("=" * 70)
        
        return result
    
    async def research_and_analyze(
        self,
        topic: str,
        analysis_type: str = "trend_analysis"
    ) -> Dict[str, Any]:
        """
        Deep research and analysis workflow
        
        Args:
            topic: Research topic
            analysis_type: "trend_analysis" | "model_research" | "investment_research"
            
        Returns:
            Detailed research report
        """
        print("=" * 70)
        print(f"DEEP RESEARCH: {topic}")
        print("=" * 70)
        
        if analysis_type == "trend_analysis":
            result = await self.researcher.analyze_tech_trend({
                "trend": topic,
                "timeframe": "next_year",
                "focus": ["adoption", "technology", "market"]
            })
        elif analysis_type == "model_research":
            result = await self.researcher.research_ai_model({
                "model_name": topic,
                "aspects": ["capabilities", "pricing", "use_cases"]
            })
        elif analysis_type == "investment_research":
            result = await self.researcher.research_investment_opportunity({
                "category": topic,
                "risk_profile": "moderate",
                "investment_horizon": "medium"
            })
        else:
            result = await self.researcher.general_research({
                "query": topic,
                "depth": "deep"
            })
        
        print("\nResearch completed!")
        print("=" * 70)
        
        return result
    
    def save_result(self, result: Dict[str, Any], filename: str):
        """Save result to output directory"""
        output_dir = Path(__file__).parent / "output"
        output_dir.mkdir(exist_ok=True)
        
        filepath = output_dir / filename
        with open(filepath, "w", encoding="utf-8") as f:
            if filename.endswith(".json"):
                json.dump(result, f, indent=2, ensure_ascii=False)
            else:
                # Save as text
                if isinstance(result, dict):
                    for key, value in result.items():
                        f.write(f"=== {key.upper()} ===\n\n")
                        f.write(str(value) + "\n\n")
                else:
                    f.write(str(result))
        
        print(f"\nResult saved to: {filepath}")


async def main():
    """Main entry point with example workflows"""
    orchestrator = AgentOrchestrator()
    
    print("\nJ-Jeco AI Platform - Available Workflows:\n")
    print("1. Create Tutorial Video (with research)")
    print("2. Create Newsletter")
    print("3. Research & Analyze")
    print("4. Run all examples")
    print()
    
    choice = input("Select workflow (1-4): ").strip()
    
    if choice == "1":
        # Example: Create tutorial video
        result = await orchestrator.create_tutorial_video(
            topic="Proxmox für Anfänger: Dein erstes Homelab",
            duration=10,
            research_first=True
        )
        orchestrator.save_result(result, "tutorial_video_output.txt")
        
    elif choice == "2":
        # Example: Create newsletter
        result = await orchestrator.create_newsletter(
            theme="Diese Woche in AI & Homelab",
            research_topics=[
                "Latest AI model releases in December 2024",
                "Best self-hosted apps for beginners"
            ]
        )
        orchestrator.save_result(result, "newsletter_output.txt")
        
    elif choice == "3":
        # Example: Research and analyze
        result = await orchestrator.research_and_analyze(
            topic="Local LLMs and AI Self-Hosting",
            analysis_type="trend_analysis"
        )
        orchestrator.save_result(result, "research_report.txt")
        
    elif choice == "4":
        # Run all examples
        print("\n[Running all example workflows...]")
        
        # 1. Video
        print("\n\n")
        video_result = await orchestrator.create_tutorial_video(
            topic="AI Avatars: Die Zukunft der Content Creation",
            duration=5,
            research_first=False  # Skip research for speed
        )
        orchestrator.save_result(video_result, "example_video.txt")
        
        # 2. Newsletter (quick version)
        print("\n\n")
        newsletter_result = await orchestrator.create_newsletter(
            theme="AI Quick-Updates der Woche",
            research_topics=[]  # Skip research for speed
        )
        orchestrator.save_result(newsletter_result, "example_newsletter.txt")
        
        print("\n\nAll examples completed! Check the output/ directory.")
    
    else:
        print("Invalid choice. Exiting.")


if __name__ == "__main__":
    asyncio.run(main())
