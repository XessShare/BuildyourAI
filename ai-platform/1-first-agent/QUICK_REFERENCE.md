# Quick Reference: LLM & Agents Zugriff

## Schnellstart

### 1. API Keys einrichten (einmalig)
```bash
cp .env.template .env
nano .env  # Füge deine API Keys ein
```

### 2. System testen
```bash
python test_all_models.py
```

### 3. Beispiele ausführen
```bash
python examples/multi_model_workflow.py
```

---

## Wichtigste Kommandos

### Einen Agent verwenden
```python
from agents.content_creator_agent import ContentCreatorAgent
import asyncio

async def main():
    agent = ContentCreatorAgent()
    result = await agent.execute({
        "task_type": "video_script",
        "topic": "Dein Thema hier"
    })
    print(result)

asyncio.run(main())
```

### Modell zur Laufzeit wechseln
```python
# Nutze Claude statt Standard-Modell
agent = ContentCreatorAgent(
    custom_config={"model": "claude-3-5-sonnet-20241022"}
)

# Nutze Gemini
agent = ContentCreatorAgent(
    custom_config={"model": "gemini-2.0-flash-exp"}
)
```

### Mehrere Modelle vergleichen
```python
models = ["gpt-4o-mini", "claude-3-5-sonnet-20241022", "gemini-2.0-flash-exp"]

for model in models:
    agent = BaseAgent("test", custom_config={"model": model})
    response = await agent.think("Deine Frage hier")
    print(f"{model}: {response}")
```

---

## Verfügbare Modelle

| Modell | API Key | Kosten | Gut für |
|--------|---------|--------|---------|
| `gpt-4o-mini` | OPENAI | € | Bulk-Tasks |
| `gpt-4o` | OPENAI | €€ | Allzweck |
| `claude-3-5-sonnet-20241022` | ANTHROPIC | €€€ | Reasoning, Code |
| `gemini-2.0-flash-exp` | GOOGLE | € | Schnell, günstig |
| `llama-3.1-sonar-large-128k-online` | PERPLEXITY | €€ | Online-Recherche |

---

## Agents & ihre Default-Modelle

```python
AGENT_CONFIG = {
    "project_manager": "claude-3-5-sonnet-20241022",
    "content_creator": "gpt-4o-mini",
    "researcher": "gpt-4o-mini + perplexity",
    "verifier": "gpt-4o-mini",
    "communicator": "claude-3-5-sonnet-20241022",
    "analyst": "gemini-2.0-flash-exp"
}
```

---

## Häufige Patterns

### Pattern 1: Multi-Step mit verschiedenen Modellen
```python
# 1. Recherche (Perplexity)
researcher = ResearcherAgent()
data = await researcher.execute({"topic": "AI Trends"})

# 2. Planung (Claude)
pm = ProjectManagerAgent()
plan = await pm.execute({"research": data})

# 3. Content (GPT)
creator = ContentCreatorAgent()
content = await creator.execute({"plan": plan})
```

### Pattern 2: Kostenoptimierung
```python
# Nutze günstiges Modell für erste Iteration
cheap_agent = BaseAgent("test", {"model": "gemini-2.0-flash-exp"})
draft = await cheap_agent.think("Schreibe einen Entwurf")

# Nutze Premium-Modell für Verfeinerung
premium_agent = BaseAgent("test", {"model": "claude-3-5-sonnet-20241022"})
final = await premium_agent.think(f"Verbessere: {draft}")
```

### Pattern 3: Fallback bei Fehler
```python
try:
    agent = BaseAgent("test", {"model": "claude-3-5-sonnet-20241022"})
    result = await agent.think(prompt)
except Exception:
    # Fallback zu günstigerem Modell
    agent = BaseAgent("test", {"model": "gpt-4o-mini"})
    result = await agent.think(prompt)
```

---

## API Keys besorgen

1. **OpenAI (ChatGPT)**: https://platform.openai.com/api-keys
2. **Anthropic (Claude)**: https://console.anthropic.com/
3. **Google (Gemini)**: https://makersuite.google.com/app/apikey
4. **Perplexity**: https://www.perplexity.ai/settings/api

---

## Troubleshooting

### "API Key not found"
```bash
# Prüfe ob .env Datei existiert
ls -la .env

# Prüfe ob Keys gesetzt sind
grep API_KEY .env
```

### "Module not found"
```bash
pip install -r requirements.txt
```

### "Rate limit exceeded"
- Reduziere concurrent requests
- Wechsle zu Modell mit höherem Limit
- Füge `await asyncio.sleep(1)` zwischen Calls ein

---

## Kostenübersicht (ca.)

| Modell | 1M Input Tokens | 1M Output Tokens |
|--------|----------------|------------------|
| GPT-4o-mini | $0.15 | $0.60 |
| GPT-4o | $2.50 | $10.00 |
| Claude 3.5 | $3.00 | $15.00 |
| Gemini Flash | $0.10 | $0.30 |
| Perplexity | $1.00 | $1.00 |

**Tipp**: 1M tokens ≈ 750.000 Wörter

---

## Weitere Ressourcen

- **Vollständiges Tutorial**: `TUTORIAL_LLM_ZUGRIFF.md`
- **Test Script**: `test_all_models.py`
- **Beispiele**: `examples/multi_model_workflow.py`
- **Konfiguration**: `config.py`

---

## Support

Bei Fragen:
1. Prüfe Tutorial: `TUTORIAL_LLM_ZUGRIFF.md`
2. Führe Test aus: `python test_all_models.py`
3. Prüfe Logs: `logs/*.log`
