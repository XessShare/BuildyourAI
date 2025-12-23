# J-Jeco AI Platform - First Agent System

Multi-agent AI system for content creation, research, and automation.

## Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Configure API keys:**
Copy `.env.template` to `.env` and fill in your API keys:
```bash
cp .env.template .env
# Edit .env with your keys
```

Required keys:
- `OPENAI_API_KEY` - For GPT models
- `ANTHROPIC_API_KEY` - For Claude models  
- `GOOGLE_API_KEY` - For Gemini models
- `PERPLEXITY_API_KEY` - For online research (optional)

## Available Agents

### 1. **ContentCreatorAgent**
Creates video scripts, newsletters, and blog posts.

**Features:**
- Video script generation (with timing)
- Newsletter writing
- Blog post creation
- Platform optimization (YouTube, LinkedIn, etc.)
- Content idea generation

### 2. **ResearcherAgent**
Deep research with online capabilities.

**Features:**
- Real-time research via Perplexity API
- AI model comparison
- Tech trend analysis
- Investment opportunity research
- Fact verification

### 3. **VerifierAgent**
Fact-checking and content quality assurance.

**Features:**
- Fact verification with online sources
- Source credibility assessment
- Actuality/freshness checking
- Cross-referencing claims
- Content accuracy scoring
- Misinformation detection

### 4. **AnalystAgent**
Data analysis and insights extraction.

**Features:**
- Dataset analysis (CSV, JSON, DataFrames)
- Pattern and trend detection
- Statistical analysis
- Performance metrics evaluation
- Comparative analysis across periods
- KPI tracking and reporting

### 5. **ProjectManagerAgent**
Coordinates tasks and manages workflows.

**Features:**
- Task breakdown and planning
- Priority management
- Progress tracking
- Team coordination

### 6. **CommunicatorAgent**
Optimizes prompts and communication.

**Features:**
- Prompt engineering
- Message optimization
- Tone adjustment
- Multi-language support

## Usage

### Quick Start - Run Orchestrator

```bash
python run_agents.py
```

Select from available workflows:
1. Create Tutorial Video (with research)
2. Create Newsletter
3. Research & Analyze
4. Run all examples

### Individual Agent Tests

Test specific agents:

```bash
# Test Content Creator
python test_content_creator.py

# Test Researcher
python test_researcher.py

# Test Verifier
python test_verifier.py

# Test Analyst
python test_analyst.py
```

### Programmatic Usage

```python
from agents import ContentCreatorAgent, ResearcherAgent

# Create video script
content_agent = ContentCreatorAgent()
result = await content_agent.create_video_script({
    "topic": "AI Homelab Setup",
    "target_duration": 10,
    "key_points": ["Hardware", "Software", "Setup"],
    "style": "educational"
})
print(result["content"])

# Research a trend
research_agent = ResearcherAgent()
analysis = await research_agent.analyze_tech_trend({
    "trend": "Local AI Models",
    "timeframe": "next_year",
    "focus": ["adoption", "technology"]
})
print(analysis["report"])
```

## Architecture

```
1-first-agent/
├── agents/              # Agent implementations
│   ├── base_agent.py           # Base agent class
│   ├── content_creator_agent.py
│   ├── researcher_agent.py
│   ├── project_manager_agent.py
│   └── communicator_agent.py
├── config.py            # Configuration & API keys
├── run_agents.py        # Main orchestrator
├── test_*.py            # Test scripts
├── output/              # Generated content
├── logs/                # Agent logs
└── data/                # Data & knowledge base
```

## Configuration

Edit `config.py` to customize:

- **Models**: Choose which LLM for each agent
- **Agent Settings**: Temperature, roles, specialties
- **Paths**: Output, logs, data directories
- **KPI Targets**: Track progress towards goals

Example:
```python
AGENT_CONFIG = {
    "content_creator": {
        "model": "gpt-4o-mini",
        "temperature": 0.8,
        "role": "Creative content generator"
    },
    ...
}
```

## Workflows

### Tutorial Video Creation
1. Research topic (optional)
2. Generate video script
3. Optimize for platform (YouTube)
4. Save to output/

### Newsletter Creation  
1. Research topics
2. Write newsletter sections
3. Optimize length and format
4. Save to output/

### Research & Analysis
1. Deep dive on topic
2. Gather latest information
3. Analyze trends
4. Generate report with sources

## Output

All generated content is saved to `output/`:
- `tutorial_video_output.txt` - Video scripts
- `newsletter_output.txt` - Newsletters
- `research_report.txt` - Research reports

Logs are saved to `logs/`:
- `content_creator.log`
- `researcher.log`
- etc.

## Moonshot Goal

Building towards **100K YouTube subscribers** in 18 months through:
- Regular tutorial videos
- Weekly newsletters
- AI-powered content at scale

Track progress in `config.py` → `KPI_TARGETS`

## Knowledge Base System

The platform includes a persistent vector database (ChromaDB) for knowledge storage and semantic search.

**Features:**
- Semantic search across all stored knowledge
- Multiple collections (research, facts, insights, content)
- Metadata tracking (source, agent, timestamp, confidence)
- Persistent storage across sessions
- Cross-agent knowledge sharing

**Usage:**
```python
from knowledge_base import KnowledgeBase

kb = KnowledgeBase()

# Add research findings
kb.add_research(
    topic="AI Model Performance",
    findings="GPT-4o-mini shows strong performance...",
    sources=["OpenAI Docs"],
    confidence=0.95
)

# Add verified facts
kb.add_fact(
    fact="ChromaDB is an open-source vector database",
    verified=True,
    confidence=1.0
)

# Semantic search
results = kb.search("AI model capabilities", n_results=5)

# Get statistics
stats = kb.get_stats()
print(f"Total knowledge items: {stats['total_knowledge']}")
```

**Test:**
```bash
python test_knowledge_base.py
```

## Next Steps

- [x] Add VerifierAgent for fact-checking
- [x] Add AnalystAgent for data analysis
- [x] Implement vector database for knowledge
- [ ] Integrate HeyGen/D-ID for avatar videos
- [ ] Add Telegram notifications

## License

Private project - All rights reserved
