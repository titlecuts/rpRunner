#!/bin/bash
# Install shortcuts for Runpod Agent

echo "🚀 Installing Runpod Agent shortcuts..."

# Detect shell
SHELL_RC=""
if [ -f "$HOME/.zshrc" ]; then
    SHELL_RC="$HOME/.zshrc"
elif [ -f "$HOME/.bashrc" ]; then
    SHELL_RC="$HOME/.bashrc"
else
    echo "❌ Could not find .zshrc or .bashrc"
    exit 1
fi

echo "📝 Adding shortcuts to $SHELL_RC"

# Backup shell rc
cp "$SHELL_RC" "$SHELL_RC.backup.$(date +%Y%m%d_%H%M%S)"

# Remove old shortcuts if they exist
sed -i.tmp '/# Runpod Agent Shortcuts/,/# End Runpod Agent Shortcuts/d' "$SHELL_RC"
rm -f "$SHELL_RC.tmp"

# Add new shortcuts
cat >> "$SHELL_RC" << 'EOF'

# Runpod Agent Shortcuts
export RUNPOD_AGENT_DIR="/Volumes/Dr_Mang0_SSD_4TB/AI Projects & Files/Cursor Agent Work/Runpod Agent"

# Quick command to run runpod agent
runpod() {
    python3 "$RUNPOD_AGENT_DIR/runpod_agent.py" "$@"
}

# Aliases for ALL commands
# Core
alias rp='runpod'
alias rpi='runpod interactive'
alias rphelp='runpod --help'

# Pod Management
alias rpc='runpod create'
alias rpp='runpod pods'
alias rpstart='runpod start'
alias rpstop='runpod stop'
alias rprestart='runpod restart'
alias rpterm='runpod terminate'
alias rpset='runpod set'

# Monitoring & Health
alias rph='runpod health --pod-id $RUNPOD_CURRENT_POD'
alias rpl='runpod logs --pod-id $RUNPOD_CURRENT_POD'
alias rpmon='runpod monitor --pod-id $RUNPOD_CURRENT_POD'
alias rpinv='runpod inventory --pod-id $RUNPOD_CURRENT_POD'

# ComfyUI Operations
alias rpcomfy='runpod comfy --pod-id $RUNPOD_CURRENT_POD'
alias rpqueue='runpod queue --pod-id $RUNPOD_CURRENT_POD'
alias rprun='runpod run --pod-id $RUNPOD_CURRENT_POD'
alias rpdownload='runpod download --pod-id $RUNPOD_CURRENT_POD'
alias rpint='runpod interrupt --pod-id $RUNPOD_CURRENT_POD'
alias rpclear='runpod clear-queue --pod-id $RUNPOD_CURRENT_POD'

# GPU & Info
alias rpg='runpod gpus'
alias rpgpus='runpod gpus'

# Workflow Templating (Phase 1)
alias rptemplates='runpod templates'
alias rpinject='runpod inject'
alias rpvalidate='runpod validate'
alias rpfields='runpod templates --show-fields'

# AI Providers (Phase 2a)
alias rpgenerate='runpod generate'
alias rpproviders='runpod providers'
alias rpvoices='runpod voices'
alias rpkeys='runpod check-keys'

# GCS Backup & Restore (Phase 2B.2)
alias rpbackup='runpod backup'
alias rprestore='runpod restore'
alias rpbackups='runpod backup --list'

# Reference Management (Phase 2C)
alias rpref='runpod ref'
alias rpupload='runpod upload'

# Airtable Production Tracking (Phase 2C)
alias rpat='runpod airtable'
alias rpshots='runpod shots'
alias rptrack='runpod track'
alias rpscenes='runpod scenes'

# Utilities
alias rpfix='python3 "$RUNPOD_AGENT_DIR/runpod_agent.py" fix --pod-id $RUNPOD_CURRENT_POD'
alias rpman='python3 "$RUNPOD_AGENT_DIR/runpod_agent.py" manager --pod-id $RUNPOD_CURRENT_POD'
alias cdrunpod='cd "$RUNPOD_AGENT_DIR"'

# Quick actions (with prompts)
rpnew() {
    echo "🚀 Quick Pod Creation"
    echo "Available regions: us, ca, europe, asia"
    read -p "GPU [NVIDIA RTX 4090]: " gpu
    gpu=${gpu:-"NVIDIA RTX 4090"}
    read -p "Region [us]: " region
    region=${region:-"us"}
    runpod create --gpu "$gpu" --region "$region"
}

rpwatch() {
    echo "👀 Watching ComfyUI queue (Ctrl+C to stop)"
    while true; do
        clear
        runpod comfy --pod-id $RUNPOD_CURRENT_POD
        sleep 5
    done
}

# Reload shell (easy to remember!)
reload() {
    echo "🔄 Reloading shell configuration..."
    source ~/.zshrc
    echo "✅ Shell reloaded!"
}
# End Runpod Agent Shortcuts
EOF

echo "✅ Shortcuts installed!"
echo ""
echo "📋 Pod Management:"
echo "  rpc                - Create new pod"
echo "  rpp                - List all pods"
echo "  rpstart            - Start stopped pod"
echo "  rpstop             - Stop running pod"
echo "  rprestart          - Restart pod/service"
echo "  rpterm             - Terminate pod"
echo "  rpset              - Set current pod"
echo ""
echo "📊 Monitoring & Health:"
echo "  rph                - Check health"
echo "  rpl                - Analyze logs"
echo "  rpmon              - Enable monitoring"
echo "  rpinv              - Update inventory"
echo "  rpwatch            - Watch queue (live)"
echo ""
echo "🎨 ComfyUI Operations:"
echo "  rpcomfy            - ComfyUI status"
echo "  rpqueue <file>     - Queue workflow (auto-organized outputs)"
echo "  rprun <file>       - Complete pipeline: upload images, queue, wait, download"
echo "  rpdownload         - Bulk download recent completions"
echo "  rpint              - Interrupt execution"
echo "  rpclear            - Clear queue"
echo ""
echo "✨ Workflow Templating (Phase 1):"
echo "  rptemplates        - List workflow templates"
echo "  rpfields <file>    - Analyze templateable fields"
echo "  rpinject <file>    - Inject variables into template"
echo "  rpvalidate <file>  - Validate template syntax"
echo ""
echo "🎨 AI Providers (Phase 2a):"
echo "  rpgenerate         - Generate with AI providers"
echo "  rpproviders        - List available providers"
echo "  rpvoices           - List ElevenLabs voices"
echo ""
echo "💾 Backup & Restore (Phase 2B.2):"
echo "  rpbackup <path>    - Backup directory to GCS"
echo "  rpbackup --all     - Backup all generated_outputs/"
echo "  rpbackup --today   - Backup today's outputs"
echo "  rpbackups          - List GCS backups"
echo "  rprestore <path>   - Restore from GCS"
echo ""
echo "🖼️  Reference Management (Phase 2C):"
echo "  rpref list         - List available references"
echo "  rpref add          - Add reference image"
echo "  rpref show <name>  - Show reference variants"
echo "  rpupload           - Upload reference to pod"
echo ""
echo "📊 Production Tracking (Phase 2C):"
echo "  rpshots            - View shot list (Airtable)"
echo "  rptrack            - Track shot progress"
echo "  rpscenes           - View scenes"
echo "  rpat setup         - Configure Airtable"
echo ""
echo "💡 Utilities:"
echo "  rpi                - Interactive mode"
echo "  rpg                - Show GPU options"
echo "  rpnew              - Quick pod creation"
echo "  rphelp             - Show help"
echo "  cdrunpod           - Jump to directory"
echo "  reload             - Reload shell config (source ~/.zshrc)"
echo ""
echo "🔄 To activate, run: reload"
echo "   Or: source $SHELL_RC"
echo "   Or close and reopen your terminal"

