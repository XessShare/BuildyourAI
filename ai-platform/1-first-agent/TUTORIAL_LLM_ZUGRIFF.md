# Tutorial: Zugriff auf Agents und verschiedene LLMs

## Übersicht

Dein J-Jeco AI Platform System ist bereits für mehrere LLMs konfiguriert. Dieses Tutorial zeigt dir, wie du:
1. Verschiedene LLM-APIs einrichtest
2. Agents mit spezifischen LLMs verwendest
3. Zwischen Modellen wechselst
4. Neue LLMs hinzufügst

---

## 1. API-Keys einrichten

### Schritt 1: API-Keys besorgen

**Claude (Anthropic)**
```bash
# Registriere dich auf: https://console.anthropic.com/
# Gehe zu: API Keys → Create Key
# Modelle: claude-3-5-sonnet, claude-3-opus, etc.
```

**Gemini (Google)**
```bash
# Registriere dich auf: https://makersuite.google.com/app/apikey
# Erstelle API Key
# Modelle: gemini-2.0-flash-exp, gemini-pro, etc.
```

**ChatGPT (OpenAI)**
```bash
# Registriere dich auf: https://platform.openai.com/api-keys
# Erstelle API Key
# Modelle: gpt-4o, gpt-4-turbo, gpt-4o-mini, etc.
```

**Perplexity (Optional für Online-Search)**
```bash
# Registriere dich auf: https://www.perplexity.ai/settings/api
# Erstelle API Key
# Modelle: llama-3.1-sonar-large-128k-online
```

### Schritt 2: .env Datei konfigurieren

```bash
# Kopiere das Template
cp .env.template .env

# Bearbeite die .env Datei
nano .env  # oder vim, code, etc.
```

Füge deine API-Keys ein:
```bash
# AI Model Configuration
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
GOOGLE_API_KEY=AIzaSyxxxxxxxxxxxxxxxxx
PERPLEXITY_API_KEY=pplx-xxxxxxxxxxxxx

# Optional AI Providers
MISTRAL_API_KEY=
GROQ_API_KEY=
COHERE_API_KEY=
TOGETHER_API_KEY=
```

---

## 2. Agents und ihre LLMs

### Aktuelle Agent-Konfiguration

Jeder Agent ist für eine spezifische Aufgabe mit einem optimalen Modell konfiguriert:

| Agent | Modell | Zweck | Temperature |
|-------|--------|-------|-------------|
| **project_manager** | Claude 3.5 Sonnet | Strategische Planung | 0.3 |
| **content_creator** | GPT-4o-mini | Content Erstellung | 0.8 |
| **researcher** | GPT-4o-mini + Perplexity | Recherche | 0.4 |
| **verifier** | GPT-4o-mini | Fact-Checking | 0.2 |
| **communicator** | Claude 3.5 Sonnet | Prompt Optimierung | 0.5 |
| **analyst** | Gemini 2.0 Flash | Datenanalyse | 0.3 |

---

## 3. Agents verwenden

### Option A: Python Script

```python
import asyncio
from agents.content_creator_agent import ContentCreatorAgent
from agents.researcher_agent import ResearcherAgent
from agents.project_manager_agent import ProjectManagerAgent

async def main():
    # 1. Content Creator (nutzt GPT-4o-mini)
    creator = ContentCreatorAgent()
    result = await creator.execute({
        "task_type": "video_script",
        "topic": "Claude vs ChatGPT vs Gemini Vergleich",
        "duration_minutes": 10
    })
    print("Content Creator Result:", result)

    # 2. Researcher (nutzt Perplexity für Online-Info)
    researcher = ResearcherAgent()
    research = await researcher.execute({
        "task_type": "deep_research",
        "topic": "Aktuelle AI Modell Benchmarks 2025"
    })
    print("Research Result:", research)

    # 3. Project Manager (nutzt Claude)
    pm = ProjectManagerAgent()
    plan = await pm.execute({
        "task_type": "create_plan",
        "project": "AI Tutorial Serie"
    })
    print("Project Plan:", plan)

if __name__ == "__main__":
    asyncio.run(main())
```

### Option B: Direkter Agent-Aufruf

```python
from agents.base_agent import BaseAgent
from agents.content_creator_agent import ContentCreatorAgent

async def quick_task():
    agent = ContentCreatorAgent()

    # Denken mit dem konfigurierten LLM
    response = await agent.think(
        prompt="Erkläre den Unterschied zwischen Claude und GPT-4",
        context="Für einen YouTube-Tutorial"
    )

    print(response)

    # Metrics anzeigen
    print(agent.get_metrics())
```

---

## 4. Zwischen LLMs wechseln

### Methode 1: config.py anpassen

```python
# In config.py
AGENT_CONFIG = {
    "content_creator": {
        "model": CLAUDE_MODEL,  # Wechsel von DEFAULT_MODEL zu CLAUDE_MODEL
        "temperature": 0.8,
        "role": "Creative content generator"
    }
}
```

### Methode 2: Custom Config zur Laufzeit

```python
from agents.content_creator_agent import ContentCreatorAgent

# Nutze Claude statt GPT
agent = ContentCreatorAgent(
    custom_config={
        "model": "claude-3-5-sonnet-20241022",
        "temperature": 0.7
    }
)
```

### Methode 3: Verschiedene Modelle für verschiedene Tasks

```python
async def multi_model_workflow():
    # GPT für kreative Tasks
    gpt_agent = ContentCreatorAgent()

    # Claude für analytische Tasks
    claude_agent = ContentCreatorAgent(
        custom_config={"model": "claude-3-5-sonnet-20241022"}
    )

    # Gemini für multimodale Tasks
    gemini_agent = ContentCreatorAgent(
        custom_config={"model": "gemini-2.0-flash-exp"}
    )

    # Parallel ausführen
    results = await asyncio.gather(
        gpt_agent.think("Erstelle einen catchy Titel"),
        claude_agent.think("Analysiere die Zielgruppe"),
        gemini_agent.think("Strukturiere den Content")
    )
```

---

## 5. Neue LLMs hinzufügen

### Beispiel: Mistral AI hinzufügen

**Schritt 1: API Key in .env**
```bash
MISTRAL_API_KEY=your_mistral_key_here
```

**Schritt 2: In config.py hinzufügen**
```python
# config.py
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "")
MISTRAL_MODEL = "mistral-large-latest"
```

**Schritt 3: BaseAgent erweitern**
```python
# In base_agent.py → _initialize_llm()

def _initialize_llm(self):
    model = self.config.get("model", "gpt-4-turbo-preview")
    temperature = self.config.get("temperature", 0.7)

    if "claude" in model.lower():
        return ChatAnthropic(...)
    elif "mistral" in model.lower():
        from langchain_mistralai import ChatMistralAI
        return ChatMistralAI(
            model=model,
            mistral_api_key=MISTRAL_API_KEY,
            temperature=temperature
        )
    else:
        return ChatOpenAI(...)
```

**Schritt 4: Requirements aktualisieren**
```bash
pip install langchain-mistralai
```

---

## 6. Praktische Workflows

### Workflow 1: Multi-Model Content Pipeline

```python
async def content_pipeline(topic: str):
    """
    Verwendet verschiedene LLMs für verschiedene Schritte
    """
    # 1. Recherche mit Perplexity (Online-Daten)
    researcher = ResearcherAgent()
    research_data = await researcher.execute({
        "task_type": "deep_research",
        "topic": topic
    })

    # 2. Planung mit Claude (Strategisch)
    pm = ProjectManagerAgent()
    content_plan = await pm.execute({
        "task_type": "create_content_plan",
        "research": research_data
    })

    # 3. Content Creation mit GPT (Kreativ)
    creator = ContentCreatorAgent()
    content = await creator.execute({
        "task_type": "video_script",
        "plan": content_plan
    })

    # 4. Analyse mit Gemini (Multimodal)
    from agents.base_agent import BaseAgent
    analyst = BaseAgent(
        agent_type="analyst"  # Nutzt Gemini
    )
    analysis = await analyst.think(
        "Analysiere und optimiere diesen Content",
        context=str(content)
    )

    return {
        "research": research_data,
        "plan": content_plan,
        "content": content,
        "analysis": analysis
    }
```

### Workflow 2: A/B Testing verschiedener Modelle

```python
async def compare_models(prompt: str):
    """
    Vergleiche Outputs von verschiedenen LLMs
    """
    from agents.base_agent import BaseAgent

    models = [
        ("GPT-4o", "gpt-4o"),
        ("Claude", "claude-3-5-sonnet-20241022"),
        ("Gemini", "gemini-2.0-flash-exp")
    ]

    results = {}

    for name, model in models:
        agent = BaseAgent(
            agent_type="content_creator",
            custom_config={"model": model}
        )

        response = await agent.think(prompt)
        results[name] = {
            "response": response,
            "tokens": agent.metrics["tokens_used"]
        }

    return results

# Verwendung
comparison = await compare_models(
    "Erkläre Quantencomputing in einfachen Worten"
)
for model, result in comparison.items():
    print(f"\n=== {model} ===")
    print(result["response"])
    print(f"Tokens: {result['tokens']}")
```

---

## 7. Kostenoptimierung

### Token-Kosten pro Modell (ca. Preise)

| Modell | Input (1M tokens) | Output (1M tokens) |
|--------|-------------------|-------------------|
| GPT-4o | $2.50 | $10.00 |
| GPT-4o-mini | $0.15 | $0.60 |
| Claude 3.5 Sonnet | $3.00 | $15.00 |
| Gemini 2.0 Flash | $0.10 | $0.30 |
| Perplexity Sonar | $1.00 | $1.00 |

### Strategie für Kosteneffizienz

```python
# In config.py
AGENT_CONFIG = {
    "content_creator": {
        "model": "gpt-4o-mini",  # Günstig für Masse
        "fallback_model": "gpt-4o"  # Premium wenn nötig
    },
    "researcher": {
        "model": "gemini-2.0-flash-exp",  # Sehr günstig
        "use_perplexity": True  # Nur für Online-Recherche
    },
    "project_manager": {
        "model": "claude-3-5-sonnet-20241022"  # Premium für wichtige Entscheidungen
    }
}
```

---

## 8. Testing & Debugging

### Test Script erstellen

```python
# test_all_models.py
import asyncio
from agents.base_agent import BaseAgent
from config import AGENT_CONFIG

async def test_all_models():
    """Teste ob alle konfigurierten Modelle funktionieren"""

    for agent_type, config in AGENT_CONFIG.items():
        print(f"\nTesting {agent_type} with {config['model']}...")

        try:
            agent = BaseAgent(
                agent_type=agent_type,
                custom_config=config
            )

            response = await agent.think(
                "Sage Hallo und nenne deinen Namen und Zweck."
            )

            print(f"✓ {agent_type} works!")
            print(f"  Response: {response[:100]}...")
            print(f"  Metrics: {agent.get_metrics()}")

        except Exception as e:
            print(f"✗ {agent_type} failed: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_all_models())
```

Ausführen:
```bash
python test_all_models.py
```

---

## 9. Best Practices

### 1. Model Selection Guide

- **Claude 3.5 Sonnet**: Lange Reasoning-Tasks, Code-Analyse, strategische Planung
- **GPT-4o**: Allzweck, gutes Preis-Leistungs-Verhältnis
- **GPT-4o-mini**: Bulk-Tasks, einfache Content-Erstellung
- **Gemini 2.0 Flash**: Sehr schnell, günstig, gut für Datenanalyse
- **Perplexity**: Nur für aktuelle Online-Informationen

### 2. Error Handling

```python
async def robust_agent_call(agent_type: str, prompt: str):
    """Agent-Aufruf mit Fallback"""
    try:
        agent = BaseAgent(agent_type=agent_type)
        return await agent.think(prompt)
    except Exception as e:
        print(f"Primary model failed: {e}")

        # Fallback zu günstigerem Modell
        agent = BaseAgent(
            agent_type=agent_type,
            custom_config={"model": "gpt-4o-mini"}
        )
        return await agent.think(prompt)
```

### 3. Rate Limiting

```python
import asyncio
from asyncio import Semaphore

async def batch_process(tasks: list, max_concurrent: int = 5):
    """Verhindere API Rate Limits"""
    semaphore = Semaphore(max_concurrent)

    async def process_with_limit(task):
        async with semaphore:
            agent = ContentCreatorAgent()
            return await agent.execute(task)

    return await asyncio.gather(*[
        process_with_limit(task) for task in tasks
    ])
```

---

## 10. Quick Reference

### Alle Agents nutzen
```bash
python run_agents.py
```

### Einzelnen Agent testen
```bash
python test_content_creator.py
python test_researcher.py
```

### Metrics anzeigen
```python
agent.get_metrics()
# Returns: {tasks_completed, tokens_used, errors, memory_size, uptime}
```

### Model zur Laufzeit wechseln
```python
agent = ContentCreatorAgent(
    custom_config={"model": "claude-3-5-sonnet-20241022"}
)
```

---

## Troubleshooting

### Problem: "API Key not found"
```bash
# Prüfe .env Datei
cat .env

# Stelle sicher dass dotenv geladen wird
pip install python-dotenv
```

### Problem: "Module not found: langchain_anthropic"
```bash
# Installiere fehlende Dependencies
pip install langchain-anthropic
pip install langchain-openai
pip install langchain-google-genai
```

### Problem: "Rate limit exceeded"
```python
# Reduziere concurrent requests
# Nutze Semaphore (siehe Best Practices)
# Oder wechsle zu günstigerem Modell
```

---

## Nächste Schritte

1. **API Keys einrichten**: Folge Schritt 1-2
2. **Test Script ausführen**: `python test_all_models.py`
3. **Ersten Workflow bauen**: Nutze Beispiele aus Abschnitt 6
4. **Kosten monitoren**: Logge Token-Usage für jeden Agent

Viel Erfolg mit deinem Multi-LLM Agent System!
