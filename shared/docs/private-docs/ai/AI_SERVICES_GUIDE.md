# 🤖 AI Services - Setup & Nutzung

## Übersicht

Dieser Guide erklärt, wie AI-Services im Homelab konfiguriert und genutzt werden.

---

## 📍 Wo laufen AI-Services?

```
ThinkPad  →  Entwicklung & Tests
RTX1080   →  Production AI (GPU!)
VPS       →  Lightweight AI (Communicator, etc.)
```

---

## 🔑 API-Keys verwalten

### Zentrale Secrets-Datei

**Location:** `/opt/ai-services/.secrets/.env`

**Inhalt:**
```bash
# AI Models
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Voice/Video
ELEVENLABS_API_KEY=...
HEYGEN_API_KEY=...
```

### Keys rotieren (monatlich)

```bash
# 1. Neue Keys generieren:
#    - OpenAI: https://platform.openai.com/api-keys
#    - Anthropic: https://console.anthropic.com/settings/keys

# 2. Master Secrets updaten:
nano /home/fitna/J-Jeco/.env.master

# 3. Zu allen Systemen verteilen:
cd /home/fitna/J-Jeco
./sync-secrets.sh sync

# 4. Services neustarten:
docker-compose restart
```

---

## 🚀 AI-Agenten starten

### Content Creator Agent (RTX1080)

```bash
# SSH zu RTX1080
ssh proxmox-rtx1080

# Agent starten
cd ~/J-Jeco/1-first-agent
source ../ai-agents-masterclass/bin/activate
python agents/content_creator_agent.py
```

### Research Agent (RTX1080)

```bash
# Automated Research Pipeline
docker run -d \
  --name research-agent \
  --gpus all \
  -v /opt/ai-services/research:/data \
  -v /opt/ai-services/.secrets:/secrets:ro \
  --env-file /secrets/.env \
  jjeco/research-agent:latest
```

### Communicator Agent (VPS - Lightweight)

```bash
# SSH zu VPS
ssh jonas-homelab-vps

# Agent starten
cd ~/J-Jeco/1-first-agent
source ../ai-agents-masterclass/bin/activate
python main.py optimize-prompt "Dein Prompt"
```

---

## 🎬 Video-Generation

### HeyGen/D-ID Integration

**Script:**
```python
from agents.content_creator_agent import ContentCreatorAgent

agent = ContentCreatorAgent()

# Generate video script
script = await agent.generate_script(
    topic="Homelab für Anfänger",
    duration_minutes=10,
    language="de"
)

# Generate video with avatar
video_url = await agent.create_video(
    script=script,
    avatar="professional_male",
    voice="de-DE-Neural2-D"
)

print(f"Video URL: {video_url}")
```

---

## 📊 Monitoring

### GPU Usage (RTX1080)

```bash
# Real-time GPU monitoring
watch -n 1 nvidia-smi

# Grafana Dashboard:
# → http://192.168.17.1:3000/d/gpu-monitoring
```

### API Usage & Kosten

**Token Usage Tracking:**
```python
from agents.base_agent import BaseAgent

agent = BaseAgent(agent_type="content_creator")
metrics = agent.get_metrics()

print(f"Tokens used: {metrics['tokens_used']}")
print(f"Cost estimate: ${metrics['tokens_used'] * 0.00002}")  # GPT-4
```

---

## 🔧 Troubleshooting

### "API Key Invalid"

```bash
# 1. Check .env file exists:
ls -la /opt/ai-services/.secrets/.env

# 2. Check key format:
cat /opt/ai-services/.secrets/.env | grep API_KEY

# 3. Test key manually:
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer sk-YOUR-KEY"
```

### "Out of Memory" (GPU)

```bash
# 1. Check GPU memory:
nvidia-smi

# 2. Kill hung process:
nvidia-smi | grep python
kill <PID>

# 3. Reduce batch size in code
```

---

**Version:** 1.0
**Last Updated:** 2025-12-20
