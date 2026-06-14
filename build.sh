#!/usr/bin/env bash
echo "=================================="
echo "  Arabic Code Auditor Pro"
echo "  Build System"
echo "=================================="

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

cd "$(dirname "$0")"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python3 not found!${NC}"
    exit 1
fi

echo -e "${BLUE}[*] Installing build dependencies...${NC}"
pip install pyinstaller cython

echo -e "${BLUE}[*] Step 1: Obfuscating core files...${NC}"
python3 obfuscate.py

echo -e "${BLUE}[*] Step 2: Building Cython extensions...${NC}"
python3 setup_cython.py build_ext --inplace

echo -e "${BLUE}[*] Step 3: Building executable...${NC}"
pyinstaller aca.spec --clean --noconfirm

echo -e "${BLUE}[*] Step 4: Copying assets...${NC}"
mkdir -p dist/aca/assets
cp -r src/analyzers dist/aca/assets/
cp -r src/api dist/aca/assets/
cp -r src/database dist/aca/assets/

echo -e "${BLUE}[*] Step 5: Creating distribution package...${NC}"
cd dist
zip -r arabic-code-auditor-pro-v1.0.0.zip aca/

echo ""
echo -e "${GREEN}==================================${NC}"
echo -e "${GREEN}  Build Complete!${NC}"
echo -e "${GREEN}==================================${NC}"
echo ""
echo "Output:"
echo "  dist/aca/ - Executable"
echo "  dist/arabic-code-auditor-pro-v1.0.0.zip - Distribution"
