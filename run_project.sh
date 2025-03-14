#!/bin/bash

# Water Quality Dynamics in Malaysia - Project Runner Script
# This script automates the workflow from data analysis to serving the dashboard

# Color codes for prettier output
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
RED="\033[0;31m"
BLUE="\033[0;34m"
NC="\033[0m" # No Color

# Function to check if a command is available
check_command() {
    if ! command -v "$1" &> /dev/null; then
        echo -e "${RED}Error: $1 is not installed.${NC}"
        echo -e "Please install $1 before running this script."
        if [ "$1" = "python" ] || [ "$1" = "python3" ]; then
            echo -e "Visit ${BLUE}https://www.python.org/downloads/${NC} to download Python."
        elif [ "$1" = "pip" ] || [ "$1" = "pip3" ]; then
            echo -e "Pip should be installed with Python. If not, visit ${BLUE}https://pip.pypa.io/en/stable/installation/${NC}"
        fi
        return 1
    fi
    return 0
}

# Function to check Python dependencies
check_python_dependencies() {
    echo -e "${BLUE}Checking Python dependencies...${NC}"
    
    # Check if requirements.txt exists, if not create one
    if [ ! -f "requirements.txt" ]; then
        echo "pandas>=1.3.0" > requirements.txt
        echo "matplotlib>=3.4.0" >> requirements.txt
        echo "seaborn>=0.11.0" >> requirements.txt
        echo "openpyxl>=3.0.0" >> requirements.txt
        echo "numpy>=1.20.0" >> requirements.txt
        echo "scikit-learn>=0.24.0" >> requirements.txt
        echo -e "${YELLOW}Created requirements.txt file${NC}"
    fi
    
    # Install required packages
    echo -e "${BLUE}Installing required Python packages...${NC}"
    if [ "$(uname)" == "Darwin" ]; then
        # macOS
        pip3 install -r requirements.txt || {
            echo -e "${RED}Failed to install Python dependencies.${NC}"
            return 1
        }
    else
        # Linux and others
        pip install -r requirements.txt || {
            echo -e "${RED}Failed to install Python dependencies.${NC}"
            return 1
        }
    fi
    
    echo -e "${GREEN}Python dependencies installed successfully.${NC}"
    return 0
}

# Function to run the water quality analysis script
run_analysis() {
    echo -e "${BLUE}Running water quality analysis script...${NC}"
    
    if [ -f "water_quality_analysis.py" ]; then
        if [ "$(uname)" == "Darwin" ]; then
            # macOS
            python3 water_quality_analysis.py || {
                echo -e "${RED}Error running analysis script.${NC}"
                return 1
            }
        else
            # Linux and others
            python water_quality_analysis.py || {
                echo -e "${RED}Error running analysis script.${NC}"
                return 1
            }
        fi
        echo -e "${GREEN}Analysis completed successfully.${NC}"
        return 0
    else
        echo -e "${RED}Error: water_quality_analysis.py not found.${NC}"
        return 1
    fi
}

# Function to start an HTTP server
start_server() {
    echo -e "${BLUE}Starting HTTP server...${NC}"
    
    # Check if port 8000 is already in use
    if command -v lsof &> /dev/null; then
        if lsof -Pi :8000 -sTCP:LISTEN -t &> /dev/null ; then
            echo -e "${YELLOW}Warning: Port 8000 is already in use. Server may not start correctly.${NC}"
        fi
    fi
    
    # Start server in background
    if [ "$(uname)" == "Darwin" ]; then
        # macOS
        python3 -m http.server 8000 &
    else
        # Linux and others
        python -m http.server 8000 &
    fi
    
    # Save server process ID
    SERVER_PID=$!
    
    # Check if server started successfully
    sleep 2
    if kill -0 $SERVER_PID 2>/dev/null; then
        echo -e "${GREEN}HTTP server started successfully on port 8000.${NC}"
        return 0
    else
        echo -e "${RED}Failed to start HTTP server.${NC}"
        return 1
    fi
}

# Function to open the dashboard in the default browser
open_dashboard() {
    echo -e "${BLUE}Opening dashboard in your default browser...${NC}"
    
    # URL to open
    DASHBOARD_URL="http://localhost:8000/water_quality_dashboard.html"
    
    # Check if the dashboard file exists
    if [ ! -f "water_quality_dashboard.html" ]; then
        echo -e "${RED}Error: water_quality_dashboard.html not found.${NC}"
        return 1
    fi
    
    # Open browser based on OS
    if [ "$(uname)" == "Darwin" ]; then
        # macOS
        open "$DASHBOARD_URL"
    elif [ "$(uname)" == "Linux" ]; then
        # Linux
        if command -v xdg-open &> /dev/null; then
            xdg-open "$DASHBOARD_URL"
        elif command -v gnome-open &> /dev/null; then
            gnome-open "$DASHBOARD_URL"
        else
            echo -e "${YELLOW}Could not automatically open browser. Please visit:${NC}"
            echo -e "${BLUE}$DASHBOARD_URL${NC}"
            return 1
        fi
    else
        # Other OS
        echo -e "${YELLOW}Could not automatically open browser. Please visit:${NC}"
        echo -e "${BLUE}$DASHBOARD_URL${NC}"
        return 1
    fi
    
    echo -e "${GREEN}Dashboard opened in browser.${NC}"
    return 0
}

# Function to cleanup on exit
cleanup() {
    echo -e "\n${BLUE}Cleaning up...${NC}"
    if [ ! -z "$SERVER_PID" ]; then
        kill $SERVER_PID 2>/dev/null
        echo -e "${GREEN}HTTP server stopped.${NC}"
    fi
    echo -e "${GREEN}Done!${NC}"
}

# Register cleanup function to run on script exit
trap cleanup EXIT

# Main function
main() {
    echo -e "${BLUE}===============================================${NC}"
    echo -e "${GREEN}Water Quality Dynamics in Malaysia - Project Runner${NC}"
    echo -e "${BLUE}===============================================${NC}"
    
    # Check essential commands
    echo -e "\n${BLUE}Checking for required dependencies...${NC}"
    
    # Determine python command (python or python3)
    PYTHON_CMD="python"
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        # Check Python version
        PYTHON_VERSION=$(python --version 2>&1 | cut -d' ' -f2)
        if [[ "${PYTHON_VERSION}" < "3" ]]; then
            echo -e "${YELLOW}Warning: Python version ${PYTHON_VERSION} detected. This script requires Python 3.${NC}"
            if ! command -v python3 &> /dev/null; then
                echo -e "${RED}Error: Python 3 is not installed.${NC}"
                exit 1
            else
                PYTHON_CMD="python3"
            fi
        fi
    else
        echo -e "${RED}Error: Python is not installed.${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}Using ${PYTHON_CMD} command.${NC}"
    
    # Check for pip
    PIP_CMD="pip"
    if command -v pip3 &> /dev/null; then
        PIP_CMD="pip3"
    elif ! command -v pip &> /dev/null; then
        echo -e "${RED}Error: pip is not installed.${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}Using ${PIP_CMD} command.${NC}"
    
    # Run the workflow
    check_python_dependencies || exit 1
    run_analysis || exit 1
    start_server || exit 1
    open_dashboard || echo -e "${YELLOW}Warning: Could not open browser automatically. Please visit http://localhost:8000/water_quality_dashboard.html${NC}"
    
    # Keep the script running until user decides to stop
    echo -e "\n${GREEN}Project is now running.${NC}"
    echo -e "${YELLOW}Press Ctrl+C to stop the server and exit.${NC}"
    
    # Wait for user to press Ctrl+C
    while true; do
        sleep 1
    done
}

# Show note for Windows users
if [ "$OSTYPE" == "msys" ] || [ "$OSTYPE" == "win32" ]; then
    echo -e "${YELLOW}Note for Windows users:${NC}"
    echo -e "This script is designed for Linux/macOS. For Windows, you can:"
    echo -e "1. Use Windows Subsystem for Linux (WSL) to run this script"
    echo -e "2. Or manually run these steps:"
    echo -e "   a. Install Python 3 and required packages: pip install -r requirements.txt"
    echo -e "   b. Run the analysis: python water_quality_analysis.py"
    echo -e "   c. Start a server: python -m http.server 8000"
    echo -e "   d. Open http://localhost:8000/water_quality_dashboard.html in your browser"
    
    read -p "Do you want to continue running this script? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Execute main function
main

