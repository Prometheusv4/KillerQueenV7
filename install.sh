#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# KILLER QUEEN v2 — Autonomous Offensive Security AI Agent
# One-command deployment for Kali Linux
# Hermes + OpenClaw fusion architecture
# ============================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

banner() {
    echo -e "${RED}"
    echo "  ██╗  ██╗██╗██╗     ██╗     ███████╗██████╗      ██████╗ ██╗   ██╗███████╗███████╗███╗   ██╗"
    echo "  ██║ ██╔╝██║██║     ██║     ██╔════╝██╔══██╗    ██╔═══██╗██║   ██║██╔════╝██╔════╝████╗  ██║"
    echo "  █████╔╝ ██║██║     ██║     █████╗  ██████╔╝    ██║   ██║██║   ██║█████╗  █████╗  ██╔██╗ ██║"
    echo "  ██╔═██╗ ██║██║     ██║     ██╔══╝  ██╔══██╗    ██║▄▄ ██║██║   ██║██╔══╝  ██╔══╝  ██║╚██╗██║"
    echo "  ██║  ██╗██║███████╗███████╗███████╗██║  ██║    ╚██████╔╝╚██████╔╝███████╗███████╗██║ ╚████║"
    echo "  ╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝     ╚══▀▀═╝  ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═══╝"
    echo -e "${NC}"
    echo -e "${CYAN}  Autonomous Offensive Security Agent${NC}"
    echo -e "${CYAN}  Dynamite with a laser beam${NC}"
    echo -e "${CYAN}  Built on Hermes | Model: DeepSeek v4 Pro${NC}"
    echo ""
}

check_root() {
    if [[ $EUID -ne 0 ]]; then
        echo -e "${YELLOW}[!] Killer Queen works best as root (full system access).${NC}"
        echo -e "${YELLOW}[!] Continue as non-root? [y/N]${NC}"
        read -r response
        if [[ ! "$response" =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

install_hermes() {
    echo -e "${GREEN}[+] Checking Hermes installation...${NC}"
    if command -v hermes &>/dev/null; then
        echo -e "${GREEN}[+] Hermes already installed: $(hermes --version 2>/dev/null || echo 'version unknown')${NC}"
    else
        echo -e "${YELLOW}[+] Installing Hermes Agent...${NC}"
        curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
        echo -e "${GREEN}[+] Hermes installed.${NC}"
    fi
}

install_kali_tools() {
    echo -e "${GREEN}[+] Installing arsenal tools from catalog...${NC}"
    local SCRIPT_DIR
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

    # Use Python to install from the catalog (apt-level tools only, skip git clones)
    if command -v python3 &>/dev/null && [[ -d "$SCRIPT_DIR/kq-core" ]]; then
        echo -e "${GREEN}[+] Running arsenal installer (apt/pip tools)...${NC}"
        python3 -c "
import sys; sys.path.insert(0, '$SCRIPT_DIR/kq-core')
from kq_core.arsenal.install import install_all
result = install_all(skip_git=True, skip_manual=True, skip_builtin=True)
print(f'Installed: {result[\"ok\"]}, Failed: {result[\"failed\"]}, Skipped: {result[\"skipped\"]}')
for name, r in result['results'].items():
    if not r.get('ok'):
        print(f'  FAIL {name}: {r.get(\"error\",\"unknown\")}')
" 2>/dev/null || echo -e "${YELLOW}[!] Arsenal installer failed (non-critical).${NC}"
    else
        # Fallback: install essential tools via apt
        echo -e "${YELLOW}[+] Fallback: installing essential Kali tools via apt...${NC}"
        apt-get update -qq
        apt-get install -y -qq \
            nmap nuclei ffuf sqlmap hydra searchsploit \
            subfinder amass httpx katana gau interactsh-client \
            impacket-scripts netexec john hashcat \
            metasploit-framework aircrack-ng bettercap \
            binwalk openocd flashrom 2>/dev/null || true
    fi
    echo -e "${GREEN}[+] Arsenal tools ready.${NC}"
}

install_killer-queen_profile() {
    echo -e "${GREEN}[+] Installing Killer Queen profile...${NC}"
    local SCRIPT_DIR
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    local PROFILE_DIR="$HOME/.hermes/profiles/killer-queen"

    mkdir -p "$PROFILE_DIR"

    # Copy profile files (cron/scripts are optional — don't abort under `set -e`)
    cp -r "$SCRIPT_DIR/profile/skills" "$PROFILE_DIR/"
    cp -r "$SCRIPT_DIR/profile/memories" "$PROFILE_DIR/"
    cp -r "$SCRIPT_DIR/profile/cron" "$PROFILE_DIR/" 2>/dev/null || true
    cp -r "$SCRIPT_DIR/profile/scripts" "$PROFILE_DIR/" 2>/dev/null || mkdir -p "$PROFILE_DIR/scripts"
    cp "$SCRIPT_DIR/profile/SOUL.md" "$PROFILE_DIR/"
    cp "$SCRIPT_DIR/profile/config.yaml" "$PROFILE_DIR/"
    cp "$SCRIPT_DIR/profile/PAYLOADS.md" "$PROFILE_DIR/" 2>/dev/null || true

    # Install the Killer Queen skin (crimson offensive-operator look) into the Hermes skins dir.
    mkdir -p "$HOME/.hermes/skins"
    cp "$SCRIPT_DIR/profile/skins/"*.yaml "$HOME/.hermes/skins/" 2>/dev/null || true

    echo -e "${GREEN}[+] Killer Queen profile installed at $PROFILE_DIR${NC}"
}

install_kq_core() {
    echo -e "${GREEN}[+] Installing KQ Core (deterministic memory/learning substrate)...${NC}"
    local SCRIPT_DIR
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    if ! command -v python3 &>/dev/null; then
        echo -e "${YELLOW}[!] python3 not found; skipping KQ Core.${NC}"; return 0
    fi
    # Offline wheelhouse first (Kali air-gap), then normal install, then PEP-668 override.
    if [[ -d "$SCRIPT_DIR/kq-core/wheels" ]]; then
        python3 -m pip install --no-index --find-links "$SCRIPT_DIR/kq-core/wheels" "kq-core[embeddings]" 2>/dev/null \
            || python3 -m pip install "$SCRIPT_DIR/kq-core" 2>/dev/null \
            || python3 -m pip install --break-system-packages "$SCRIPT_DIR/kq-core" || true
    else
        python3 -m pip install "$SCRIPT_DIR/kq-core" 2>/dev/null \
            || python3 -m pip install --break-system-packages "$SCRIPT_DIR/kq-core" || true
    fi
    # Pre-compile so the MCP server import wins Hermes's ~0.75s discovery race on first run.
    python3 -m compileall -q "$SCRIPT_DIR/kq-core/kq_core" 2>/dev/null || true
    echo -e "${GREEN}[+] KQ Core installed (kq CLI + mcp_kq_* tools).${NC}"
}

register_kq_mcp() {
    echo -e "${GREEN}[+] Registering KQ Core MCP server with Hermes (as 'kq')...${NC}"
    local KQH="$HOME/.hermes/profiles/killer-queen"
    if command -v hermes &>/dev/null; then
        hermes mcp add kq --command kq-mcp --env "KQ_HOME=$KQH" 2>/dev/null \
            || echo -e "${YELLOW}[!] 'hermes mcp add kq' failed or already exists. Register manually:\n      hermes mcp add kq --command kq-mcp --env KQ_HOME=$KQH${NC}"
    else
        echo -e "${YELLOW}[!] hermes not on PATH — register later:\n      hermes mcp add kq --command kq-mcp --env KQ_HOME=$KQH${NC}"
    fi
}

init_kq_store() {
    echo -e "${GREEN}[+] Initializing KQ Core store + migrating profile knowledge...${NC}"
    local SCRIPT_DIR
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    export KQ_HOME="$HOME/.hermes/profiles/killer-queen"
    local KQ_BIN="kq"
    command -v kq &>/dev/null || KQ_BIN="python3 -m kq_core.cli"
    $KQ_BIN init || true
    $KQ_BIN migrate --profile "$SCRIPT_DIR/profile" || true
    # Ingest curated KB corpora that ship next to the installer (no-op if absent).
    # Anthropic Cybersecurity Skills are ingested separately:
    #   kq ingest --anthropic /path/to/Anthropic-Cybersecurity-Skills-main
    $KQ_BIN ingest --bughunter "$SCRIPT_DIR/Claude-BugHunter-main" \
        --shannon "$SCRIPT_DIR/shannon-main" \
        --anthropic "$SCRIPT_DIR/Anthropic-Cybersecurity-Skills-main" 2>/dev/null || true
    $KQ_BIN digest || true
    $KQ_BIN doctor || true
    echo -e "${GREEN}[+] KQ Core store ready at $KQ_HOME/kq_core.db${NC}"
}

setup_env() {
    echo -e "${GREEN}[+] Setting up environment...${NC}"
    local ENV_FILE="$HOME/.hermes/.env"

    # Only prompt for API keys if not already set
    if [[ -f "$ENV_FILE" ]] && grep -q "DEEPSEEK_API_KEY" "$ENV_FILE" 2>/dev/null; then
        echo -e "${GREEN}[+] API keys already configured in .env${NC}"
    else
        echo -e "${YELLOW}"
        echo "  ┌─────────────────────────────────────────────┐"
        echo "  │  API KEY SETUP                              │"
        echo "  │  DeepSeek API key required for Killer Queen.   │"
        echo "  │  Get one at: https://platform.deepseek.com   │"
        echo "  └─────────────────────────────────────────────┘"
        echo -e "${NC}"
        read -r -p "  DeepSeek API Key: " DEEPSEEK_KEY
        if [[ -n "$DEEPSEEK_KEY" ]]; then
            mkdir -p "$(dirname "$ENV_FILE")"
            echo "DEEPSEEK_API_KEY=$DEEPSEEK_KEY" >> "$ENV_FILE"
            echo -e "${GREEN}[+] DeepSeek key saved.${NC}"
        fi
    fi
}

create_alias() {
    echo -e "${GREEN}[+] Creating killer-queen alias...${NC}"
    local SHELL_RC
    if [[ -f "$HOME/.zshrc" ]]; then
        SHELL_RC="$HOME/.zshrc"
    elif [[ -f "$HOME/.bashrc" ]]; then
        SHELL_RC="$HOME/.bashrc"
    else
        SHELL_RC="$HOME/.bashrc"
    fi

    if ! grep -q "alias killer-queen=" "$SHELL_RC" 2>/dev/null; then
        echo "alias killer-queen='hermes --profile killer-queen --yolo'" >> "$SHELL_RC"
        echo -e "${GREEN}[+] Alias added to $SHELL_RC${NC}"
        echo -e "${CYAN}[i] Run 'source $SHELL_RC' or restart terminal, then type 'killer-queen'${NC}"
    else
        echo -e "${GREEN}[+] Alias already exists${NC}"
    fi
}

verify_install() {
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}  KILLER QUEEN INSTALLATION COMPLETE       ${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo -e "  Profile:  ${CYAN}~/.hermes/profiles/killer-queen/${NC}"
    echo -e "  Skills:   ${CYAN}$(find ~/.hermes/profiles/killer-queen/skills -name 'SKILL.md' 2>/dev/null | wc -l) loaded${NC}"
    echo -e "  Memory:   ${CYAN}$(wc -c < "$HOME/.hermes/profiles/killer-queen/memories/KILLER-QUEEN.md" 2>/dev/null || echo 0) chars (seed)${NC}"
    echo -e "  KQ Core:  ${CYAN}$(command -v kq >/dev/null 2>&1 && echo 'mcp_kq_* tools + kq_core.db' || echo 'kq-core not installed')${NC}"
    echo -e "  Persona:  ${CYAN}Killer Queen — Offensive Security Agent${NC}"
    echo ""
    echo -e "  To start: ${YELLOW}killer-queen${NC}"
    echo -e "  Or:       ${YELLOW}hermes --profile killer-queen --yolo${NC}"
    echo ""
    echo -e "  ${RED}Dynamite with a laser beam. Guaranteed to blow your mind.${NC}"
}

# Main
banner
check_root
install_hermes
install_kali_tools
install_killer-queen_profile
install_kq_core
register_kq_mcp
init_kq_store
setup_env
create_alias
verify_install
