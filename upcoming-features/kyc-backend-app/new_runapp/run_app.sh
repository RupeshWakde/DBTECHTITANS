#!/bin/bash

# KYC API Application Runner - Shell Script
# This shell script provides easy access to run the KYC application
source venv/bin/activate
# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Default values
HOST="0.0.0.0"
PORT=8000
DEV_MODE=false
WORKERS=1
HEALTH_CHECK=false

# Function to print colored output
print_status() {
    echo -e "${CYAN}============================================================${NC}"
    echo -e "${CYAN}🎯 KYC API Application Runner - Shell${NC}"
    echo -e "${CYAN}============================================================${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --host)
            HOST="$2"
            shift 2
            ;;
        --port)
            PORT="$2"
            shift 2
            ;;
        --dev|-d)
            DEV_MODE=true
            shift
            ;;
        --workers)
            WORKERS="$2"
            shift 2
            ;;
        --health-check)
            HEALTH_CHECK=true
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --host HOST          Host to bind to (default: 0.0.0.0)"
            echo "  --port PORT          Port to bind to (default: 8000)"
            echo "  --dev, -d            Enable development mode with auto-reload"
            echo "  --workers NUM        Number of worker processes (default: 1)"
            echo "  --health-check       Run health check after startup"
            echo "  --help, -h           Show this help message"
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Print header
print_status

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        print_error "Python is not installed or not in PATH"
        print_info "Please install Python and add it to your PATH"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

# Get Python version
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1)
print_success "Python found: $PYTHON_VERSION"

# Get script directory and change to parent directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"

# Change to parent directory
cd "$PARENT_DIR"

# Check if main.py exists
if [ ! -f "main.py" ]; then
    print_error "main.py not found in parent directory"
    print_info "Please run this script from the new_runapp folder"
    exit 1
fi

print_success "main.py located successfully"
echo ""

# Display configuration
echo -e "${GREEN}🚀 Starting KYC API Application...${NC}"
echo -e "${BLUE}📍 Host: $HOST${NC}"
echo -e "${BLUE}🔌 Port: $PORT${NC}"
echo -e "${BLUE}🔄 Dev Mode: $DEV_MODE${NC}"
echo -e "${BLUE}👥 Workers: $WORKERS${NC}"
echo -e "${BLUE}🏥 Health Check: $HEALTH_CHECK${NC}"
echo ""

# Build the command
CMD_ARGS=("new_runapp/run_app.py" "--host" "$HOST" "--port" "$PORT" "--workers" "$WORKERS")

if [ "$DEV_MODE" = true ]; then
    CMD_ARGS+=("--dev")
fi

if [ "$HEALTH_CHECK" = true ]; then
    CMD_ARGS+=("--health-check")
fi

COMMAND="$PYTHON_CMD ${CMD_ARGS[*]}"
echo -e "${YELLOW}Executing: $COMMAND${NC}"
echo ""

# Function to handle cleanup on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}🛑 Application stopped${NC}"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Run the application
if $PYTHON_CMD "${CMD_ARGS[@]}"; then
    print_success "Application completed successfully"
else
    print_error "Application failed to run"
    exit 1
fi

cleanup 