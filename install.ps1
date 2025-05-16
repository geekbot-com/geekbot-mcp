# PowerShell installation script for Windows

# 1. Open PowerShell as Administrator
# 2. Run this command:
#    powershell -ExecutionPolicy Bypass -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/geekbot-com/geekbot-mcp/main/install.ps1' -OutFile 'install.ps1'; .\install.ps1"

# Function to install Python 3.10
function Install-Python {
    if (Get-Command python -ErrorAction SilentlyContinue) {
        Write-Host "Python is already installed"
    } else {
        Write-Host "Downloading Python 3.10..."
        $pythonUrl = "https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe"
        $pythonInstaller = "python-3.10.11-amd64.exe"
        
        Invoke-WebRequest -Uri $pythonUrl -OutFile $pythonInstaller
        Write-Host "Installing Python 3.10..."
        Start-Process -FilePath $pythonInstaller -ArgumentList "/quiet", "InstallAllUsers=1", "PrependPath=1" -Wait
        Remove-Item $pythonInstaller
    }
}

# Function to check if uv is installed
function Test-UVInstalled {
    return (Get-Command uv -ErrorAction SilentlyContinue) -ne $null
}

# Function to install uv
function Install-UV {
    if (Test-UVInstalled) {
        Write-Host "uv is already installed"
        return
    }

    Write-Host "Installing uv..."
    Invoke-WebRequest -Uri "https://astral.sh/uv/install.ps1" -OutFile "uv-install.ps1"
    .\uv-install.ps1
    Remove-Item "uv-install.ps1"

    if (-not (Test-UVInstalled)) {
        Write-Host "Error: uv installation failed or PATH not updated"
        exit 1
    }
}

# Function to create MCP configuration
function Create-MCPConfig {
    param (
        [string]$ApiKey,
        [string]$UvPath
    )
    
    $configDir = "$env:APPDATA\geekbot-mcp"
    if (-not (Test-Path $configDir)) {
        New-Item -ItemType Directory -Path $configDir | Out-Null
    }

    $config = @{
        mcpServers = @{
            "geekbot-mcp" = @{
                command = $UvPath
                args = @("tool", "run", "geekbot-mcp")
                env = @{
                    GB_API_KEY = $ApiKey
                }
            }
        }
    }

    $configJson = $config | ConvertTo-Json -Depth 10
    $configJson | Out-File "$configDir\config.json" -Encoding UTF8
    Write-Host "MCP configuration created at: $configDir\config.json"
    return $config
}

# Function to configure Claude Desktop
function Configure-ClaudeDesktop {
    param (
        [hashtable]$MCPConfig
    )
    
    $claudeConfigPath = "$env:APPDATA\Claude\claude_desktop_config.json"
    $claudeConfigDir = Split-Path -Parent $claudeConfigPath
    
    # Create directory if it doesn't exist
    if (-not (Test-Path $claudeConfigDir)) {
        New-Item -ItemType Directory -Path $claudeConfigDir | Out-Null
    }
    
    # Read existing config or create new one
    $claudeConfig = $null
    $fileContent = $null
    if (Test-Path $claudeConfigPath) {
        $fileContent = (Get-Content $claudeConfigPath -Raw)
    }
    if ($fileContent -and $fileContent.Trim().Length -gt 0) {
        $claudeConfig = $fileContent | ConvertFrom-Json
    }
    if ($null -eq $claudeConfig) {
        $claudeConfig = New-Object PSObject
    }
    # Ensure mcpServers property exists and is a hashtable
    if (-not ($claudeConfig.PSObject.Properties.Name -contains 'mcpServers')) {
        $claudeConfig | Add-Member -MemberType NoteProperty -Name mcpServers -Value @{}
    } elseif ($claudeConfig.mcpServers -isnot [hashtable]) {
        $mcpServersHash = @{}
        foreach ($prop in $claudeConfig.mcpServers.PSObject.Properties) {
            $mcpServersHash[$prop.Name] = $prop.Value
        }
        $claudeConfig.mcpServers = $mcpServersHash
    }
    # Ensure geekbot-mcp server exists or update only GB_API_KEY
    $hasKey = $false
    if ($claudeConfig.mcpServers -is [hashtable]) {
        $hasKey = $claudeConfig.mcpServers.ContainsKey('geekbot-mcp')
    } else {
        $hasKey = $claudeConfig.mcpServers.PSObject.Properties.Name -contains 'geekbot-mcp'
    }
    if (-not $hasKey) {
        $claudeConfig.mcpServers['geekbot-mcp'] = $MCPConfig.mcpServers['geekbot-mcp']
    } else {
        $claudeConfig.mcpServers['geekbot-mcp'].env.GB_API_KEY = $MCPConfig.mcpServers['geekbot-mcp'].env.GB_API_KEY
    }
    
    # Save updated config
    $claudeConfigJson = $claudeConfig | ConvertTo-Json -Depth 10
    $claudeConfigJson | Out-File $claudeConfigPath -Encoding UTF8
    Write-Host "Claude Desktop configuration updated at: $claudeConfigPath"
}

# Function to check if Claude is installed
function Test-ClaudeInstalled {
    $claudePathLocal = "$env:LOCALAPPDATA\AnthropicClaude\claude.exe"
    return (Test-Path $claudePathLocal)
}

# Function to check if Cursor is installed
function Test-CursorInstalled {
    $cursorPathLocal = "$env:LOCALAPPDATA\Programs\cursor\Cursor.exe"
    return (Test-Path $cursorPathLocal)
}

# Function to prompt for Claude configuration
function Prompt-ClaudeConfig {
    Write-Host "`nClaude is installed. Would you like to add Geekbot MCP configuration to Claude? (y/N)"
    $response = Read-Host
    return $response -match '^[yY](es)?$'
}

# Function to check if geekbot-mcp is installed
function Test-GeekbotMCPInstalled {
    $toolList = uv tool list
    return $toolList -match "geekbot-mcp"
}

# Function to get Cursor config path
function Get-CursorConfigPath {
    return "$env:USERPROFILE\.cursor\mcp.json"
}

# Function to configure Cursor Desktop
function Configure-CursorDesktop {
    param (
        [hashtable]$MCPConfig
    )
    
    $cursorConfigPath = Get-CursorConfigPath
    $cursorConfigDir = Split-Path -Parent $cursorConfigPath
    
    # Create directory if it doesn't exist
    if (-not (Test-Path $cursorConfigDir)) {
        New-Item -ItemType Directory -Path $cursorConfigDir | Out-Null
    }
    
    # Read existing config or create new one
    $cursorConfig = $null
    $fileContent = $null
    if (Test-Path $cursorConfigPath) {
        $fileContent = (Get-Content $cursorConfigPath -Raw)
    }
    if ($fileContent -and $fileContent.Trim().Length -gt 0) {
        $cursorConfig = $fileContent | ConvertFrom-Json
    }
    if ($null -eq $cursorConfig) {
        $cursorConfig = New-Object PSObject
    }
    # Ensure mcpServers property exists and is a hashtable
    if (-not ($cursorConfig.PSObject.Properties.Name -contains 'mcpServers')) {
        $cursorConfig | Add-Member -MemberType NoteProperty -Name mcpServers -Value @{}
    } elseif ($cursorConfig.mcpServers -isnot [hashtable]) {
        $mcpServersHash = @{}
        foreach ($prop in $cursorConfig.mcpServers.PSObject.Properties) {
            $mcpServersHash[$prop.Name] = $prop.Value
        }
        $cursorConfig.mcpServers = $mcpServersHash
    }
    # Ensure geekbot-mcp server exists or update only GB_API_KEY
    $hasKey = $false
    if ($cursorConfig.mcpServers -is [hashtable]) {
        $hasKey = $cursorConfig.mcpServers.ContainsKey('geekbot-mcp')
    } else {
        $hasKey = $cursorConfig.mcpServers.PSObject.Properties.Name -contains 'geekbot-mcp'
    }
    if (-not $hasKey) {
        $cursorConfig.mcpServers['geekbot-mcp'] = $MCPConfig.mcpServers['geekbot-mcp']
    } else {
        $cursorConfig.mcpServers['geekbot-mcp'].env.GB_API_KEY = $MCPConfig.mcpServers['geekbot-mcp'].env.GB_API_KEY
    }
    
    # Save updated config
    $cursorConfigJson = $cursorConfig | ConvertTo-Json -Depth 10
    $cursorConfigJson | Out-File $cursorConfigPath -Encoding UTF8
    Write-Host "Cursor configuration updated at: $cursorConfigPath"
}

# Function to prompt for Cursor configuration
function Prompt-CursorConfig {
    Write-Host "`nCursor is installed. Would you like to add Geekbot MCP configuration to Cursor? (y/N)"
    $response = Read-Host
    return $response -match '^[yY](es)?$'
}

# Main installation process
Write-Host "Starting installation for Windows..."

# Check for Claude and Cursor
$claudeInstalled = Test-ClaudeInstalled
$cursorInstalled = Test-CursorInstalled
if (-not $claudeInstalled -and -not $cursorInstalled) {
    Write-Host "Neither Claude nor Cursor is installed. Please install at least one before running this script."
    exit 1
}
if (-not $claudeInstalled) {
    Write-Host "Claude is not installed. Skipping Claude configuration."
}
if (-not $cursorInstalled) {
    Write-Host "Cursor is not installed. Skipping Cursor configuration."
}

# Install Python
Install-Python

# Install uv
Install-UV

# Get uv path
$uvPath = (Get-Command uv | Select-Object -ExpandProperty Path) -replace '\\', '\\'

# Prompt for API key
Write-Host "`nPlease enter your Geekbot API key (you can find it at https://geekbot.com/dashboard/api-webhooks:"
$apiKey = Read-Host
# Create MCP configuration
$mcpConfig = Create-MCPConfig -ApiKey $apiKey -UvPath $uvPath

# Install geekbot-mcp
Write-Host "Installing geekbot-mcp..."
if (Test-GeekbotMCPInstalled) {
    Write-Host "geekbot-mcp is already installed, upgrading..."
    uv tool install --upgrade geekbot-mcp
} else {
    Write-Host "Installing geekbot-mcp..."
    uv tool install geekbot-mcp
}

# Configure Claude if installed
$claudeConfigured = $false
if (Test-ClaudeInstalled) {
    if (Prompt-ClaudeConfig) {
        # Configure Claude Desktop
        Configure-ClaudeDesktop -MCPConfig $mcpConfig
        $claudeConfigured = $true
        Write-Host "Claude configuration completed."
    } else {
        Write-Host "Skipping Claude configuration as requested."
    }
}

# Configure Cursor if installed
$cursorConfigured = $false
if (Test-CursorInstalled) {
    if (Prompt-CursorConfig) {
        # Configure Cursor Desktop
        Configure-CursorDesktop -MCPConfig $mcpConfig
        $cursorConfigured = $true
        Write-Host "Cursor configuration completed."
    } else {
        Write-Host "Skipping Cursor configuration as requested."
    }
}

Write-Host "Installation completed!"
if ($claudeConfigured -or $cursorConfigured) {
    Write-Host "`nNext steps:"
    if ($claudeConfigured) {
        Write-Host "- Restart Claude Desktop to apply the changes"
    }
    if ($cursorConfigured) {
        Write-Host "- Restart Cursor to apply the changes"
    }
    Write-Host "- You can now use Geekbot MCP in your conversations"
}