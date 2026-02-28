#!/bin/bash
# Cluster management script for nanobot deployment
# Provides commands to check status, restart, update configs across all bots

set -e

# Configuration
NAMESPACE="${NAMESPACE:-nanobot}"
CONFIG_DIR="${CONFIG_DIR:-./configs}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

log_bot() {
    echo -e "${BLUE}[BOT]${NC} $1"
}

# Get all nanobot containers
get_bots() {
    docker ps -a --filter "name=${NAMESPACE}" --format "{{.Names}}"
}

# Get bot type from container labels/env
get_bot_type() {
    local container=$1
    docker inspect "$container" --format '{{range .Config.Env}}{{if eq . "BOT_TYPE=master"}}master{{end}}{{end}}' | head -1
    if [ -z "$(docker inspect "$container" --format '{{range .Config.Env}}{{if eq . "BOT_TYPE=master"}}master{{end}}{{end}}')" ]; then
        echo "slave"
    else
        echo "master"
    fi
}

# Check status of all bots
check_status() {
    log_info "Checking status of all nanobot containers..."
    echo

    local master_found=false
    local slave_count=0

    for bot in $(get_bots); do
        local status=$(docker inspect "$bot" --format '{{.State.Status}}')
        local health=$(docker inspect "$bot" --format '{{.State.Health.Status}}' 2>/dev/null || echo "none")
        local bot_type=$(get_bot_type "$bot")

        if [ "$bot_type" = "master" ]; then
            log_bot "🔷 MASTER: $bot"
            master_found=true
        else
            log_bot "🔹 SLAVE: $bot"
            ((slave_count++))
        fi

        echo "   Status: $status"
        echo "   Health: $health"
        echo "   Uptime: $(docker inspect "$bot" --format '{{.State.StartedAt}}')"
        echo
    done

    if [ "$master_found" = false ]; then
        log_warn "No master bot found"
    fi
    if [ "$slave_count" -eq 0 ]; then
        log_warn "No slave bots found"
    else
        log_info "Total: 1 master, $slave_count slave(s)"
    fi
}

# Restart specific bot or all bots
restart_bots() {
    local target=$1

    if [ "$target" = "all" ]; then
        log_info "Restarting all nanobot containers..."
        for bot in $(get_bots); do
            log_info "Restarting $bot..."
            docker restart "$bot" >/dev/null 2>&1
        done
        log_info "All bots restarted"
    elif [ -n "$target" ]; then
        if docker ps -a --format '{{.Names}}' | grep -q "^${target}$"; then
            log_info "Restarting $target..."
            docker restart "$target" >/dev/null 2>&1
            log_info "$target restarted"
        else
            log_error "Bot not found: $target"
            exit 1
        fi
    else
        log_error "Please specify a bot name or 'all'"
        exit 1
    fi
}

# Stop bots
stop_bots() {
    local target=$1

    if [ "$target" = "all" ]; then
        log_info "Stopping all nanobot containers..."
        for bot in $(get_bots); do
            log_info "Stopping $bot..."
            docker stop "$bot" >/dev/null 2>&1
        done
        log_info "All bots stopped"
    elif [ -n "$target" ]; then
        if docker ps --format '{{.Names}}' | grep -q "^${target}$"; then
            log_info "Stopping $target..."
            docker stop "$target" >/dev/null 2>&1
            log_info "$target stopped"
        else
            log_error "Bot not found or not running: $target"
            exit 1
        fi
    else
        log_error "Please specify a bot name or 'all'"
        exit 1
    fi
}

# Start bots
start_bots() {
    local target=$1

    if [ "$target" = "all" ]; then
        log_info "Starting all nanobot containers..."
        for bot in $(get_bots); do
            if [ "$(docker inspect "$bot" --format '{{.State.Status}}')" != "running" ]; then
                log_info "Starting $bot..."
                docker start "$bot" >/dev/null 2>&1
            fi
        done
        log_info "All bots started"
    elif [ -n "$target" ]; then
        if docker ps -a --format '{{.Names}}' | grep -q "^${target}$"; then
            log_info "Starting $target..."
            docker start "$target" >/dev/null 2>&1
            log_info "$target started"
        else
            log_error "Bot not found: $target"
            exit 1
        fi
    else
        log_error "Please specify a bot name or 'all'"
        exit 1
    fi
}

# Update configuration for a bot
update_config() {
    local bot=$1
    local config_file=$2

    if [ -z "$bot" ]; then
        log_error "Please specify a bot name"
        exit 1
    fi

    if [ ! -f "$config_file" ]; then
        log_error "Config file not found: $config_file"
        exit 1
    fi

    if docker ps --format '{{.Names}}' | grep -q "^${bot}$"; then
        log_info "Copying config to $bot..."
        cat "$config_file" | docker exec -i "$bot" sh -c 'cat > /root/.nanobot/config.json'
        log_info "Config updated, restarting $bot..."
        docker restart "$bot" >/dev/null 2>&1
        log_info "$bot restarted with new config"
    else
        log_error "Bot not found or not running: $bot"
        exit 1
    fi
}

# View logs for a bot
view_logs() {
    local bot=$1
    local lines=$2

    if [ -z "$bot" ]; then
        log_error "Please specify a bot name"
        exit 1
    fi

    if docker ps -a --format '{{.Names}}' | grep -q "^${bot}$"; then
        docker logs --tail "${lines:-100}" -f "$bot"
    else
        log_error "Bot not found: $bot"
        exit 1
    fi
}

# Execute command in a bot
exec_command() {
    local bot=$1
    shift
    local cmd="$@"

    if [ -z "$bot" ]; then
        log_error "Please specify a bot name"
        exit 1
    fi

    if [ -z "$cmd" ]; then
        log_error "Please specify a command to execute"
        exit 1
    fi

    if docker ps --format '{{.Names}}' | grep -q "^${bot}$"; then
        docker exec -it "$bot" $cmd
    else
        log_error "Bot not found or not running: $bot"
        exit 1
    fi
}

# Show usage
usage() {
    cat << EOF
Usage: $0 COMMAND [OPTIONS]

Cluster management commands for nanobot deployment.

Commands:
    status              Show status of all bots
    restart <bot|all>   Restart specific bot or all bots
    start <bot|all>     Start specific bot or all bots
    stop <bot|all>      Stop specific bot or all bots
    config <bot> <file> Update config for a bot and restart it
    logs <bot> [lines]  View logs for a bot (default: 100 lines)
    exec <bot> <cmd>    Execute command in a bot container
    list                List all nanobot containers

Environment:
    NAMESPACE           Bot namespace filter (default: nanobot)

Examples:
    # Check status of all bots
    $0 status

    # Restart all bots
    $0 restart all

    # Restart specific bot
    $0 restart nanobot-master

    # Update config for a bot
    $0 config nanobot-slave ./config.json

    # View logs
    $0 logs nanobot-master

    # Execute nanobot status command in container
    $0 exec nanobot-master nanobot status

EOF
}

# Main
case "${1:-}" in
    status)
        check_status
        ;;
    restart)
        restart_bots "${2:-}"
        ;;
    start)
        start_bots "${2:-}"
        ;;
    stop)
        stop_bots "${2:-}"
        ;;
    config)
        update_config "$2" "$3"
        ;;
    logs)
        view_logs "$2" "${3:-100}"
        ;;
    exec)
        shift
        exec_command "$@"
        ;;
    list)
        get_bots
        ;;
    -h|--help|help)
        usage
        ;;
    *)
        log_error "Unknown command: ${1:-}"
        usage
        exit 1
        ;;
esac
