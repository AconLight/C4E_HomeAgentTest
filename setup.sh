#!/usr/bin/env bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check system requirements
check_requirement() {
    local command=$1
    local package=$2
    
    if ! command -v $command &> /dev/null; then
        echo -e "${RED}Error: $package is required but not found.${NC}"
        echo -e "${YELLOW}Please install $package using your system's package manager before running this script.${NC}"
        exit 1
    fi
}

echo -e "${GREEN}Starting HomeAgent Test environment setup...${NC}\n"

# Check if script is run with sudo
if [ "$EUID" -eq 0 ]; then
    echo -e "${RED}Please do not run this script as root or with sudo${NC}"
    exit 1
fi

# Check Python3 installation
echo -e "${YELLOW}Checking Python installation...${NC}"
check_requirement "python3" "python3"

# Check Python version
REQUIRED_PYTHON_VERSION="3.10"
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
if [ "$(echo -e "$PYTHON_VERSION\n$REQUIRED_PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_PYTHON_VERSION" ]; then
    echo -e "${RED}Python version $REQUIRED_PYTHON_VERSION or higher is required. Found version $PYTHON_VERSION${NC}"
    echo -e "${YELLOW}Please upgrade Python using your system's package manager.${NC}"
    exit 1
fi

echo -e "${GREEN}Found Python $PYTHON_VERSION${NC}"

# Check pip3 installation
echo -e "${YELLOW}Checking pip installation...${NC}"
check_requirement "pip3" "python3-pip"

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
if [ "$(echo -e "$PYTHON_VERSION\n$REQUIRED_PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_PYTHON_VERSION" ]; then
    echo -e "${RED}Python version $REQUIRED_PYTHON_VERSION or higher is required. Found version $PYTHON_VERSION${NC}"
    exit 1
fi

echo -e "${GREEN}Python $PYTHON_VERSION found${NC}"

# Check venv module
echo -e "${YELLOW}Checking venv module...${NC}"
if ! python3 -c "import venv" &> /dev/null; then
    echo -e "${RED}Python venv module is required but not found.${NC}"
    echo -e "${YELLOW}Please install python3-venv using your system's package manager.${NC}"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "\n${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to create virtual environment${NC}"
        exit 1
    fi
else
    echo -e "\n${YELLOW}Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo -e "\n${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to activate virtual environment${NC}"
    exit 1
fi

# Upgrade pip in virtual environment
echo -e "\n${YELLOW}Upgrading pip...${NC}"
./venv/bin/python -m pip install --upgrade pip

# Install wheel first (helps with binary packages)
echo -e "\n${YELLOW}Installing wheel...${NC}"
./venv/bin/pip install wheel

# Install requirements
echo -e "\n${YELLOW}Installing requirements...${NC}"
./venv/bin/pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to install requirements${NC}"
    exit 1
fi

# Install development dependencies
echo -e "\n${YELLOW}Installing development dependencies...${NC}"
./venv/bin/pip install pytest pytest-cov black isort mypy

# Ensure .env file exists
if [ ! -f .env ]; then
    touch .env
fi

# Check for Hugging Face token in .env (must be set and non-empty)
HF_TOKEN_IN_ENV=$(grep '^HUGGINGFACE_HUB_TOKEN=' .env | cut -d'=' -f2-)
if [ -z "$HF_TOKEN_IN_ENV" ]; then
    echo "HUGGINGFACE_HUB_TOKEN is not set in your .env file."
    read -p "Please enter your Hugging Face token: " HF_TOKEN_INPUT
    if [ -z "$HF_TOKEN_INPUT" ]; then
        echo "Error: Hugging Face token is required. Exiting."
        exit 1
    fi
    # Remove any existing (possibly empty) HUGGINGFACE_HUB_TOKEN lines from .env
    grep -v '^HUGGINGFACE_HUB_TOKEN=' .env > .env.tmp && mv .env.tmp .env
    echo "HUGGINGFACE_HUB_TOKEN=$HF_TOKEN_INPUT" >> .env
    echo "Token saved to .env."
fi

echo -e "\n${GREEN}Setup completed successfully!${NC}"
echo -e "\n${YELLOW}To activate the virtual environment, run:${NC}"
echo -e "source venv/bin/activate"

echo -e "\n${YELLOW}To run tests:${NC}"
echo -e "source venv/bin/activate && python -m pytest"
echo -e "# or for more detailed output:"
echo -e "source venv/bin/activate && python -m pytest -v"
echo -e "# or for coverage report:"
echo -e "source venv/bin/activate && python -m pytest --cov=core"

echo -e "\n${YELLOW}To format code:${NC}"
echo -e "source venv/bin/activate && black ."
echo -e "source venv/bin/activate && isort ."

echo -e "\n${GREEN}Happy coding!${NC}"
