#!/bin/bash
# Fantasy Baseball Decision Log Setup Script

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Fantasy Baseball Decision Log Setup${NC}"
echo "This script will set up the project for development."

# Check for required tools
echo -e "\n${YELLOW}Checking prerequisites...${NC}"

# Check Python
if command -v python3 &>/dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo -e "✅ Python $PYTHON_VERSION installed"
else
    echo -e "${RED}❌ Python 3.9+ is required but not found${NC}"
    echo "Please install Python 3.9 or higher: https://www.python.org/downloads/"
    exit 1
fi

# Check Node.js
if command -v node &>/dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "✅ Node.js $NODE_VERSION installed"
else
    echo -e "${RED}❌ Node.js 18+ is required but not found${NC}"
    echo "Please install Node.js 18 or higher: https://nodejs.org/"
    exit 1
fi

# Check Bun
if command -v bun &>/dev/null; then
    BUN_VERSION=$(bun --version)
    echo -e "✅ Bun $BUN_VERSION installed"
else
    echo -e "${RED}❌ Bun is required but not found${NC}"
    echo "Please install Bun: https://bun.sh/"
    exit 1
fi

# Check uv
if command -v uv &>/dev/null; then
    UV_VERSION=$(uv --version)
    echo -e "✅ uv $UV_VERSION installed"
else
    echo -e "${RED}❌ uv is required but not found${NC}"
    echo "Please install uv: https://github.com/astral-sh/uv"
    exit 1
fi

# Check Docker (optional)
if command -v docker &>/dev/null; then
    DOCKER_VERSION=$(docker --version | cut -d' ' -f3 | tr -d ',')
    echo -e "✅ Docker $DOCKER_VERSION installed"

    if command -v docker-compose &>/dev/null; then
        DOCKER_COMPOSE_VERSION=$(docker-compose --version | cut -d' ' -f3 | tr -d ',')
        echo -e "✅ Docker Compose $DOCKER_COMPOSE_VERSION installed"
    else
        echo -e "${YELLOW}⚠️ Docker Compose not found (optional)${NC}"
    fi
else
    echo -e "${YELLOW}⚠️ Docker not found (optional)${NC}"
fi

# Create .env file if it doesn't exist
echo -e "\n${YELLOW}Setting up environment...${NC}"
if [ ! -f .env ]; then
    cp .env.example .env
    echo -e "✅ Created .env file from .env.example"
    echo -e "${YELLOW}⚠️ Please edit .env file with your Yahoo API credentials${NC}"
else
    echo -e "✅ .env file already exists"
fi

# Set up backend
echo -e "\n${YELLOW}Setting up backend...${NC}"
cd backend || exit 1
uv venv
if [ "$(uname)" == "Darwin" ] || [ "$(uname)" == "Linux" ]; then
    source .venv/bin/activate
else
    # Windows
    .venv\\Scripts\\activate
fi
uv pip install -r requirements.txt
echo -e "✅ Backend dependencies installed"

# Set up frontend
echo -e "\n${YELLOW}Setting up frontend...${NC}"
cd ../frontend || exit 1
bun install
echo -e "✅ Frontend dependencies installed"

# Set up database directories
echo -e "\n${YELLOW}Setting up data directories...${NC}"
cd ..
mkdir -p data/json
echo -e "✅ Data directories created"

echo -e "\n${GREEN}Setup complete!${NC}"
echo -e "To start the backend: cd backend && python run.py --reload"
echo -e "To start the frontend: cd frontend && bun run dev"
echo -e "To start PostgreSQL (optional): cd docker && docker-compose up -d"
echo -e "\nHappy fantasy baseball managing! 🎯⚾"
