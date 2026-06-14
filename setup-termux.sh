#!/data/data/com.termux/files/usr/bin/bash
# Arabic Code Auditor Pro - Termux Setup
# المطور: الجنرال

echo "=================================="
echo "  Arabic Code Auditor Pro"
echo "  منصة فحص الأكواد العربية"
echo "=================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Update packages
echo -e "${BLUE}[*] Updating packages...${NC}"
pkg update -y && pkg upgrade -y

# Install Python
echo -e "${BLUE}[*] Installing Python...${NC}"
pkg install -y python python-pip

# Install Node.js (for frontend)
echo -e "${BLUE}[*] Installing Node.js...${NC}"
pkg install -y nodejs

# Install Git
echo -e "${BLUE}[*] Installing Git...${NC}"
pkg install -y git

# Install PostgreSQL (optional)
echo -e "${BLUE}[*] Installing PostgreSQL...${NC}"
pkg install -y postgresql

# Install Redis (optional)
echo -e "${BLUE}[*] Installing Redis...${NC}"
pkg install -y redis

# Create project directory
PROJECT_DIR="$HOME/arabic-code-auditor-pro"
echo -e "${BLUE}[*] Creating project directory: $PROJECT_DIR${NC}"
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

# Install Python dependencies
echo -e "${BLUE}[*] Installing Python dependencies...${NC}"
pip install fastapi uvicorn pydantic sqlalchemy python-multipart aiofiles httpx python-dotenv

# Install analysis tools
echo -e "${BLUE}[*] Installing code analysis tools...${NC}"
pip install ruff pylint mypy bandit radon black

# Create directory structure
echo -e "${BLUE}[*] Creating directory structure...${NC}"
mkdir -p backend/src/{core,analyzers/{python,javascript,php},api,cli,database,security,ai,fixers,scanners,reports,plugins}
mkdir -p frontend/src/{app,components,dashboard,editor,reports,scans,projects,settings,plugins,lib,hooks,types,styles}
mkdir -p reports plugins uploads

# Create .env file
echo -e "${BLUE}[*] Creating environment file...${NC}"
cat > .env << 'EOF'
DATABASE_URL=sqlite:///aca.db
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key-here
DEBUG=true
API_HOST=0.0.0.0
API_PORT=8000
EOF

# Create run script
echo -e "${BLUE}[*] Creating run scripts...${NC}"
cat > run-api.sh << 'EOF'
#!/bin/bash
cd backend
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
EOF
chmod +x run-api.sh

cat > run-cli.sh << 'EOF'
#!/bin/bash
cd backend
python -m src.cli.main "$@"
EOF
chmod +x run-cli.sh

cat > run-frontend.sh << 'EOF'
#!/bin/bash
cd frontend
npm run dev
EOF
chmod +x run-frontend.sh

# Create aca alias
echo -e "${BLUE}[*] Creating aca command alias...${NC}"
mkdir -p $HOME/.local/bin
cat > $HOME/.local/bin/aca << 'EOF'
#!/bin/bash
cd $HOME/arabic-code-auditor-pro/backend
python -m src.cli.main "$@"
EOF
chmod +x $HOME/.local/bin/aca

# Add to PATH if not already there
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> $HOME/.bashrc
    export PATH="$HOME/.local/bin:$PATH"
fi

# Create systemd-like service script
cat > run-daemon.sh << 'EOF'
#!/bin/bash
# Run API in background
nohup ./run-api.sh > api.log 2>&1 &
echo "API started on http://localhost:8000"
echo "API docs: http://localhost:8000/docs"
EOF
chmod +x run-daemon.sh

echo ""
echo -e "${GREEN}==================================${NC}"
echo -e "${GREEN}  Installation Complete!${NC}"
echo -e "${GREEN}==================================${NC}"
echo ""
echo -e "${YELLOW}Usage:${NC}"
echo "  aca scan <file.py>        - Scan a file"
echo "  aca fix <file.py>         - Auto-fix issues"
echo "  aca security <file.py>    - Security scan"
echo "  aca report <project>      - Generate report"
echo ""
echo -e "${YELLOW}Run API:${NC}"
echo "  ./run-api.sh              - Start API server"
echo "  ./run-daemon.sh           - Start in background"
echo ""
echo -e "${YELLOW}API Endpoints:${NC}"
echo "  http://localhost:8000     - API Root"
echo "  http://localhost:8000/docs - API Documentation"
echo ""
echo -e "${BLUE}Developer: الجنرال${NC}"
echo ""
