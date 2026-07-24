#!/bin/bash
# H9 Eye - Wireless Surveillance Dashboard - Easy Pop!_OS One-Click Deploy Script
# Author: Jules & Hayden

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}[+] Initializing HayOS H9 Eye Deployment on Pop!_OS / Debian...${NC}"

# 1. Install System Dependencies
echo -e "${BLUE}[+] Checking system package dependencies...${NC}"
if ! command -v pip3 &> /dev/null || ! python3 -c "import venv" &> /dev/null; then
    echo -e "${YELLOW}[!] Missing Python3 development tools. Installing python3-pip and python3-venv...${NC}"
    sudo apt update
    sudo apt install -y python3-pip python3-venv xdg-utils
else
    echo -e "${GREEN}[✓] System packages are already installed.${NC}"
fi

# 2. Configure Virtual Environment
if [ ! -d ".venv" ]; then
    echo -e "${BLUE}[+] Creating isolated Python virtual environment...${NC}"
    python3 -m venv .venv
fi

echo -e "${BLUE}[+] Activating virtual environment...${NC}"
source .venv/bin/activate

# 3. Install Python Library Dependencies
echo -e "${BLUE}[+] Upgrading pip and installing requirements...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

# 4. Resolve Port Collisions (Port 8080)
echo -e "${BLUE}[+] Checking port 8080 status...${NC}"
PORT_OCCUPIED=$(lsof -t -i :8080 || true)
if [ ! -z "$PORT_OCCUPIED" ]; then
    echo -e "${YELLOW}[!] Port 8080 is currently in use by PID(s): $PORT_OCCUPIED. Terminating old process...${NC}"
    kill -9 $PORT_OCCUPIED || true
    sleep 1
fi

# 5. Launch Server
echo -e "${BLUE}[+] Starting H9 Eye Server on port 8080...${NC}"
nohup python3 app-env.py > flask.log 2>&1 &

echo -e "${GREEN}[✓] H9 Eye Server has been launched in the background!${NC}"
echo -e "${BLUE}[+] Logs are being streamed to 'flask.log'.${NC}"

# 6. Auto-Open Browser Dashboard
sleep 2
echo -e "${BLUE}[+] Launching Web Interface...${NC}"
if command -v xdg-open &> /dev/null; then
    xdg-open "http://127.0.0.1:8080/" &
else
    echo -e "${YELLOW}[!] xdg-open is not available. Please navigate to http://127.0.0.1:8080/ manually in your browser.${NC}"
fi

echo -e "${GREEN}[✓] Deployment complete! Enjoy your wireless surveillance panel.${NC}"
