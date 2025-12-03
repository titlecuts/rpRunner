# rpRunner™ - AI Video Production Pipeline

**Production-grade CLI orchestrating AI video, image, and audio generation.**

[![Status](https://img.shields.io/badge/status-production--ready-brightgreen)](https://github.com)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Built by **Dr_M4ng0 @ TitleCuts** for documentary and commercial video production.

---

## 📦 What's In This Repo

**This is the open-source core** - a portfolio showcase demonstrating the architecture and methodology behind a production AI video pipeline.

| This Repo (Open Source) | Full Production Suite (Private) |
|-------------------------|--------------------------------|
| ✅ Architecture overview | 🔒 15+ video model integrations |
| ✅ AI Co-Pilot Methodology | 🔒 Voice/SFX/Music generation |
| ✅ Basic RunPod connection example | 🔒 259 production templates |
| ✅ Framework documentation | 🔒 Batch processing with resume |
| | 🔒 Lipsync pipelines |
| | 🔒 Script parsing & shot generation |
| | 🔒 Project/scene/character context |

**Want the full rig?** [Contact me](#-work-with-me)

---

## 🎬 Full Suite Capabilities

*The following showcases what the complete rpRunner production suite can do:*

### Video Generation (15+ Models)
- **Cloud APIs**: Veo 3.1, Kling 2.5 Pro, Luma Ray 2, Minimax, LTX 2.0, Hunyuan
- **Local/RunPod**: Wan 2.2 (14B & 1.3B), AnimateDiff (via ComfyUI)
- **Techniques**: Image-to-Video, Text-to-Video, First/Last Frame interpolation, 4K upscaling, Lipsync

### Image Generation (10+ Models)
- **Cloud APIs**: Flux Dev/Pro/Ultra (Fal.ai)
- **ComfyUI**: SDXL, NBPro (Gemini 3 Pro - 2K/4K), Qwen (text rendering), Kontext (context-aware)
- **Techniques**: ControlNet, Inpainting, LoRA, Character consistency (VACE)

### Audio Generation
- **Voice Synthesis**: 30+ voices + custom cloning (ElevenLabs)
- **Sound Effects**: Text-to-SFX with duration control
- **Music Creation**: AI-generated scores and stems
- **Advanced Control**: Emotion tags, SSML prosody, presets

### Production Context System
- **Projects**: Isolated workspaces with their own assets and history
- **Scenes**: Organize shots by narrative structure
- **Characters**: Consistent character definitions across generations
- **Shots**: Track and iterate on specific shots
- **Script Parsing**: Import Fountain screenplays, auto-generate shot lists

### 259 ComfyUI Templates
- **ControlNet** (18 templates): Pose, depth, canny edge, lineart, segmentation
- **Camera Control**: Pan, zoom, orbit, dolly movements
- **Character Consistency**: VACE (video-aware character embedding)
- **Lipsync**: Audio-driven facial animation
- **Upscaling**: 4x UltraSharp, Real-ESRGAN
- **Style Transfer**: LoRA injection, style mixing
- **Masking**: SAM (Segment Anything), GroundingDINO
- **Face Restoration**: GFPGAN, CodeFormer

---

## ⚡ Example Commands (Full Suite)

```bash
# Video from image
rpvideo i2v -i photo.png -p "cinematic camera pan" -d 6 --model veo-3.1

# Video from ComfyUI workflow
rpqueue wan22_i2v.json -p "forest scene, misty morning" --wait --download

# Voice with emotion
rpsound voice gen "Help me! Someone please help!" -v kayla --emotion crying

# Sound effect
rpsound sfx gen "thunder clap in distance, reverberating" -d 3.0

# Music generation
rpsound music gen "tense documentary underscore, minimal piano"

# Parse screenplay and generate shot list
rpscript parse screenplay.fountain --output shots.json

# Batch upscale videos
rpbatch run "rpvideo upscale -i {input}" -i ./720p/*.mp4 --parallel

# Project-aware generation (all outputs organized automatically)
rpproject switch harper_bell
rpvideo i2v -i scene.png -p "slow push in" --scene "forest_search" --shot 12
```

---

## 🔧 Two Execution Paths

The full suite provides **two powerful ways** to generate content:

### 1. Cloud APIs (`rpvideo`, `rpsound`)
- ✅ **Instant access** - No GPU required
- ✅ **Pay-per-use** - Via Fal.ai, ElevenLabs
- ✅ **Managed infrastructure** - Zero setup
- 🎯 **Best for**: Quick iteration, experimentation, production at scale

### 2. ComfyUI on RunPod (`rpqueue`, `rpq`)
- ✅ **Full control** - Custom workflows, LoRA support
- ✅ **GPU rental** - $0.50-2.00/hour (cheaper for bulk)
- ✅ **259 templates included** - Searchable, categorized
- 🎯 **Best for**: Advanced workflows, batch processing, custom models

---

## 🧠 AI Co-Pilot Methodology

One of the most valuable parts of this project is **how it was built**.

I developed rpRunner using a two-agent AI workflow:
- **Claude** - Strategic planning, architecture decisions, documentation
- **Cursor** - Implementation, debugging, code generation

This methodology is documented in [docs/CO_PILOT_METHODOLOGY.md](docs/CO_PILOT_METHODOLOGY.md) and demonstrates how a creative professional (not a developer) can build production-grade tools using AI assistance.

**Key insight**: The co-pilot approach isn't just how I built it—it's a feature of how I work. I can apply this same methodology to build pipelines for your projects.

---

## 🚀 Getting Started (Open Source Core)

This repo includes a basic example to get you connected to RunPod:

```bash
# Clone the repo
git clone https://github.com/titlecuts/rpRunner-core.git
cd rpRunner-core

# Set your RunPod API key
export RUNPOD_API_KEY="your_key_here"

# Run the example
pip install runpod requests
python examples/basic_pod_connect.py
```

This shows the foundation. The full suite builds 50+ commands on top of this.

---

## 🤝 Work With Me

I'm available for:

| Service | Description |
|---------|-------------|
| **Production Consulting** | Bring my pipeline to your project |
| **Custom Pipeline Builds** | I'll build YOUR AI video infrastructure |
| **Training & Workshops** | Teach your team the methodology |

📧 **Email**: [allan@titlecuts.com](mailto:allan@titlecuts.com)

---

## 📚 Documentation

- **[CO_PILOT_METHODOLOGY.md](docs/CO_PILOT_METHODOLOGY.md)** - The Claude + Cursor workflow
- **[examples/basic_pod_connect.py](examples/basic_pod_connect.py)** - Starter code

---

## 🙏 Credits

**Built by:** Dr_M4ng0 @ TitleCuts

**The full suite is powered by:**
- [RunPod](https://runpod.io) - GPU infrastructure
- [Fal.ai](https://fal.ai) - Video generation APIs
- [ElevenLabs](https://elevenlabs.io) - Voice synthesis
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI) - Workflow engine

**Models include:**
- Veo 3.1 (Google DeepMind)
- Kling 2.5 (Kuaishou)
- Wan 2.2 (Alibaba)
- Flux (Black Forest Labs)
- And many more...

---

## 📜 License

MIT License - See [LICENSE](LICENSE)

---

**rpRunner™ - From AI chaos to production pipeline. 🎬✨**
