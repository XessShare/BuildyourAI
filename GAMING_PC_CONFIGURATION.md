# Gaming PC Configuration - Ryzen 9 5900X + RX 6800 XT

**Created:** 2025-12-25  
**Status:** Ready for Integration  
**Hardware Class:** High-Performance Compute Node

---

## 🖥️ Hardware Specifications

### CPU: AMD Ryzen 9 5900X
- **Architecture:** Zen 3
- **Cores/Threads:** 12 cores / 24 threads
- **Base Clock:** 3.7 GHz
- **Boost Clock:** 4.8 GHz
- **TDP:** 105W
- **PCIe:** Gen 4.0
- **Performance:** ~30,000 PassMark score

### GPU: AMD Radeon RX 6800 XT
- **Architecture:** RDNA 2 (Big Navi)
- **VRAM:** 16GB GDDR6
- **Compute Units:** 72 CUs (4608 Stream Processors)
- **Memory Bandwidth:** 512 GB/s
- **TDP:** 300W
- **Ray Tracing:** Yes (Hardware accelerated)
- **ROCm Support:** Yes (AMD's CUDA equivalent)

### Memory
- **Capacity:** 32GB DDR4
- **Estimated Speed:** 3200-3600 MHz (typical for Ryzen 5900X)

### Total System Power
- **Idle:** ~80-100W
- **Load:** ~450-500W
- **24/7 Monthly Cost:** ~€30-40 (@ 0.30€/kWh, 100W average)

---

## 💡 Current Setup Analysis

### OS Configuration
- **Primary:** Linux (currently booted)
- **Secondary:** Windows (separate partition, bootable)
- **Dual-Boot:** Yes (Option 3 - confirmed)

### Network
- **Current Access:** Via Traefik proxy (reverse proxy in front)
- **Direct IP:** NEEDS DETERMINATION
- **Network Segment:** Likely same as other hosts (192.168.x.x)

### 24/7 Availability
- **Status:** NOT SPECIFIED
- **Recommendation:** Needed for GPU workloads (AI training, transcoding)
- **Alternative:** On-demand wake-on-LAN

---

## 🚨 CRITICAL: Missing Information

**Need to determine:**

1. **Direct IP Address:**
   ```bash
   # On gaming PC, run:
   ip addr show | grep "inet " | grep -v 127.0.0.1
   # Or: hostname -I
   ```

2. **Current Linux Distribution:**
   ```bash
   cat /etc/os-release | grep -E "^NAME=|^VERSION="
   # Is it Ubuntu, Debian, Arch, Fedora?
   ```

3. **Docker Status:**
   ```bash
   docker --version
   systemctl status docker
   ```

4. **ROCm (AMD GPU compute) Installed?**
   ```bash
   rocm-smi || rocminfo || echo "Not installed"
   ```

5. **Available Storage:**
   ```bash
   df -h | grep -E "/$|/home"
   ```

6. **24/7 Availability Decision:**
   - Can it run 24/7 for AI workloads?
   - Or on-demand only?

---

## 🎯 Recommended Service Allocation

### High Priority (GPU-Intensive)

**1. Stable Diffusion WebUI** 🎨
- **VRAM Required:** 8-12GB
- **Why RX 6800 XT is perfect:** 16GB VRAM > most NVIDIA cards
- **ROCm Support:** Excellent for AMD GPUs
- **Use Case:** Image generation, AI art
- **Performance:** Comparable to RTX 3080 Ti

**2. Ollama - Large Language Models** 🤖
- **Current:** Running on RTX 1080 (8GB VRAM limit)
- **Upgrade:** RX 6800 XT can run 70B parameter models
- **Models to host:**
  - Llama 3 70B (needs ~40GB with quantization → use 4-bit)
  - Mixtral 8x7B (needs ~26GB → fits in 16GB quantized)
  - DeepSeek Coder 33B (~18GB → fits!)
- **ROCm:** Full support for Ollama

**3. Video Transcoding** 🎬
- **Current:** Jellyfin uses Intel QSV on ThinkPad
- **Upgrade:** AMD VCE/VCN encoder on RX 6800 XT
- **Performance:** 4K HEVC encoding at 60+ FPS
- **Benefit:** Offload from ThinkPad

**4. ComfyUI (Advanced Stable Diffusion)** 🖼️
- **VRAM:** 10-14GB for complex workflows
- **AMD Support:** Native ROCm
- **Use Case:** Advanced AI image workflows

### Medium Priority (CPU-Intensive)

**5. Docker Build Agents** 🏗️
- **Use Case:** CI/CD pipelines, large builds
- **Ryzen 5900X:** 24 threads for parallel builds
- **Example:** Building OpenWebUI, Outline, etc.

**6. Data Processing** 📊
- **Workloads:** Pandas, Spark, ML preprocessing
- **Benefit:** 12 cores for parallel processing

**7. Backup Target** 💾
- **If Windows partition has free space**
- **Use Case:** Restic backup destination

### Low Priority (Gaming PC Specific)

**8. Gaming VM (when needed)** 🎮
- **If using Proxmox:** GPU passthrough to Windows VM
- **Dual-Boot:** Just reboot to Windows partition

---

## 🏗️ Ansible Inventory Entry

**File:** `/home/fitna/homelab/infrastructure/ansible/inventory/hosts.yml`

```yaml
    gaming-pc:
      ansible_host: [NEEDS_IP]  # TODO: Get from `hostname -I`
      ansible_user: root  # Or your Linux user
      role: heavy_compute_gpu
      cpu_model: AMD Ryzen 9 5900X
      cpu_cores: 12
      cpu_threads: 24
      memory_gb: 32
      gpu_vendor: amd
      gpu_model: Radeon RX 6800 XT
      gpu_vram_gb: 16
      gpu_compute: rocm  # AMD's CUDA equivalent
      storage_gb: [NEEDS_CHECK]
      dual_boot: true
      dual_boot_os: windows
      network_speed: 1000  # Assume gigabit, verify
      power_mode: on_demand  # Change to "24_7" if decided
```

**Add to groups:**
```yaml
docker_hosts:
  hosts:
    pve-thinkpad:
    pve-ryzen:
    gaming-pc:  # Add here

gpu_hosts:
  hosts:
    pve-ryzen:  # RTX 1080 (NVIDIA)
    gaming-pc:  # RX 6800 XT (AMD)
  vars:
    gpu_passthrough_enabled: true

amd_gpu_hosts:  # New group for ROCm
  hosts:
    gaming-pc:
  vars:
    rocm_version: "6.0"  # Latest ROCm
    amdgpu_driver: amdgpu-pro  # Or mesa
```

---

## 🐳 Docker Compose - AMD GPU Configuration

### ROCm GPU Passthrough (AMD equivalent of NVIDIA CUDA)

**For Ollama with AMD GPU:**

```yaml
  ollama-amd:
    image: ollama/ollama:rocm  # AMD-specific image
    container_name: ollama-amd
    restart: unless-stopped
    networks:
      - homelab_network
    ports:
      - "11435:11434"  # Different port from RTX1080 Ollama
    environment:
      - TZ=${TZ}
      - OLLAMA_HOST=0.0.0.0
      - HSA_OVERRIDE_GFX_VERSION=10.3.0  # For RX 6800 XT
    volumes:
      - ollama_amd_data:/root/.ollama
    devices:
      - /dev/kfd  # ROCm kernel driver
      - /dev/dri  # AMD GPU access
    group_add:
      - video
      - render
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.ollama-amd.rule=Host(`ollama-amd.${DOMAIN}`)"
      - "traefik.http.routers.ollama-amd.entrypoints=websecure"
      - "traefik.http.routers.ollama-amd.tls.certresolver=cloudflare"
      - "traefik.http.services.ollama-amd.loadbalancer.server.port=11434"
```

**For Stable Diffusion WebUI:**

```yaml
  stable-diffusion-webui:
    image: rocm/pytorch:latest  # AMD base image
    container_name: stable-diffusion
    restart: unless-stopped
    networks:
      - homelab_network
    ports:
      - "7860:7860"
    environment:
      - TZ=${TZ}
      - CLI_ARGS=--listen --enable-insecure-extension-access
      - HSA_OVERRIDE_GFX_VERSION=10.3.0
    volumes:
      - sd_webui_data:/data
      - sd_models:/models
    devices:
      - /dev/kfd
      - /dev/dri
    group_add:
      - video
      - render
    command: |
      bash -c "
        git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git /app &&
        cd /app &&
        ./webui.sh --listen --skip-torch-cuda-test
      "
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.sdwebui.rule=Host(`sd.${DOMAIN}`)"
      - "traefik.http.routers.sdwebui.entrypoints=websecure"
      - "traefik.http.routers.sdwebui.tls.certresolver=cloudflare"
      - "traefik.http.routers.sdwebui.middlewares=authentik@file"
      - "traefik.http.services.sdwebui.loadbalancer.server.port=7860"
```

**For ComfyUI (Advanced Workflows):**

```yaml
  comfyui:
    image: yanwk/comfyui-boot:rocm  # Community AMD image
    container_name: comfyui
    restart: unless-stopped
    networks:
      - homelab_network
    ports:
      - "8188:8188"
    environment:
      - TZ=${TZ}
      - HSA_OVERRIDE_GFX_VERSION=10.3.0
    volumes:
      - comfyui_data:/root
      - comfyui_models:/root/ComfyUI/models
    devices:
      - /dev/kfd
      - /dev/dri
    group_add:
      - video
      - render
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.comfyui.rule=Host(`comfy.${DOMAIN}`)"
      - "traefik.http.routers.comfyui.entrypoints=websecure"
      - "traefik.http.routers.comfyui.tls.certresolver=cloudflare"
      - "traefik.http.routers.comfyui.middlewares=authentik@file"
      - "traefik.http.services.comfyui.loadbalancer.server.port=8188"
```

---

## 📋 Service Deployment Plan

### Phase 1: Foundation (Day 1)

**Prerequisites:**
```bash
# 1. Install ROCm (if not already)
# For Ubuntu/Debian:
wget https://repo.radeon.com/amdgpu-install/latest/ubuntu/jammy/amdgpu-install_6.0.60000-1_all.deb
sudo dpkg -i amdgpu-install_6.0.60000-1_all.deb
sudo amdgpu-install --usecase=rocm

# 2. Verify GPU access
rocm-smi
# Should show RX 6800 XT

# 3. Install Docker (if not already)
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# 4. Add to homelab network
# Ensure gaming PC can reach 192.168.16.7 and 192.168.17.1
```

### Phase 2: Ollama AMD Deployment (Day 1)

```bash
# Create compose file
cat > /opt/homelab/gaming-pc-ai.yml << 'YAML'
# [Insert Ollama AMD config from above]
YAML

# Deploy
docker compose -f /opt/homelab/gaming-pc-ai.yml up -d ollama-amd

# Test
docker logs ollama-amd -f

# Pull large models (RTX 1080 can't handle)
docker exec ollama-amd ollama pull deepseek-coder:33b
docker exec ollama-amd ollama pull mixtral:8x7b-instruct-v0.1-q4_K_M
```

### Phase 3: Stable Diffusion (Day 2)

```bash
# Deploy SD WebUI
docker compose -f /opt/homelab/gaming-pc-ai.yml up -d stable-diffusion-webui

# Wait for model download (first run takes 10-15 min)
docker logs stable-diffusion -f

# Access: https://sd.${DOMAIN}
```

### Phase 4: ComfyUI (Day 3)

```bash
# Deploy ComfyUI
docker compose -f /opt/homelab/gaming-pc-ai.yml up -d comfyui

# Access: https://comfy.${DOMAIN}
```

### Phase 5: Integration with Homelab (Week 2)

**Open WebUI Multi-Backend:**
- Configure Open WebUI to use BOTH:
  - Ollama (RTX 1080): Small models (7B, 8B)
  - Ollama AMD (RX 6800 XT): Large models (33B, 70B)
- Users select model, request routes to appropriate backend

**n8n Workflows:**
- Image generation workflow: Trigger → ComfyUI/SD → Store in Outline
- Large model inference: Complex prompts → Ollama AMD (33B model)

---

## 🔧 Configuration Commands

### Get Missing Info (Run on Gaming PC)

```bash
# IP Address
echo "IP: $(hostname -I | awk '{print $1}')"

# Linux Distribution
cat /etc/os-release | grep -E "^NAME=|^VERSION="

# Docker Status
docker --version && systemctl is-active docker

# ROCm Status
rocm-smi 2>/dev/null || echo "ROCm not installed"

# Available Storage
df -h / /home | tail -n +2

# GPU Info
lspci | grep -i vga
lspci | grep -i amd

# Network connectivity to other hosts
ping -c 2 192.168.16.7 && echo "ThinkPad reachable"
ping -c 2 192.168.17.1 && echo "RTX1080 reachable"
```

**Send output back for finalization.**

---

## ⚡ Performance Comparison

| Workload | RTX 1080 (8GB) | RX 6800 XT (16GB) | Advantage |
|----------|----------------|-------------------|-----------|
| **Llama 3 8B** | ✅ Fast | ✅ Fast | Equal |
| **Llama 3 70B** | ❌ Won't fit | ✅ Possible (4-bit) | AMD |
| **Stable Diffusion 1.5** | ✅ ~2s/img | ✅ ~1.5s/img | AMD (faster) |
| **Stable Diffusion XL** | ⚠️ Slow (8GB limit) | ✅ Fast (16GB) | AMD |
| **ComfyUI Workflows** | ⚠️ Limited | ✅ Complex workflows | AMD |
| **Video Encoding (4K)** | ❌ No NVENC | ✅ VCE/VCN | AMD |
| **Power Consumption** | ~180W | ~300W | NVIDIA (efficient) |

**Verdict:** RX 6800 XT is **superior for large VRAM workloads** (LLMs 70B, SDXL, complex workflows)

---

## 🎮 Dual-Boot Strategy

### Linux (Homelab) Boot
- **Services:** All AI/compute workloads
- **Uptime:** 24/7 or on-demand
- **Access:** SSH from network

### Windows Boot (Gaming)
- **When:** Gaming sessions
- **Duration:** On-demand (evenings/weekends)
- **Homelab Impact:** Services unavailable during Windows boot

**Recommendation:** 
- **Default boot:** Linux (for homelab services)
- **On-demand:** Reboot to Windows for gaming
- **Automation:** Wake-on-LAN to power on remotely

---

## 📊 Resource Summary

**Gaming PC Contribution to Homelab:**

| Resource | Capacity | Usage (Estimated) | Remaining |
|----------|----------|-------------------|-----------|
| CPU | 24 threads | 8-12 threads (AI) | 12-16 threads |
| RAM | 32GB | 16-20GB (AI+Docker) | 12-16GB |
| GPU VRAM | 16GB | 12-14GB (SD+LLM) | 2-4GB |
| Storage | TBD | 100-200GB (models) | TBD |
| Network | 1 Gbps | 100-200 Mbps | 800+ Mbps |
| Power | 450W load | 300W avg | - |

---

## ✅ Next Actions Required

**From you (Gaming PC commands):**
1. Run configuration commands above
2. Provide:
   - IP address
   - Linux distribution
   - Docker status
   - Storage availability
   - 24/7 decision

**From me (after info received):**
1. Finalize Ansible inventory
2. Create AMD GPU Docker Compose stack
3. Generate deployment script
4. Configure Open WebUI multi-backend
5. Update n8n workflows for GPU services

---

**Status:** READY FOR INFO GATHERING  
**Estimated Setup Time:** 2-3 hours (after info provided)  
**Services to Deploy:** 4-6 GPU-accelerated containers

