# rpRunner™ - AI Video Production Pipeline

**Production-grade CLI orchestrating AI video, image, and audio generation.**

[![Status](https://img.shields.io/badge/status-production--ready-brightgreen)](https://github.com)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Built by **Allan @ TitleCuts** for documentary and commercial video production.

---

## 🎬 Capabilities at a Glance

### Video Generation (15+ Models)
- **Cloud APIs**: Veo 3.1, Kling 2.5 Pro, Luma Ray 2, Minimax, LTX 2.0, Hunyuan
- **Local/RunPod**: Wan 2.2 (14B & 1.3B), AnimateDiff (via ComfyUI)
- **Techniques**: Image-to-Video, Text-to-Video, First/Last Frame interpolation, 4K upscaling

### Image Generation (10+ Models)
- **Cloud APIs**: Flux Dev/Pro/Ultra (Fal.ai)
- **ComfyUI**: SDXL, NBPro (Gemini 3 Pro - 2K/4K), Qwen (text rendering), Kontext (context-aware)
- **Techniques**: ControlNet, Inpainting, LoRA, Character consistency (VACE)

### Audio Generation
- **Voice Synthesis**: 30+ voices + custom cloning (ElevenLabs)
- **Sound Effects**: Text-to-SFX with duration control
- **Advanced Control**: Emotion tags, SSML prosody, presets

### 259 ComfyUI Templates
- **ControlNet** (18 templates): Pose, depth, canny edge, lineart, segmentation
- **Camera Control**: Pan, zoom, orbit, dolly movements
- **Character Consistency**: VACE (video-aware character embedding)
- **Upscaling**: 4x UltraSharp, Real-ESRGAN, RealESRGAN_x4plus
- **Style Transfer**: LoRA injection, style mixing
- **Masking**: SAM (Segment Anything), GroundingDINO
- **Face Restoration**: GFPGAN, CodeFormer

---

## ⚡ Quick Examples

```bash
# Video from image (cloud API)
rpvideo i2v -i photo.png -p "cinematic camera pan" -d 6 --model veo-3.1

# Video from ComfyUI workflow (local GPU)
rpqueue wan22_i2v.json -p "forest scene, misty morning" --wait --download

# Voice with emotion
rpsound voice gen "Help me! Someone please help!" -v kayla --emotion crying

# Sound effect
rpsound sfx gen "thunder clap in distance, reverberating" -d 3.0

# Batch upscale videos
rpbatch run "rpvideo upscale -i {input}" -i ./720p/*.mp4 --parallel
```

---

## 🔧 Two Execution Paths

rpRunner provides **two powerful ways** to generate content:

### 1. Cloud APIs (`rpvideo`, `rpsound`)
- ✅ **Instant access** - No GPU required
- ✅ **Pay-per-use** - Via Fal.ai, ElevenLabs
- ✅ **Managed infrastructure** - Zero setup
- 🎯 **Best for**: Quick iteration, experimentation, production at scale

**Video Models (Fal.ai):**
- **Veo 3.1** - Google's flagship (I2V, T2V, 4-8s, with audio)
- **Kling 2.5 Pro** - Best first/last frame interpolation
- **Luma Ray 2** - Natural motion, great for landscapes
- **Minimax** - Advanced camera control
- **LTX 2.0** - Budget-friendly 4K with audio
- **Hunyuan** - Excellent lighting and atmosphere

**Image Models:**
- **Flux Dev/Pro/Ultra** - State-of-the-art prompt adherence

**Audio:**
- **ElevenLabs** - Professional voice synthesis + SFX

### 2. ComfyUI on RunPod (`rpqueue`, `rpq`)
- ✅ **Full control** - Custom workflows, LoRA support
- ✅ **GPU rental** - $0.50-2.00/hour (cheaper for bulk)
- ✅ **259 templates included** - Searchable, categorized
- 🎯 **Best for**: Advanced workflows, batch processing, custom models

**Video Models (ComfyUI):**
- **Wan 2.2** (14B & 1.3B) - Respects input frames closely, great FLF
- **AnimateDiff** - Motion modules, extensive style control

**Image Models:**
- **NBPro (Gemini 3 Pro)** - 2K/4K, character consistency
- **Flux** (various) - LoRA support, ControlNet integration
- **SDXL** - Wide ecosystem, inpainting, style transfer
- **Qwen** - Text rendering, multilingual
- **Kontext** - Context-aware generation

**Template Techniques:**
- ControlNet (pose, depth, canny, lineart)
- VACE (video-aware character consistency)
- Camera control (pan, zoom, orbit)
- 4x UltraSharp upscaling
- Face restoration (GFPGAN, CodeFormer)
- Inpainting/Outpainting
- Style transfer via LoRA

---

## 🚀 Getting Started

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/rpRunner.git
cd rpRunner

# 2. Install dependencies
pip install -r requirements.txt

# 3. Install shell shortcuts
./shortcuts/install.sh
source ~/.zshrc  # or ~/.bashrc

# 4. Configure environment
cp .env.example .env
nano .env  # Add your API keys
```

### First Video Generation

```bash
# Set up a project
rpproject new my_project --activate

# Generate video from image (cloud)
rpvideo i2v -i photo.png -p "slow camera zoom" -d 6 --model veo-3.1-fast

# Or use ComfyUI workflow (local GPU)
rpqueue wan22_i2v.json -p "cinematic scene" --wait --download
```

### Explore Templates

```bash
# View library stats
rpt stats
# → 259 templates (199 official, 53 community, 7 wiki)

# Search for specific technique
rpt search "upscale"
rpt search "controlnet pose"
rpt search "wan video"

# List by category
rpt list --category video
rpt list --source official
```

---

## 📋 Command Reference

### Video Generation (Cloud API)
```bash
# Image to video
rpvideo i2v -i image.png -p "motion description" -d 6 --model veo-3.1

# Text to video (select models)
rpvideo t2v -p "scene description" -d 5 --model kling-2.1-master

# First/last frame interpolation
rpvideo flf -f start.png -l end.png -p "smooth transition" --model kling-2.5-pro

# Video upscaling
rpvideo upscale -i 720p.mp4 --preset 1080p

# List all models
rpvideo models
```

### ComfyUI Workflow Execution
```bash
# Queue workflow with prompt injection
rpqueue workflow.json -p "your prompt here"

# Set seed for reproducibility
rpqueue workflow.json --seed 123456

# Multiple variables
rpqueue workflow.json --var width=1024 --var height=1024

# Wait for completion and auto-download
rpqueue workflow.json -p "prompt" --wait --download

# Short alias
rpq workflow.json -p "prompt" -w -d
```

### Audio Generation
```bash
# Voice synthesis
rpsound voice gen "Dialogue text" -v vivian --emotion neutral

# Voice with emotion
rpsound voice gen "Help me!" -v kayla --emotion crying

# Sound effects
rpsound sfx gen "footsteps on gravel" -d 2.5

# Voice cloning
rpsound voice clone "Character Name" -s sample1.mp3 -s sample2.mp3
```

### Template Library
```bash
# Search templates
rpt search "keyword"
rpt search "upscale 4k"
rpt search "controlnet"

# Browse by category
rpt list --category video
rpt list --category image
rpt list --category enhancement

# View statistics
rpt stats

# Sync official templates
rpt sync
```

### Batch Processing
```bash
# Basic batch
rpbatch run "rpvideo upscale -i {input}" -i ./videos/*.mp4

# With output directory
rpbatch run "cmd {input} {output}" -i ./in/ -o ./out/

# Parallel execution (3 workers)
rpbatch run "cmd {input}" -i ./files/ --parallel -j 3

# Resume interrupted batch
rpbatch run "cmd {input}" -i ./files/ --resume

# Dry run (preview without executing)
rpbatch run "cmd {input}" -i ./files/ --dry-run
```

### Project Management
```bash
# Create new project
rpproject new my_film --title "My Film" --activate

# Switch projects
rpproject switch harper_bell

# View current project
rpproject current

# List all projects
rpproject list
```

### Pod Management (RunPod)
```bash
# Create new pod
rpc

# List pods
rpp

# Set active pod
rpset --pod-id abc123

# Start/stop pod
rpstart
rpstop

# Health check
rph

# ComfyUI status
rpcomfy
```

### Production Pipeline
```bash
# View generation history
rphistory list
rphistory list --count 20
rphistory search "prompt text"

# Auto-download completed outputs
rpwatch

# Voice notifications (macOS)
rpwatch --notify voice

# Extract shot list from screenplay
rpscript shots script.fountain
rpscript scenes script.fountain
```

---

## 🎯 Who This Is For

### Video Producers
- Automate AI shot generation at scale
- Rapid creative iteration (10 sec vs 5 min)
- Batch process hundreds of files with resume

### Documentary Makers
- Consistent character pipelines (VACE)
- Voice cloning for narration
- Scene organization and tracking

### VFX Artists
- Batch upscaling (720p → 4K)
- ControlNet workflows (pose, depth, canny)
- Style transfer and face restoration

### Studios & Agencies
- Scalable production infrastructure
- Multi-project management
- Complete reproducibility (metadata logging)
- Cost-effective GPU rental + cloud APIs

---

## 🏗️ Architecture

```
rpRunner/
├── rprunner.py              # Main CLI entry point
├── cli/                     # Command modules
│   ├── video_commands.py    # rpvideo (Fal.ai API)
│   ├── sound_commands.py    # rpsound (ElevenLabs)
│   ├── batch_commands.py    # rpbatch (universal batch)
│   ├── template_commands.py # rptemplates/rpt
│   ├── project_commands.py  # rpproject
│   └── ...
├── core/                    # Core infrastructure
│   ├── batch_runner.py      # Universal batch engine
│   ├── project_context.py   # Project-aware paths
│   ├── generation_log.py    # Metadata logging
│   └── ...
├── comfy/                   # ComfyUI integration
│   ├── workflow_manager.py  # Prompt/seed/API key injection
│   ├── api_client.py        # ComfyUI REST API
│   └── ...
├── providers/               # AI service integrations
│   ├── falai_provider.py    # Video (Veo, Kling, Luma, etc.)
│   ├── elevenlabs_provider.py # Voice + SFX
│   ├── runpod_client.py     # GPU management
│   └── ...
├── template_library/        # 259 ComfyUI templates
│   ├── official/           # ComfyUI official (199)
│   ├── community/          # Community (53)
│   └── wiki/               # Documentation (7)
├── projects/                # User projects
│   ├── example/            # Template project
│   └── */                  # Your projects
├── shortcuts/               # Shell shortcuts
│   └── install.sh
└── docs/                    # Documentation
    ├── CAPABILITIES.md      # Full model reference
    ├── GETTING_STARTED.md   # Quick start
    └── ...
```

---

## 🎨 Video Model Comparison

### Cloud API Models (via Fal.ai)

| Model | Type | Duration | Quality | Speed | Cost | Best For |
|-------|------|----------|---------|-------|------|----------|
| **Veo 3.1** | I2V, T2V | 4/6/8s | ⭐⭐⭐⭐⭐ | Slow | $$$ | Highest quality, audio output |
| **Veo 3.1 Fast** | I2V, T2V | 4/6/8s | ⭐⭐⭐⭐ | Fast | $$ | Production speed + quality |
| **Kling 2.5 Pro** | I2V, T2V, FLF | 5-10s | ⭐⭐⭐⭐⭐ | Medium | $$$ | Best FLF, cinematic |
| **Kling 2.1 Master** | I2V, T2V | 5-10s | ⭐⭐⭐⭐ | Medium | $$ | Cinematic motion |
| **Luma Ray 2** | I2V, T2V | 5s | ⭐⭐⭐⭐ | Fast | $ | Natural motion, landscapes |
| **Minimax** | I2V, T2V | 5-10s | ⭐⭐⭐ | Medium | $$ | Camera control |
| **LTX 2.0** | I2V, T2V | 6-10s | ⭐⭐⭐ | Fast | $ | Budget 4K with audio |
| **Hunyuan** | T2V | 5s | ⭐⭐⭐ | Fast | $ | Good lighting |

### ComfyUI Models (on RunPod)

| Model | Type | VRAM | Quality | Best For |
|-------|------|------|---------|----------|
| **Wan 2.2 (14B)** | I2V, FLF | 24GB | ⭐⭐⭐⭐ | Respects input frames closely |
| **Wan 2.2 (1.3B)** | I2V, FLF | 12GB | ⭐⭐⭐ | Faster, lower VRAM |
| **AnimateDiff** | I2V | 12GB+ | ⭐⭐⭐ | Motion modules, style control |

**Note:** Wan 2.2 is **ComfyUI-only** (not available via API). Use `rpqueue` to run Wan workflows.

---

## 🎵 Audio Capabilities

### Voice Synthesis (ElevenLabs)

**Available Voices:**
- **Vivian Veo** - Documentary narrator (custom clone)
- **Kayla 911** - Young Latina, emotional range (custom clone)
- **911 Dispatch** - Professional dispatcher (custom clone)
- **30+ Built-in Voices** - Various accents, ages, tones

**Emotion Tags:**
- `neutral`, `excited`, `whispers`, `crying`, `angry`, `sad`, `terrified`, `hopeful`

**Advanced Control:**
- **Stability** (0-1): Voice consistency
- **Similarity** (0-1): How closely to match reference
- **Style** (0-1): Exaggeration level
- **Speed** (0.25-4.0): Speech rate
- **SSML**: Fine-grained prosody control

### Sound Effects

Text-to-sound effect generation with duration control:
- Ambience (forest, city, ocean)
- Impacts (door slam, glass break)
- Transitions (whoosh, swell, sting)
- Tech (phone static, keyboard)
- Atmospheric (suspense, magic)

---

## 📊 Performance & Time Savings

### Batch Processing Features
- ✅ **Resume Support** - Restart without re-processing completed items
- ✅ **Error Isolation** - One failure doesn't stop the batch
- ✅ **Parallel Execution** - Process multiple items simultaneously
- ✅ **Progress Tracking** - Real-time status with rich terminal output

### Time Savings (Per Day)

| Task | Before rpRunner | After rpRunner | Savings |
|------|----------------|----------------|---------|
| Prompt iteration | 4-9 min | 10 sec | **95%** |
| Image swapping | 10-15 min | 15 sec | **98%** |
| File organization | 10 min | Automatic | **100%** |
| Batch generation | 50-100 min | 10-20 min | **80%** |
| Searching templates | 15-30 min | 30 sec | **97%** |

**Annual Savings:** 479 hours ≈ **12 work weeks**

---

## 🎬 Real-World Use Cases

### Rapid Creative Iteration
```bash
# Test 5 different prompts instantly
rpqueue workflow.json --prompt-file prompts.txt --variants 5

# Adjust seed for variation
rpqueue workflow.json -p "portrait" --seed 42
```

### Character Consistency (Documentary)
```bash
# Define character once
# projects/my_doc/characters.yaml:
#   jane: "Middle-aged woman, grey hair, blue eyes"

# Use across all shots
rpvideo i2v -i scene01.png -p "walks through door" -c jane
rpvideo i2v -i scene05.png -p "sits at table" -c jane
```

### Batch Upscaling
```bash
# Upscale entire project
rpbatch run "rpvideo upscale -i {input} --preset 1080p" \
  -i projects/my_film/generated_outputs/video/*.mp4 \
  --parallel -j 3 --resume
```

### Automated Production Workflow
```bash
# 1. Start watchdog
rpwatch --notify voice

# 2. Queue multiple workflows (other terminal)
rpq shot01.json -p "..." --wait
rpq shot02.json -p "..." --wait
rpq shot03.json -p "..." --wait

# 3. Walk away ☕
# → Outputs auto-download
# → Auto-organize by project/scene
# → Mac says "Render complete"
```

---

## 🔒 Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Required for RunPod GPU management
RUNPOD_API_KEY=your_key_here

# Optional - Enable specific features
FAL_KEY=your_fal_key              # Video generation (Veo, Kling, etc.)
ELEVENLABS_API_KEY=your_key       # Voice synthesis + SFX
GEMINI_API_KEY=your_key            # NBPro image generation (Gemini 3 Pro)
OPENAI_API_KEY=your_key            # (If using OpenAI models)
ANTHROPIC_API_KEY=your_key         # (If using Claude models)

# Google Cloud Storage (optional)
GCS_CREDENTIALS_FILE=credentials.json
GCS_BUCKET_NAME=your_bucket

# Pod defaults
DEFAULT_POD_TYPE=NVIDIA_RTX_A5000
DEFAULT_GPU_COUNT=1
```

### Project Configuration

Each project has its own `project.yaml`:

```yaml
name: my_film
title: My Film Project
description: A short film about...

defaults:
  video:
    model: veo-3.1-fast
    duration: 6
    aspect_ratio: 16:9
  image:
    model: flux-pro
    resolution: 1024x1024

characters:
  protagonist:
    description: "30-year-old detective, weathered face, trench coat"
    refs:
      - assets/protagonist_01.png
      - assets/protagonist_02.png

paths:
  working_dir: ./projects/my_film
  output_dir: ./projects/my_film/generated_outputs
```

---

## 📚 Documentation

- **[CAPABILITIES.md](docs/CAPABILITIES.md)** - Complete model/technique reference
- **[GETTING_STARTED.md](docs/GETTING_STARTED.md)** - Step-by-step tutorials
- **[CUSTOMIZATION.md](docs/CUSTOMIZATION.md)** - Advanced configuration

---

## 📦 About This Repository

**This is the open-source showcase of rpRunner** - demonstrating the architecture and methodology behind a production AI video pipeline.

### What's Here (Open Source)

| Included | Description |
|----------|-------------|
| 📖 **This README** | Full capability reference |
| 🧠 **AI Co-Pilot Methodology** | How I built this with Claude + Cursor |
| 🔧 **Starter Example** | Basic RunPod connection to get you going |

### The Full Production Suite

Everything shown above - the **15 video models**, **voice synthesis**, **259 templates**, **batch processing**, and the **"it just works" polish** - lives in my private production rig.

**This includes:**
- 🎬 `rpvideo` - Video generation across 15+ models (Veo, Kling, Luma, Minimax, LTX, Hunyuan)
- 🎤 `rpsound` - Voice synthesis, SFX generation, voice cloning (ElevenLabs)
- ⚡ `rpbatch` - Production batch processing with resume support
- 📚 259 battle-tested ComfyUI templates
- 🎯 Character consistency pipelines
- 🔄 First/Last Frame interpolation
- 📈 4K upscaling workflows

### Work With Me

I'm available for:
- **Production consulting** - Bring my pipeline to your project
- **Custom pipeline builds** - I'll build YOUR AI video infrastructure  
- **Training & workshops** - Teach your team the methodology

📧 **[allan@titlecuts.com](mailto:allan@titlecuts.com)**

---

## 🤝 Contributing

rpRunner is a **personal production tool** built for real-world use, but contributions are welcome for:

- Bug fixes
- Performance improvements
- Documentation
- New provider integrations

See `CONTRIBUTING.md` for guidelines.

---

## 📜 License

MIT License - See `LICENSE` file

---

## 🙏 Credits

**Built by:** Allan @ TitleCuts

**Powered by:**
- [RunPod](https://runpod.io) - GPU infrastructure
- [Fal.ai](https://fal.ai) - Video generation APIs
- [ElevenLabs](https://elevenlabs.io) - Voice synthesis
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI) - Workflow engine

**Models:**
- Veo 3.1 (Google DeepMind)
- Kling 2.5 (Kuaishou)
- Wan 2.2 (ISTUdio)
- Flux (Black Forest Labs)
- NBPro (Gemini 3 Pro)

---

## 💬 Contact

- **GitHub Issues** - Bug reports and feature requests
- **Email** - allan@titlecuts.com
- **Twitter** - @titlecuts

---

**Status**: 🟢 Production Ready  
**Version**: 4.2  
**Last Updated**: December 3, 2025

---

**rpRunner™ - From AI chaos to production pipeline. 🎬✨**
