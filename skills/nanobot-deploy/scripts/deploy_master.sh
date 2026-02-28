#!/bin/bash
# Deploy a nanobot master bot using Docker
# Master bot monitors and manages other bots

set -e

# Configuration
BOT_NAME="${BOT_NAME:-nanobot-master}"
BOT_TYPE="${BOT_TYPE:-master}"
NAMESPACE="${NAMESPACE:-nanobot}"
CONFIG_DIR="${CONFIG_DIR:-./configs/master}"
DATA_DIR="${DATA_DIR:-./data/master}"
IMAGE="${IMAGE:-ghcr.io/hkuds/nanobot:latest}"
PORT="${PORT:-18790}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Create necessary directories
setup_directories() {
    log_info "Setting up directories..."
    mkdir -p "${DATA_DIR}/config"
    mkdir -p "${DATA_DIR}/workspace"
    mkdir -p "${DATA_DIR}/skills"

    # Copy config if provided
    if [ -f "${CONFIG_DIR}/config.json" ]; then
        cp "${CONFIG_DIR}/config.json" "${DATA_DIR}/config/"
        log_info "Config file copied"
    else
        log_warn "No config.json found in ${CONFIG_DIR}, using default"
    fi

    # Copy master-specific skills
    if [ -d "${CONFIG_DIR}/skills" ]; then
        cp -r "${CONFIG_DIR}/skills"/* "${DATA_DIR}/skills/" 2>/dev/null || true
        log_info "Master skills copied"
    fi
}

# Create Docker command
create_docker_cmd() {
    local cmd="docker run -d \
        --name ${BOT_NAME} \
        --restart unless-stopped \
        -v ${DATA_DIR}/config:/root/.nanobot \
        -v ${DATA_DIR}/workspace:/root/.nanobot/workspace \
        -v ${DATA_DIR}/skills:/root/.nanobot/skills:ro \
        -p ${PORT}:18790 \
        -e BOT_TYPE=${BOT_TYPE} \
        -e NAMESPACE=${NAMESPACE}"

    # Add environment variables for MCP servers
    if [ -n "${MCP_SERVERS_CONFIG}" ]; then
        cmd="${cmd} -e MCP_SERVERS_CONFIG=${MCP_SERVERS_CONFIG}"
    fi

    # Add optional volumes for MCP access
    if [ -n "${MCP Mount additional directories for MCP tools
        for mount in ${MCP_MOUNTS}; do
            cmd="${cmd} -v ${mount}"
        done
    fi

    cmd="${cmd} ${IMAGE} gateway"

    echo "${cmd}"
}

# Main deployment
deploy() {
    log_info "Deploying nanobot master bot..."
    log_info "Bot name: ${BOT_NAME}"
    log_info "Type: ${BOT_TYPE}"
    log_info "Namespace: ${NAMESPACE}"

    # Check if container already exists
    if docker ps -a --format '{{.Names}}' | grep -q "^${BOT_NAME}$"; then
        log_warn "Container ${BOT_NAME} already exists"
        read -p "Remove and recreate? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            docker rm -f "${BOT_NAME}" >/dev/null 2>&1 || true
            log_info "Old container removed"
        else
            log_error "Deployment cancelled"
            exit 1
        fi
    fi

    setup_directories

    local cmd=$(create_docker_cmd)
    log_info "Running: ${cmd}"

    # Deploy
    eval "${cmd}"

    # Wait for container to start
    sleep 2

    # Check if container is running
    if docker ps --format '{{.Names}}' | grep -q "^${BOT_NAME}$"; then
        log_info "Master bot deployed successfully!"
        log_info "Container name: ${BOT_NAME}"
        log_info "Logs: docker logs -f ${BOT_NAME}"
        log_info "Status: docker exec ${BOT_NAME} nanobot status"
    else
        log_error "Deployment failed. Check logs:"
        docker logs "${BOT_NAME}" 2>&1 | tail -20
        exit 1
    fi
}

# Show usage
usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Deploy a nanobot master bot using Docker.

Options:
    BOT_NAME        Container name (default: nanobot-master)
    BOT_TYPE        Bot type (default: master)
    NAMESPACE       Namespace for bot grouping (default: nanobot)
    CONFIG_DIR      Configuration directory (default: ./configs/master)
    DATA_DIR        Data persistence directory (default: ./data/master)
    IMAGE           Docker image (default: ghcr.io/hkuds/nanobot:latest)
    PORT            API port (default: 18790)
    MCP_MOUNTS      Additional directories to mount (space-separated)

Examples:
    # Deploy with default settings
    $0

    # Deploy custom named master bot
    BOT_NAME=prod-master $0

    # Deploy with custom config and data directories
    CONFIG_DIR=/opt/nanobot/master-config DATA_DIR=/data/nanobot/master $0

    # Deploy with MCP workspace mount
    MCP_MOUNTS=/home/user/projects:/home/user/docs $0

EOF
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            usage
            exit 0
            ;;
        *)
            log_error "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

deploy
