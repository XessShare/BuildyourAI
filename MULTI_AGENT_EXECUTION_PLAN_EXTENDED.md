# Multi-Agent Execution Plan - Self-Hosted Platform
**Created:** 2025-12-25  
**Status:** Active Execution  
**Goal:** Build comprehensive self-hosted platform with auth, AI, workflows, and Notion-like features

---

## 🎯 System Architecture

### Hardware Resources
```
┌─────────────────────────────────────────────────────────┐
│                 COMPUTE RESOURCES                        │
├─────────────────────────────────────────────────────────┤
│ 1. ThinkPad (192.168.16.7)                              │
│    - Role: Development & Testing                         │
│    - CPU: 4 cores, RAM: 8GB                             │
│    - Tasks: Light agents, documentation                  │
│                                                          │
│ 2. RTX1080 Proxmox (192.168.17.1)                       │
│    - Role: Production & AI Inference                     │
│    - CPU: 8 cores, RAM: 32GB, GPU: RTX 1080            │
│    - Tasks: LLM hosting, heavy AI workloads             │
│                                                          │
│ 3. Gaming PC (NEW - to be configured)                   │
│    - Role: Resource-intensive tasks                      │
│    - Specs: TBD (likely high-end CPU/GPU)               │
│    - Tasks: Video processing, training, heavy builds    │
│                                                          │
│ 4. VPS (91.107.198.37 - external)                       │
│    - Role: Public gateway                                │
│    - Tasks: Reverse proxy, webhooks, public services    │
└─────────────────────────────────────────────────────────┘
```

### LLM Resources (OSS - Already Installed)
- **Ollama** - Local LLM serving (Llama, Mistral, etc.)
- **Open WebUI** - To be integrated
- **LocalAI** - Alternative LLM backend (if needed)

---

## 🤖 Agent Distribution (5 Parallel Agents)

### Agent 1: Infrastructure Deployment Agent
**Context:** Deploy core homelab infrastructure  
**Hardware:** RTX1080 Proxmox  
**Dependencies:** None (can start immediately)  
**LLM:** GPT-4o-mini (for planning), local Ollama for execution

**Tasks:**
1. Bootstrap Proxmox hosts with Ansible
2. Deploy Docker Compose core stack (Traefik + Authentik)
3. Configure networking and firewall rules
4. Set up monitoring (Prometheus + Grafana)

**Output:** Running infrastructure ready for applications

**Commands:**
```bash
cd /home/fitna/homelab/infrastructure/ansible
ansible-playbook -i inventory/hosts.yml playbooks/00-bootstrap.yml
cd ../docker/stacks
docker compose -f core.yml up -d
docker compose -f monitoring.yml up -d
```

---

### Agent 2: Authentication & User Management Agent
**Context:** Implement multi-tier authentication system  
**Hardware:** RTX1080 Proxmox  
**Dependencies:** Agent 1 (needs Authentik running)  
**LLM:** Claude 3.5 Sonnet (for security design)

**User Tiers to Implement:**
```yaml
Admin:
  - Full system access
  - User management
  - Service configuration
  - RBAC: admin group

Angestellte (Employees):
  - Access to work tools (n8n, documents, AI)
  - Limited admin functions
  - RBAC: employees group

Freunde (Friends):
  - Access to shared services (media, chat)
  - No admin access
  - RBAC: friends group

Besucher (Visitors):
  - Read-only access to public content
  - Limited service access
  - RBAC: guests group

Self-Registration:
  - Public signup form
  - Email verification
  - Default: Besucher role
  - Manual approval for upgrade
```

**Tasks:**
1. Configure Authentik groups and permissions
2. Create OIDC applications for each service
3. Implement self-registration flow
4. Build user management UI (or use Authentik admin)
5. Set up email verification (SMTP)

**Deliverables:**
- Working SSO for all services
- User registration page
- Admin panel for user management

---

### Agent 3: AI Platform Integration Agent
**Context:** Integrate Open WebUI + OSS LLMs into homelab  
**Hardware:** RTX1080 Proxmox (GPU for inference)  
**Dependencies:** Agent 1 (infrastructure), Agent 2 (auth)  
**LLM:** Gemini 2.0 Flash (for integration planning)

**Components:**
1. **Open WebUI** (ChatGPT-like interface)
   - Integrate with Ollama backend
   - Connect to Authentik SSO
   - Multi-user support
   - Model switching (Llama, Mistral, etc.)

2. **OSS LLM Stack:**
   - Ollama (already installed?)
   - Models: Llama 3, Mistral, CodeLlama
   - GPU acceleration via RTX 1080

3. **AI Features:**
   - Document Q&A (RAG)
   - Code generation
   - Workflow assistance
   - Multi-modal (text + image)

**Tasks:**
1. Deploy Open WebUI via Docker
2. Configure Ollama backend
3. Integrate Authentik SSO
4. Pull and test LLM models
5. Create user onboarding guide

**Docker Compose:**
```yaml
# Add to infrastructure/docker/stacks/ai-platform.yml
services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    ports:
      - "3000:8080"
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
      - OPENID_PROVIDER_URL=https://auth.yourdomain.com/application/o/open-webui/
    volumes:
      - open-webui-data:/app/backend/data
    depends_on:
      - ollama

  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama-data:/root/.ollama
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

---

### Agent 4: Notion Alternative & Productivity Suite Agent
**Context:** Deploy self-hosted Notion + Sider.AI alternatives  
**Hardware:** ThinkPad (development), RTX1080 (production)  
**Dependencies:** Agent 2 (auth), Agent 3 (AI)  
**LLM:** Perplexity (for research), GPT-4o-mini (for implementation)

**Notion Alternatives to Deploy:**

#### Option A: AppFlowy (Recommended)
- Open-source Notion clone
- Self-hostable
- Offline-first
- Blocks, databases, kanban

#### Option B: Anytype
- P2P knowledge base
- Local-first
- Encrypted

#### Option C: Outline
- Team wiki
- Markdown-based
- Slack integration

**Sider.AI Features to Replicate:**

1. **AI Sidebar/Assistant:**
   - Browser extension (optional)
   - Inline AI suggestions
   - Context-aware help

2. **Document Processing:**
   - PDF summarization
   - OCR for images
   - Translation

3. **Workflow Automation:**
   - Template generation
   - Auto-tagging
   - Smart search

**Implementation Stack:**
```yaml
Services:
  - AppFlowy (Notion clone)
  - Paperless-ngx (Document management + OCR)
  - Memos (Quick notes)
  - Hedgedoc (Collaborative markdown)
  - Excalidraw (Whiteboard)
  
AI Integration:
  - Open WebUI API for AI features
  - Custom scripts for automation
  - n8n workflows for document processing
```

**Tasks:**
1. Deploy AppFlowy via Docker
2. Set up Paperless-ngx for document management
3. Integrate with Authentik SSO
4. Connect AI assistant (Open WebUI API)
5. Create templates and workflows

---

### Agent 5: Workflow & Automation Platform Agent
**Context:** Deploy n8n for workflow orchestration + homelab integration  
**Hardware:** RTX1080 Proxmox  
**Dependencies:** All agents (needs full stack)  
**LLM:** Claude 3.5 Sonnet (for workflow design)

**n8n Workflow Platform:**
- Visual workflow builder
- 300+ integrations
- Self-hosted Zapier alternative
- Cron jobs, webhooks, API calls

**Workflows to Create:**

1. **User Onboarding:**
   - New user registers → Email verification → Welcome email + setup guide
   
2. **Document Processing:**
   - Upload PDF → OCR → Summarize (AI) → Store in AppFlowy → Notify user

3. **AI Content Generation:**
   - Template request → Open WebUI API → Format → Save to Notion

4. **Monitoring Alerts:**
   - Prometheus alert → n8n → Telegram/Email notification

5. **Backup Automation:**
   - Daily: Trigger restic backup → Verify → Log to Grafana

**Tasks:**
1. Deploy n8n via Docker
2. Configure Authentik SSO
3. Create webhook endpoints
4. Build 5 example workflows
5. Document workflow creation guide

**Docker Compose:**
```yaml
services:
  n8n:
    image: n8nio/n8n:latest
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=false
      - N8N_AUTH_TYPE=oidc
      - N8N_OIDC_ISSUER=https://auth.yourdomain.com/application/o/n8n/
    volumes:
      - n8n-data:/home/node/.n8n
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.n8n.rule=Host(`n8n.yourdomain.com`)"
```

---

## 🏗️ Gaming PC Integration

### Configuration Steps:
1. **Install Proxmox VE or Docker** on Gaming PC
2. **Add to Ansible inventory:**
   ```yaml
   gaming-pc:
     ansible_host: 192.168.X.X  # Gaming PC IP
     role: heavy_compute
     cpu_cores: 12  # Example
     memory_gb: 64  # Example
     gpu: RTX 3080  # Example
   ```

3. **Resource Allocation:**
   - Video encoding (Jellyfin transcoding)
   - AI model training
   - Heavy Docker builds
   - Large-scale data processing

4. **Services to Deploy on Gaming PC:**
   - Ollama with larger models (70B+ parameters)
   - Stable Diffusion WebUI
   - Video processing queue
   - CI/CD runners

---

## 📋 Execution Timeline

### Phase 1: Foundation (Week 1)
- **Agent 1:** Deploy infrastructure ✅
- **Gaming PC:** Add to inventory and bootstrap

### Phase 2: Authentication (Week 1-2)
- **Agent 2:** Configure Authentik with 4 user tiers
- Test SSO integration

### Phase 3: AI Platform (Week 2)
- **Agent 3:** Deploy Open WebUI + Ollama
- Test LLM inference on RTX 1080

### Phase 4: Productivity Suite (Week 2-3)
- **Agent 4:** Deploy AppFlowy + Paperless-ngx
- Integrate AI features

### Phase 5: Automation (Week 3)
- **Agent 5:** Deploy n8n
- Create initial workflows

### Phase 6: Integration & Testing (Week 4)
- End-to-end testing
- User onboarding documentation
- Performance tuning

---

## 🎨 UI/UX Design Goals

### Inspired by Notion + Sider.AI:

**Visual Design:**
- Clean, modern interface
- Dark mode support
- Responsive (mobile + desktop)
- Consistent design system

**Features:**
- Drag-and-drop blocks
- Real-time collaboration
- AI assistant sidebar
- Quick command palette (Cmd+K)
- Smart search with AI

**Navigation:**
- Sidebar with workspaces
- Breadcrumb navigation
- Recent pages
- Favorites/bookmarks

---

## 🔐 Security Architecture

```
Internet → VPS (Cloudflare Tunnel) → Traefik → Authentik SSO
                                              ↓
                                    Check user tier (Admin/Employee/Friend/Guest)
                                              ↓
                                    Route to allowed services
```

**Access Control Matrix:**
| Service | Admin | Employee | Friend | Guest |
|---------|-------|----------|--------|-------|
| Authentik Admin | ✅ | ❌ | ❌ | ❌ |
| n8n Workflows | ✅ | ✅ | ❌ | ❌ |
| Open WebUI | ✅ | ✅ | ✅ | View only |
| AppFlowy | ✅ | ✅ | ✅ | Public pages |
| Jellyfin | ✅ | ✅ | ✅ | ✅ |
| Grafana | ✅ | ✅ | View only | ❌ |
| Portainer | ✅ | ❌ | ❌ | ❌ |

---

## 📊 Success Criteria

- [ ] 4-tier authentication working (Admin, Employee, Friend, Guest)
- [ ] Self-registration with email verification
- [ ] Open WebUI accessible with OSS LLMs
- [ ] Notion-like workspace deployed (AppFlowy)
- [ ] Document processing pipeline (upload → OCR → AI summary)
- [ ] n8n with 5+ working workflows
- [ ] Gaming PC integrated as compute node
- [ ] All services behind Authentik SSO
- [ ] Mobile-responsive UI
- [ ] User documentation complete

---

## 🚀 Next Steps (Immediate)

1. **Start Agent 1:** Infrastructure deployment
2. **Document Gaming PC specs** for inventory
3. **Test Ollama** on RTX 1080 Proxmox
4. **Research AppFlowy deployment** options
5. **Design Authentik user groups** and permissions

---

**End of Execution Plan**

**Agents: Ready for parallel execution**  
**Timeline: 4 weeks to full deployment**  
**Priority: Security → AI → Productivity → Automation**
