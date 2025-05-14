#!/bin/bash

# Installation Instructions:
# One-line installation command for macOS/Linux:
# curl -sSL https://raw.githubusercontent.com/geekbot-com/geekbot-mcp/main/install.sh | bash
#
# Or using wget:
# wget -qO- https://raw.githubusercontent.com/geekbot-com/geekbot-mcp/main/install.sh | bash
#

# Function to detect OS
detect_os() {
    case "$(uname -s)" in
        Darwin*)    echo "macos";;
        Linux*)     echo "linux";;
        *)          echo "unknown";;
    esac
}

# Function to check if Claude is installed
check_claude() {
    local os="$1"
    case "$os" in
        "macos")
            if [ -d "/Applications/Claude.app" ]; then
                return 0
            fi
            ;;
        "linux")
            if [ -d "$HOME/.local/share/Claude" ]; then
                return 0
            fi
            ;;
    esac
    return 1
}

# Function to check if Cursor is installed
check_cursor() {
    local os="$1"
    case "$os" in
        "macos")
            if [ -d "/Applications/Cursor.app" ]; then
                return 0
            fi
            ;;
        "linux")
            if [ -d "$HOME/.local/share/Cursor" ]; then
                return 0
            fi
            ;;
    esac
    return 1
}

# Function to prompt for Claude installation
prompt_claude_install() {
    local os="$1"
    echo "Claude is not installed. Please install it from:"
    case "$os" in
        "macos")
            echo "https://claude.ai/download"
            ;;
        "linux")
            echo "https://claude.ai/download"
            ;;
    esac
}

# Function to prompt for Cursor installation
prompt_cursor_install() {
    local os="$1"
    echo "Cursor is not installed. Please install it from:"
    case "$os" in
        "macos")
            echo "https://cursor.sh/download"
            ;;
        "linux")
            echo "https://cursor.sh/download"
            ;;
    esac
}

# Function to get Claude Desktop config path
get_claude_config_path() {
    local os="$1"
    case "$os" in
        "macos")
            echo "$HOME/Library/Application Support/Claude/claude_desktop_config.json"
            ;;
        "linux")
            echo "$HOME/.config/Claude/claude_desktop_config.json"
            ;;
        *)
            echo ""
            ;;
    esac
}

# Function to get Cursor config path
get_cursor_config_path() {
    echo "$HOME/.cursor/mcp.json"
}

# Function to install Python 3.10 on macOS
install_python_macos() {
    if ! command -v brew &>/dev/null; then
        echo "Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi

    if command -v python3.10 &>/dev/null; then
        echo "Python 3.10 is already installed"
    else
        echo "Installing Python 3.10..."
        brew install python@3.10
        echo 'export PATH="/usr/local/opt/python@3.10/bin:$PATH"' >> ~/.zshrc
        source ~/.zshrc
    fi
}

# Function to install Python 3.10 on Linux
install_python_linux() {
    if command -v python3.10 &>/dev/null; then
        echo "Python 3.10 is already installed"
    else
        echo "Installing Python 3.10..."
        sudo apt update
        sudo apt install -y software-properties-common
        sudo add-apt-repository -y ppa:deadsnakes/ppa
        sudo apt update
        sudo apt install -y python3.10 python3.10-venv python3.10-dev
    fi
}

# Function to check if uv is installed
check_uv() {
    if command -v uv &>/dev/null; then
        return 0
    fi
    return 1
}

# Function to install uv
install_uv() {
    if check_uv; then
        echo "uv is already installed"
        return 0
    fi

    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    
    # Add uv to PATH
    if [ -f "$HOME/.local/bin/env" ]; then
        source "$HOME/.local/bin/env"
    fi
    
    # Verify uv is in PATH
    if ! check_uv; then
        echo "Error: uv installation failed or PATH not updated"
        exit 1
    fi
}

# Function to create MCP configuration
create_mcp_config() {
    local api_key="$1"
    local uv_path="$2"
    local config_dir="$HOME/.config/geekbot-mcp"
    
    mkdir -p "$config_dir"
    
    cat > "$config_dir/config.json" << EOF
{
  "mcpServers": {
    "geekbot-mcp": {
      "command": "$uv_path",
      "args": ["tool", "run", "geekbot-mcp"],
      "env": {
        "GB_API_KEY": "$api_key"
      }
    }
  }
}
EOF
    
    echo "MCP configuration created at: $config_dir/config.json"
}

# Function to create JSON configuration using Python
create_json_config_python() {
    local config_file="$1"
    local uv_path="$2"
    local api_key="$3"
    
    python3 -c "
import json
import os

config = {
    'mcpServers': {
        'geekbot-mcp': {
            'command': '$uv_path',
            'args': ['tool', 'run', 'geekbot-mcp'],
            'env': {
                'GB_API_KEY': '$api_key'
            }
        }
    }
}

# Read existing config if it exists
if os.path.exists('$config_file'):
    with open('$config_file', 'r') as f:
        existing_config = json.load(f)
        if 'mcpServers' in existing_config:
            existing_config['mcpServers']['geekbot-mcp'] = config['mcpServers']['geekbot-mcp']
            config = existing_config

# Write the config
with open('$config_file', 'w') as f:
    json.dump(config, f, indent=2)
"
}

# Function to configure Claude Desktop
configure_claude_desktop() {
    local config_file=$(get_claude_config_path "$OS")
    local config_dir=$(dirname "$config_file")
    
    if [ -z "$config_file" ]; then
        echo "Error: Unsupported operating system for Claude Desktop configuration"
        return 1
    fi
    
    # Create directory if it doesn't exist
    mkdir -p "$config_dir"
    
    # Check if jq is installed
    if command -v jq &>/dev/null; then
        # Use jq for JSON manipulation
        if [ -f "$config_file" ]; then
            local temp_file=$(mktemp)
            jq --arg cmd "$UV_PATH" --arg api_key "$API_KEY" '
                .mcpServers["geekbot-mcp"] = {
                    "command": $cmd,
                    "args": ["tool", "run", "geekbot-mcp"],
                    "env": {
                        "GB_API_KEY": $api_key
                    }
                }
            ' "$config_file" > "$temp_file"
            mv "$temp_file" "$config_file"
        else
            # Create new config with jq
            jq -n --arg cmd "$UV_PATH" --arg api_key "$API_KEY" '
                {
                    "mcpServers": {
                        "geekbot-mcp": {
                            "command": $cmd,
                            "args": ["tool", "run", "geekbot-mcp"],
                            "env": {
                                "GB_API_KEY": $api_key
                            }
                        }
                    }
                }
            ' > "$config_file"
        fi
    else
        # Use Python as fallback for JSON manipulation
        echo "jq not found, using Python for JSON manipulation..."
        create_json_config_python "$config_file" "$UV_PATH" "$API_KEY"
    fi
    
    echo "Claude Desktop configuration updated at: $config_file"
}

# Function to configure Cursor Desktop
configure_cursor_desktop() {
    local config_file=$(get_cursor_config_path)
    local config_dir=$(dirname "$config_file")
    
    # Create directory if it doesn't exist
    mkdir -p "$config_dir"
    
    # Check if jq is installed
    if command -v jq &>/dev/null; then
        # Use jq for JSON manipulation
        if [ -f "$config_file" ]; then
            local temp_file=$(mktemp)
            jq --arg cmd "$UV_PATH" --arg api_key "$API_KEY" '
                .mcpServers["geekbot-mcp"] = {
                    "command": $cmd,
                    "args": ["tool", "run", "geekbot-mcp"],
                    "env": {
                        "GB_API_KEY": $api_key
                    }
                }
            ' "$config_file" > "$temp_file"
            mv "$temp_file" "$config_file"
        else
            # Create new config with jq
            jq -n --arg cmd "$UV_PATH" --arg api_key "$API_KEY" '
                {
                    "mcpServers": {
                        "geekbot-mcp": {
                            "command": $cmd,
                            "args": ["tool", "run", "geekbot-mcp"],
                            "env": {
                                "GB_API_KEY": $api_key
                            }
                        }
                    }
                }
            ' > "$config_file"
        fi
    else
        # Use Python as fallback for JSON manipulation
        echo "jq not found, using Python for JSON manipulation..."
        create_json_config_python "$config_file" "$UV_PATH" "$API_KEY"
    fi
    
    echo "Cursor configuration updated at: $config_file"
}

# Function to check if geekbot-mcp is installed
check_geekbot_mcp() {
    if uv tool list | grep -q "geekbot-mcp"; then
        return 0
    fi
    return 1
}

# Function to prompt for Claude configuration
prompt_claude_config() {
    echo -e "\nClaude is installed. Would you like to add Geekbot MCP configuration to Claude? (y/N)"
    read -r response </dev/tty
    case "$response" in
        [yY][eE][sS]|[yY])
            return 0
            ;;
        *)
            return 1
            ;;
    esac
}

# Function to prompt for Cursor configuration
prompt_cursor_config() {
    echo -e "\nCursor is installed. Would you like to add Geekbot MCP configuration to Cursor? (y/N)"
    read -r response </dev/tty
    case "$response" in
        [yY][eE][sS]|[yY])
            return 0
            ;;
        *)
            return 1
            ;;
    esac
}

# Main installation process
echo "Detecting operating system..."
OS=$(detect_os)

# Check for Claude and Cursor
if ! check_claude "$OS"; then
    echo "Claude is not installed. Skipping Claude configuration."
fi

if ! check_cursor "$OS"; then
    echo "Cursor is not installed. Skipping Cursor configuration."
fi

case "$OS" in
    "macos")
        echo "Detected macOS"
        install_python_macos
        ;;
    "linux")
        echo "Detected Linux"
        install_python_linux
        ;;
    *)
        echo "Unsupported operating system"
        exit 1
        ;;
esac

# Install uv (common for all OS)
install_uv

# Get uv path
UV_PATH=$(which uv)

# Prompt for API key
echo -e "\nPlease enter your Geekbot API key (you can find it at https://geekbot.com/dashboard/api-webhooks):"
read API_KEY </dev/tty

# Create MCP configuration
create_mcp_config "$API_KEY" "$UV_PATH"

# Install geekbot-mcp
echo "Installing geekbot-mcp..."
if check_geekbot_mcp; then
    echo "geekbot-mcp is already installed, upgrading..."
    uv tool install --upgrade geekbot-mcp
else
    echo "Installing geekbot-mcp..."
    uv tool install geekbot-mcp
fi

# Configure Claude if installed
CLAUDE_CONFIGURED=false
if check_claude "$OS"; then
    if prompt_claude_config; then
        # Configure Claude Desktop
        configure_claude_desktop
        CLAUDE_CONFIGURED=true
        echo "Claude configuration completed."
    else
        echo "Skipping Claude configuration as requested."
    fi
fi

# Configure Cursor if installed
CURSOR_CONFIGURED=false
if check_cursor "$OS"; then
    if prompt_cursor_config; then
        # Configure Cursor Desktop
        configure_cursor_desktop
        CURSOR_CONFIGURED=true
        echo "Cursor configuration completed."
    else
        echo "Skipping Cursor configuration as requested."
    fi
fi

echo "Installation completed!"
if [ "$CLAUDE_CONFIGURED" = true ] || [ "$CURSOR_CONFIGURED" = true ]; then
    echo -e "\nNext steps:"
    if [ "$CLAUDE_CONFIGURED" = true ]; then
        echo "- Restart Claude Desktop to apply the changes"
    fi
    if [ "$CURSOR_CONFIGURED" = true ]; then
        echo "- Restart Cursor to apply the changes"
    fi
    echo "- You can now use Geekbot MCP in your conversations"
fi