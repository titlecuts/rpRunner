# rpRunner™

**Zero-touch CLI for RunPod GPU management**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

---

## What is rpRunner™?

rpRunner™ eliminates the friction of connecting to RunPod GPU instances. No more copy-pasting SSH commands or manually configuring connections.

```bash
# That's it. You're connected.
rpconnect abc123xyz
```

---

## Features

- **Zero-Touch Connection**: `rpconnect` queries RunPod API, establishes SSH, verifies health
- **Pod Lifecycle**: Start, stop, restart pods from CLI
- **Health Monitoring**: Automated health checks for running pods
- **Simple File Transfer**: Upload/download files via SFTP
- **SSH Config Management**: Automatic SSH config updates

---

## Installation

```bash
git clone https://github.com/titlecuts/rpRunner.git
cd rpRunner
pip install -r requirements.txt

# Configure
cp config.py.example config.py
# Edit config.py with your RUNPOD_API_KEY

# Install shortcuts (optional)
bash install_shortcuts.sh
source ~/.zshrc
```

---

## Quick Start

```bash
# Set your API key
export RUNPOD_API_KEY="your_key_here"

# List your pods
python3 rprunner.py pods

# Connect to a pod (auto-configures everything)
python3 rprunner.py connect <pod_id>

# Or use shortcut after install
rpconnect <pod_id>

# Check pod health
rpcheck

# Upload a file
rpupload ./myfile.png

# Download a file
rpdownload /workspace/output.png ./local_output.png
```

---

## Commands

| Command | Description |
|---------|-------------|
| `rpconnect <pod_id>` | Connect to pod, configure SSH, verify health |
| `rpp` or `pods` | List all your RunPod pods |
| `rpstart <pod_id>` | Start a stopped pod |
| `rpstop [pod_id]` | Stop a running pod (uses current if not specified) |
| `rpcheck` | Health check current pod |
| `rpupload <file>` | Upload file to pod's /workspace |
| `rpdownload <remote> <local>` | Download file from pod |
| `rpstatus` | Show current pod configuration |
| `rpkeys` | Verify API key setup |

---

## Configuration

### Option 1: Environment Variable (Recommended)

```bash
export RUNPOD_API_KEY="your_runpod_api_key"
export SSH_KEY_PATH="~/.ssh/id_ed25519"  # optional, this is default
```

### Option 2: Config File

```bash
cp config.py.example config.py
# Edit config.py with your settings
```

### Option 3: Secrets File

```bash
mkdir -p ~/rpagent/Secrets
echo '{"api_key": "your_key_here"}' > ~/rpagent/Secrets/Runpod_API_Key.json
```

---

## Requirements

- Python 3.9+
- RunPod account with API access
- SSH key configured (`~/.ssh/id_ed25519` by default)

---

## How rpconnect Works

rpRunner's `rpconnect` command automates the entire connection process:

1. **API Query**: Fetches pod details from RunPod GraphQL API
2. **SSH Config**: Extracts connection info (host, port)
3. **Connection Test**: Establishes and verifies SSH connection
4. **Health Check**: Runs nvidia-smi to verify GPU
5. **State Save**: Saves connection to `POD_STATE.json` for future commands

All in 2-3 seconds.

---

## Add-ons

rpRunner™ is the foundation. Additional modules available for advanced workflows:

### rpComfy (Private)
ComfyUI workflow automation with:
- Full pipeline execution (upload → queue → monitor → download)
- Reference image management
- Organized output folders (by project/scene/date)
- SaveImage path rewriting
- Workflow shortcuts (`rpscene`, `rpchar`, `rptest`)

### rpAPI (Private)
Multi-provider AI orchestration:
- 13+ AI services with unified interface
- Video (Fal.ai, Runway, LTX)
- Audio (ElevenLabs, Azure Speech)
- Images (FLUX, DALL-E, Imagen)
- Music generation

### rpPipe (Private)
Production tracking and management:
- Airtable integration
- Shot list management
- Generation logging
- Error detection & solutions database

### rpStore (Private)
Hybrid storage for 98% cost reduction:
- 3-tier storage (hot/warm/cold)
- GCS sync automation
- Model tiering scripts
- Cost analytics

**Contact for add-on licensing**: [titlecuts@gmail.com](mailto:titlecuts@gmail.com)

---

## Examples

### Daily Workflow

```bash
# Morning: Start pod
rpstart abc123xyz
sleep 60  # Wait for boot

# Connect
rpconnect abc123xyz
# ✓ SSH connection successful!
# ✓ GPU: NVIDIA RTX A6000 48GB

# Upload work files
rpupload ./project_files.zip

# Do your work...
# (ComfyUI, training, rendering, etc.)

# Evening: Stop pod to save costs
rpstop
```

### Multi-Pod Management

```bash
# List all pods
rpp
# Pod ID       Name            Status    GPU
# abc123xyz    comfy-prod      RUNNING   RTX A6000
# def456uvw    training-01     STOPPED   H100

# Switch between pods
rpconnect abc123xyz
rpcheck  # Verify health

rpconnect def456uvw
rpcheck  # Verify health
```

### Quick Health Check

```bash
rpcheck
# 🎮 Checking GPU...
# ✓ NVIDIA RTX A6000, 2048 MiB / 49140 MiB
# 💾 Checking disk space...
# ✓ /dev/sda 100G  23G   78G  23% /workspace
# ✅ Health check complete
```

---

## Why rpRunner?

Built from real production frustration:

**Before rpRunner:**
1. Go to RunPod dashboard
2. Find pod
3. Copy SSH command
4. Paste in terminal
5. Test connection
6. Forget which pod you're on
7. Repeat daily

**With rpRunner:**
```bash
rpconnect abc123xyz
```

Done.

---

## Security

- API keys via environment variables or separate config files
- SSH keys managed by your system
- No secrets in repository
- `POD_STATE.json` automatically gitignored

---

## Contributing

Contributions welcome! This is the free, open-source foundation.

- Submit PRs for bug fixes
- Open issues for feature requests
- Keep it focused on pod management
- Commercial add-ons available separately

---

## Roadmap

**Core (Free/Open Source):**
- ✅ Zero-touch connection
- ✅ Pod lifecycle management
- ✅ Health monitoring
- ✅ Basic file transfer
- 🔄 Pod templates/presets
- 🔄 Multi-SSH key support
- 🔄 Connection pooling

**Add-ons (Private/Commercial):**
- ComfyUI automation (rpComfy)
- Provider integrations (rpAPI)
- Production tracking (rpPipe)
- Storage optimization (rpStore)

---

## License

MIT License - see [LICENSE](LICENSE)

---

## FAQ

**Q: Is this officially affiliated with RunPod?**  
A: No, this is a community tool that uses RunPod's public API.

**Q: What about the add-ons?**  
A: rpRunner (core) is free and open-source. The add-ons (rpComfy, rpAPI, rpPipe, rpStore) are private commercial modules built for production workflows. Contact for licensing.

**Q: Can I build my own add-ons?**  
A: Absolutely! rpRunner is MIT licensed. Build whatever you want on top of it.

**Q: Does this work with other GPU cloud providers?**  
A: Currently RunPod only. The core architecture could be adapted for other providers.

**Q: Why split into separate repos?**  
A: The core pod management is universally useful. The add-ons contain proprietary workflows and integrations developed for specific production needs.

---

## Acknowledgments

Built by [Allan Title](https://titlecuts.com) for real production work at TitleCuts.

Inspired by frustration with manual RunPod workflows and a desire for zero-friction GPU access.

---

## Support

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/titlecuts/rpRunner/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/titlecuts/rpRunner/discussions)
- 📧 **Commercial Inquiries**: titlecuts@gmail.com

---

*Built for real production work, not demos.*

