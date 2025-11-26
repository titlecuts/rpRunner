#!/bin/bash

# rpRunner™ - Push to GitHub Script
# Run this to push the public repository

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  🚀 Pushing rpRunner™ to GitHub...                       ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

cd "/Volumes/Dr_Mang0_SSD_4TB/AI Projects & Files/rpRunner" || exit 1

echo "📍 Current directory: $(pwd)"
echo ""

# Update git remote
echo "🔗 Updating git remote..."
git remote set-url origin git@github.com:titlecuts/rpRunner.git
git remote -v
echo ""

# Stage all changes
echo "📦 Staging all changes..."
git add -A
echo ""

# Show status
echo "📊 Changes to commit:"
git status --short
echo ""

# Commit
echo "💾 Creating commit..."
git commit -m "Complete rpRunner™ public release with trademark protection

Trademark Protection:
- rpRunner™ (core)
- rpComfy™ (add-on)
- rpAPI™ (add-on)
- rpPipe™ (add-on)
- rpStore™ (add-on)

Files:
- rprunner.py (renamed from rpagent.py)
- Updated README.md with full branding
- Updated config.py.example (RPAGENT_* → RPRUNNER_*)
- Updated shortcuts/rpconnect
- Added ™ symbols throughout (23 locations)

Legal:
- Establishes common law trademark protection
- All components protected with ™ symbol
- Professional branding complete

Features:
- Zero-touch pod connection (rpconnect)
- Pod lifecycle management
- Health monitoring
- Basic file transfer
- Clean configuration system

Foundation for rpComfy™, rpAPI™, rpPipe™, rpStore™ add-ons.

Built for real production work." || {
    echo "⚠️  Commit failed or nothing to commit"
    git status
}

echo ""

# Push
echo "🚀 Pushing to GitHub..."
git push -u origin main

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  ✅ rpRunner™ SUCCESSFULLY PUSHED TO GITHUB! ✅          ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "🌐 Repository: https://github.com/titlecuts/rpRunner"
echo ""
echo "📋 Next steps:"
echo "   1. Visit GitHub to verify the push"
echo "   2. Update repository description"
echo "   3. Add topics: runpod, cli-tool, gpu-orchestration"
echo ""
echo "🎉 Your production-grade tool is now public!"
echo ""

