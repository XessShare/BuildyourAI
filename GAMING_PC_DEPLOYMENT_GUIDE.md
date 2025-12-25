# 🎮 Gaming PC Deployment Guide - FINALIZED

**Host:** Arch Linux Gaming PC  
**IP:** 192.168.16.2 (needs confirmation - Arch hostname -I failed)  
**Hardware:** Ryzen 9 5900X (12C/24T) + RX 6800 XT (16GB) + 32GB RAM  
**Storage:** 930GB total, 390GB free (59% used)  
**Status:** ✅ ROCm INSTALLED & WORKING  
**Docker:** ✅ v29.1.3 installed  
**Network:** ✅ ThinkPad & RTX1080 reachable  
**24/7:** ✅ Confirmed

---

## 🚀 IMMEDIATE DEPLOYMENT STEPS

### Step 1: Verify IP Address (2 min)

**On Gaming PC (Arch Linux):**
```bash
# Arch uses different command
ip -4 addr show | grep inet | grep -v 127.0.0.1 | awk '{print $2}' | cut -d/ -f1

# Or check with:
ip route get 8.8.8.8 | awk '{print $7; exit}'
```

**Send me the IP, then I'll update inventory.**

---

### Step 2: Copy Files to Gaming PC (5 min)

**From ThinkPad or wherever you have homelab repo:**

```bash
# Copy AI stack compose file
scp /home/fitna/homelab/infrastructure/docker/stacks/gaming-pc-ai.yml \
    root@192.168.16.2:/opt/homelab/

# Or if using different user:
scp /home/fitna/homelab/infrastructure/docker/stacks/gaming-pc-ai.yml \
    youruser@192.168.16.2:~/gaming-pc-ai.yml
```

---

### Step 3: Deploy Services (10 min)

**On Gaming PC:**

```bash
# Create directories
sudo mkdir -p /opt/homelab /mnt/media

# Create Docker network (if not exists)
docker network create homelab_network 2>/dev/null || echo "Network exists"

# Deploy AI stack
cd /opt/homelab
docker compose -f gaming-pc-ai.yml up -d

# Check status
docker ps
docker compose -f gaming-pc-ai.yml logs -f
```

---

### Step 4: Pull AI Models (30-60 min)

**Large models only Gaming PC can handle:**

```bash
# DeepSeek Coder 33B (RTX 1080 can't run this!)
docker exec ollama-amd ollama pull deepseek-coder:33b

# Mixtral 8x7B Instruct (quantized to fit 16GB)
docker exec ollama-amd ollama pull mixtral:8x7b-instruct-v0.1-q4_K_M

# Llama 3 70B (4-bit quantized - frontier model!)
docker exec ollama-amd ollama pull llama3:70b-instruct-q4_K_M

# CodeLlama 34B
docker exec ollama-amd ollama pull codellama:34b-instruct-q4_K_M

# Check available models
docker exec ollama-amd ollama list
```

**Stable Diffusion models (auto-download on first use):**
- SDXL Base 1.0 (~6.9GB)
- SD 1.5 (~4GB)
- Downloaded to `/data/models/Stable-diffusion/`

---

### Step 5: Test Services (10 min)

**Ollama AMD API:**
```bash
# Test API endpoint
curl http://192.168.16.2:11435/api/tags

# Generate with large model
curl http://192.168.16.2:11435/api/generate -d '{
  "model": "deepseek-coder:33b",
  "prompt": "Write a Python function to calculate Fibonacci numbers",
  "stream": false
}'
```

**Stable Diffusion WebUI:**
```bash
# Access via Traefik
curl -I https://sd.${DOMAIN}

# Or direct (if Traefik not set up yet)
curl -I http://192.168.16.2:7860
```

**ComfyUI:**
```bash
curl -I http://192.168.16.2:8188
```

---

## 🔧 Integration with Existing Homelab

### Open WebUI Multi-Backend Configuration

**Add AMD backend to Open WebUI environment:**

**On RTX1080 host (192.168.17.1), edit automation.yml:**

```yaml
  open-webui:
    # ... existing config ...
    environment:
      # Existing NVIDIA backend
      - OLLAMA_BASE_URL=http://ollama:11434
      
      # NEW: Add AMD backend
      - OLLAMA_API_URLS=http://ollama:11434;http://192.168.16.2:11435
      - OLLAMA_API_NAMES=NVIDIA RTX 1080 (8B models);AMD RX 6800 XT (70B models)
```

**Restart Open WebUI:**
```bash
docker compose -f automation.yml restart open-webui
```

**Now users can select:**
- **RTX 1080:** Fast 7B-13B models (llama3:8b, mistral:7b)
- **RX 6800 XT:** Large 33B-70B models (deepseek:33b, llama3:70b)

---

### n8n Workflow Integration

**Image Generation Workflow:**

**Nodes:**
1. **Webhook Trigger** - Receives request (prompt, style, size)
2. **HTTP Request** - POST to Stable Diffusion API
   - URL: `http://192.168.16.2:7860/sdapi/v1/txt2img`
   - Body: 
     ```json
     {
       "prompt": "{{$json.prompt}}",
       "negative_prompt": "ugly, blurry, low quality",
       "width": 1024,
       "height": 1024,
       "steps": 30,
       "sampler_name": "DPM++ 2M Karras"
     }
     ```
3. **Code Node** - Extract image from response
4. **HTTP Request** - Upload to Outline or Paperless
5. **Send Response** - Return image URL

**Large Model Inference Workflow:**

**Nodes:**
1. **Manual Trigger** or **Schedule**
2. **HTTP Request** - POST to Ollama AMD
   - URL: `http://192.168.16.2:11435/api/generate`
   - Body:
     ```json
     {
       "model": "deepseek-coder:33b",
       "prompt": "{{$json.task}}",
       "stream": false
     }
     ```
3. **Set Node** - Format response
4. **Create Outline Document** - Save result

---

## 📊 Service URLs (via Traefik)

| Service | URL | Backend Port | VRAM Usage |
|---------|-----|--------------|------------|
| Ollama AMD | `https://ollama-amd.${DOMAIN}` | 11435 | 8-14GB |
| Stable Diffusion | `https://sd.${DOMAIN}` | 7860 | 6-12GB |
| ComfyUI | `https://comfy.${DOMAIN}` | 8188 | 8-14GB |
| Jellyfin GPU | `https://media.${DOMAIN}` | 8096 | 2-4GB |

**Total VRAM:** Can run 1-2 services simultaneously (SDXL + Ollama 70B won't fit together)

---

## 🎯 Recommended Usage Patterns

### Pattern 1: On-Demand Large Models
- Keep Ollama AMD running 24/7 with NO models loaded
- Load models on-demand via API calls
- Auto-unload after 5 min idle (Ollama default)

### Pattern 2: Dedicated Services
- **Daytime (9-17h):** Stable Diffusion WebUI (for team)
- **Evening (17-23h):** Large model inference (Ollama 70B)
- **Night (23-9h):** ComfyUI batch workflows

### Pattern 3: Multi-User Load Balancing
- **Small prompts (<1000 tokens):** Route to RTX 1080
- **Large prompts (>1000 tokens):** Route to RX 6800 XT
- **Image generation:** Always RX 6800 XT (16GB VRAM)

---

## 🔍 Monitoring & Management

### GPU Monitoring

**Check GPU usage:**
```bash
# Real-time monitoring
watch -n 1 rocm-smi

# Detailed stats
rocm-smi --showmeminfo all --showuse
```

**Add to Grafana (Optional):**
```bash
# Export metrics for Prometheus
docker run -d \
  --name amd-exporter \
  --device /dev/kfd \
  --device /dev/dri \
  -p 9101:9101 \
  ghcr.io/platina-ai/rocm_smi_prometheus_exporter:latest
```

### Container Resource Usage

```bash
# Real-time stats
docker stats

# Specific container
docker stats ollama-amd stable-diffusion comfyui

# Logs
docker logs -f ollama-amd
docker logs -f stable-diffusion --tail 100
```

---

## ⚠️ Important Notes

### GPU Memory Management

**RX 6800 XT (16GB VRAM) can run:**
- ✅ 1x 70B model (q4) = ~14GB
- ✅ SDXL alone = ~10GB
- ✅ ComfyUI complex workflow = ~12GB
- ❌ SDXL + 70B simultaneously = OOM (Out of Memory)

**Solution:** Auto-unload models in Ollama (default 5 min timeout)

### Arch Linux Specific

**Docker service management:**
```bash
# Enable Docker on boot
sudo systemctl enable docker

# Start now
sudo systemctl start docker

# Check status
systemctl status docker
```

**ROCm updates:**
```bash
# Update ROCm (Arch)
sudo pacman -Syu rocm-hip-sdk rocm-opencl-sdk

# Check version
pacman -Q | grep rocm
```

### Firewall (if enabled)

```bash
# Allow Docker ports
sudo ufw allow 11435/tcp comment 'Ollama AMD'
sudo ufw allow 7860/tcp comment 'Stable Diffusion'
sudo ufw allow 8188/tcp comment 'ComfyUI'
sudo ufw allow 8096/tcp comment 'Jellyfin'

# Or allow entire subnet
sudo ufw allow from 192.168.0.0/16
```

---

## 🐛 Troubleshooting

### Issue: GPU not detected in container

**Check:**
```bash
# Host GPU access
rocm-smi

# Container GPU access
docker exec ollama-amd rocm-smi

# If fails, check devices
ls -la /dev/kfd /dev/dri/
```

**Fix:**
```bash
# Add user to groups
sudo usermod -aG render,video $USER

# Reboot or re-login
```

### Issue: ROCm version mismatch

**Error:** `HSA_OVERRIDE_GFX_VERSION` not working

**Fix:**
```yaml
environment:
  - HSA_OVERRIDE_GFX_VERSION=10.3.0  # For RX 6800 XT (gfx1030)
  # Try alternatives:
  # - HSA_OVERRIDE_GFX_VERSION=10.3.1
```

### Issue: Out of memory (OOM)

**Symptoms:** Container crashes, `docker logs` shows memory errors

**Fix:**
1. Reduce concurrent services
2. Use smaller quantized models (q4 instead of q5)
3. Limit Docker memory:
   ```yaml
   deploy:
     resources:
       limits:
         memory: 20G
   ```

---

## 📋 Ansible Integration (Optional)

**Update inventory:**

```bash
# Edit hosts.yml
nano /home/fitna/homelab/infrastructure/ansible/inventory/hosts.yml

# Add gaming-pc entry from gaming-pc-update.yml
# Update ansible_host with actual IP from Step 1
```

**Bootstrap gaming PC:**

```bash
cd /home/fitna/homelab/infrastructure/ansible

# Test connectivity
ansible gaming-pc -i inventory/hosts.yml -m ping

# Bootstrap (if needed)
ansible-playbook -i inventory/hosts.yml playbooks/00-bootstrap.yml --limit gaming-pc
```

---

## ✅ Deployment Checklist

**Pre-deployment:**
- [ ] Confirmed IP address (Step 1)
- [ ] Docker network created (`homelab_network`)
- [ ] Copied `gaming-pc-ai.yml` to host
- [ ] Verified ROCm working (`rocm-smi`)

**Deployment:**
- [ ] Deployed services (`docker compose up -d`)
- [ ] All containers running (`docker ps`)
- [ ] Pulled large models (70B, 33B)

**Testing:**
- [ ] Ollama AMD API responding (port 11435)
- [ ] Stable Diffusion WebUI accessible (port 7860)
- [ ] ComfyUI accessible (port 8188)
- [ ] GPU being utilized (`rocm-smi`)

**Integration:**
- [ ] Added to Open WebUI multi-backend
- [ ] Created n8n workflows
- [ ] Updated Ansible inventory
- [ ] Added to monitoring (Grafana)

---

## 🎉 Success Metrics

**After deployment, you should have:**
- ✅ **70B parameter LLM** running (impossible on RTX 1080!)
- ✅ **Stable Diffusion XL** with 16GB VRAM
- ✅ **ComfyUI** for advanced workflows
- ✅ **4K video transcoding** with AMD VCE/VCN
- ✅ **24/7 availability** for AI workloads

**Performance comparison:**
- RTX 1080: Max 13B models, SD 1.5
- **RX 6800 XT: Max 70B models, SDXL, ComfyUI**

---

**Status:** READY TO DEPLOY  
**Next Action:** Get IP address from Step 1, then proceed with deployment!

**Estimated Total Time:** 60-90 minutes (including model downloads)
