#!/usr/bin/env bash
# Arabic Code Auditor Pro - One-Line Installer
# المطور: الجنرال
# التثبيت: curl -sL https://raw.githubusercontent.com/GENERAL/arabic-code-auditor-pro/main/install.sh | bash

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'
BOLD='\033[1m'

# Banner
print_banner() {
    echo ""
    echo -e "${CYAN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║                                                              ║${NC}"
    echo -e "${CYAN}║${NC}     ${BOLD}Arabic Code Auditor Pro${NC}                                 ${CYAN}║${NC}"
    echo -e "${CYAN}║${NC}     ${YELLOW}منصة فحص الأكواد العربية${NC}                                ${CYAN}║${NC}"
    echo -e "${CYAN}║                                                              ║${NC}"
    echo -e "${CYAN}║${NC}     ${GREEN}المطور: الجنرال${NC}                                         ${CYAN}║${NC}"
    echo -e "${CYAN}║                                                              ║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

# Detect OS
detect_os() {
    if [[ "$OSTYPE" == "linux-android"* ]]; then
        echo "termux"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "mac"
    else
        echo "unknown"
    fi
}

# Install for Termux
install_termux() {
    echo -e "${BLUE}[*] Detected Termux/Android${NC}"

    echo -e "${BLUE}[*] Updating packages...${NC}"
    pkg update -y &>/dev/null

    echo -e "${BLUE}[*] Installing Python...${NC}"
    pkg install -y python python-pip git &>/dev/null

    echo -e "${BLUE}[*] Installing Node.js...${NC}"
    pkg install -y nodejs &>/dev/null

    INSTALL_DIR="$HOME/arabic-code-auditor-pro"
}

# Install for Linux
install_linux() {
    echo -e "${BLUE}[*] Detected Linux${NC}"

    echo -e "${BLUE}[*] Updating packages...${NC}"
    sudo apt-get update -y &>/dev/null || true

    echo -e "${BLUE}[*] Installing Python...${NC}"
    sudo apt-get install -y python3 python3-pip git &>/dev/null || true

    echo -e "${BLUE}[*] Installing Node.js...${NC}"
    sudo apt-get install -y nodejs npm &>/dev/null || true

    INSTALL_DIR="$HOME/arabic-code-auditor-pro"
}

# Install for Mac
install_mac() {
    echo -e "${BLUE}[*] Detected macOS${NC}"

    if ! command -v brew &>/dev/null; then
        echo -e "${YELLOW}[!] Homebrew not found. Installing...${NC}"
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi

    echo -e "${BLUE}[*] Installing Python...${NC}"
    brew install python3 git &>/dev/null || true

    echo -e "${BLUE}[*] Installing Node.js...${NC}"
    brew install node &>/dev/null || true

    INSTALL_DIR="$HOME/arabic-code-auditor-pro"
}

# Download and install
download_install() {
    echo -e "${BLUE}[*] Downloading Arabic Code Auditor Pro...${NC}"

    REPO_URL="https://github.com/GENERAL/arabic-code-auditor-pro"

    if command -v git &>/dev/null; then
        # Clone with git
        if [ -d "$INSTALL_DIR" ]; then
            echo -e "${YELLOW}[!] Directory exists. Updating...${NC}"
            rm -rf "$INSTALL_DIR"
        fi
        git clone --depth 1 "$REPO_URL.git" "$INSTALL_DIR" &>/dev/null
    else
        # Download ZIP
        echo -e "${BLUE}[*] Downloading ZIP...${NC}"
        curl -sL "$REPO_URL/archive/refs/heads/main.zip" -o /tmp/aca.zip
        unzip -q /tmp/aca.zip -d /tmp/
        mv /tmp/arabic-code-auditor-pro-main "$INSTALL_DIR"
        rm /tmp/aca.zip
    fi

    echo -e "${GREEN}[✓] Downloaded to $INSTALL_DIR${NC}"
}

# Install Python dependencies
install_python_deps() {
    echo -e "${BLUE}[*] Installing Python dependencies...${NC}"
    cd "$INSTALL_DIR/backend"
    pip install -q -r requirements.txt
    echo -e "${GREEN}[✓] Python dependencies installed${NC}"
}

# Install analysis tools
install_tools() {
    echo -e "${BLUE}[*] Installing code analysis tools...${NC}"
    pip install -q ruff pylint mypy bandit radon black
    echo -e "${GREEN}[✓] Analysis tools installed${NC}"
}

# Install Frontend dependencies
install_frontend() {
    echo -e "${BLUE}[*] Installing Frontend dependencies...${NC}"
    cd "$INSTALL_DIR/frontend"
    npm install &>/dev/null || echo -e "${YELLOW}[!] Frontend install skipped${NC}"
}

# Create shortcuts
create_shortcuts() {
    echo -e "${BLUE}[*] Creating shortcuts...${NC}"

    # Create aca command
    mkdir -p "$HOME/.local/bin"

    cat > "$HOME/.local/bin/aca" << 'EOF'
#!/bin/bash
cd $HOME/arabic-code-auditor-pro/backend
python3 -m src.cli.main "$@"
EOF
    chmod +x "$HOME/.local/bin/aca"

    # Create aca-api command
    cat > "$HOME/.local/bin/aca-api" << 'EOF'
#!/bin/bash
cd $HOME/arabic-code-auditor-pro/backend
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 "$@"
EOF
    chmod +x "$HOME/.local/bin/aca-api"

    # Create aca-frontend command
    cat > "$HOME/.local/bin/aca-frontend" << 'EOF'
#!/bin/bash
cd $HOME/arabic-code-auditor-pro/frontend
npm run dev
EOF
    chmod +x "$HOME/.local/bin/aca-frontend"

    # Add to PATH if not exists
    if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
        export PATH="$HOME/.local/bin:$PATH"
    fi

    echo -e "${GREEN}[✓] Shortcuts created${NC}"
}

# Main installation
main() {
    print_banner

    OS=$(detect_os)
    echo -e "${BLUE}[*] Detected OS: $OS${NC}"

    case $OS in
        termux)
            install_termux
            ;;
        linux)
            install_linux
            ;;
        mac)
            install_mac
            ;;
        *)
            echo -e "${RED}[!] Unsupported OS: $OS${NC}"
            exit 1
            ;;
    esac

    download_install
    install_python_deps
    install_tools
    install_frontend
    create_shortcuts

    echo ""
    echo -e "${GREEN}══════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}  Installation Complete!${NC}"
    echo -e "${GREEN}══════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${CYAN}Usage:${NC}"
    echo "  aca scan <file.py>          - Scan a file"
    echo "  aca security <file.py>      - Security scan"
    echo "  aca fix <file.py>           - Auto-fix issues"
    echo "  aca report <project>        - Generate report"
    echo ""
    echo -e "${CYAN}API:${NC}"
    echo "  aca-api                     - Start API server"
    echo "  aca-frontend                - Start Frontend"
    echo ""
    echo -e "${CYAN}Examples:${NC}"
    echo "  aca scan app.py"
    echo "  aca security app.py"
    echo "  aca fix app.py --apply"
    echo ""
    echo -e "${YELLOW}Note: Restart your terminal or run: source ~/.bashrc${NC}"
    echo ""
}

main "$@"
