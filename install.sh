#!/usr/bin/env bash
# ==============================================================================
# InBoost Runtime & Proxy One-Line Installer
# Supports: macOS (Apple Silicon M1-M4 & Intel), Linux (x86_64 & arm64)
# Website:  https://inboost.pro/ai-proxy
# ==============================================================================
set -euo pipefail

COLOR_RESET="\033[0m"
COLOR_CYAN="\033[1;36m"
COLOR_GREEN="\033[1;32m"
COLOR_YELLOW="\033[1;33m"
COLOR_RED="\033[1;31m"

INBOOST_VERSION="${INBOOST_VERSION:-0.3.0}"
GITHUB_REPO="inboost-dev/inboost-ai-proxy-runtime"
RELEASE_BASE_URL="https://github.com/${GITHUB_REPO}/releases/download/v${INBOOST_VERSION}"

echo -e "${COLOR_CYAN}┌────────────────────────────────────────────────────────┐${COLOR_RESET}"
echo -e "${COLOR_CYAN}│       InBoost Runtime & Proxy Installer                │${COLOR_RESET}"
echo -e "${COLOR_CYAN}│       High-Performance Semantic Router for AI Agents   │${COLOR_RESET}"
echo -e "${COLOR_CYAN}│       https://inboost.pro/ai-proxy                     │${COLOR_RESET}"
echo -e "${COLOR_CYAN}└────────────────────────────────────────────────────────┘${COLOR_RESET}"

# 1. Detect OS
OS_RAW="$(uname -s 2>/dev/null || echo "unknown")"
case "$(echo "$OS_RAW" | tr '[:upper:]' '[:lower:]')" in
  darwin*)
    OS_NORMALIZED="macos"
    OS_TARGET="darwin"
    ;;
  linux*)
    OS_NORMALIZED="linux"
    OS_TARGET="linux"
    ;;
  mingw*|msys*|cygwin*)
    OS_NORMALIZED="windows"
    OS_TARGET="windows"
    ;;
  *)
    OS_NORMALIZED="generic"
    OS_TARGET="unknown"
    ;;
esac

# 2. Detect Architecture
ARCH_RAW="$(uname -m 2>/dev/null || echo "unknown")"
case "$ARCH_RAW" in
  arm64|aarch64)
    ARCH_TARGET="arm64"
    ARCH_LABEL="Apple Silicon / ARM64"
    ;;
  x86_64|amd64)
    ARCH_TARGET="x86_64"
    ARCH_LABEL="Intel / AMD64"
    ;;
  *)
    ARCH_TARGET="$ARCH_RAW"
    ARCH_LABEL="$ARCH_RAW"
    ;;
esac

echo -e "Detected Platform: ${COLOR_GREEN}${OS_NORMALIZED}${COLOR_RESET} (${ARCH_LABEL}, ${ARCH_TARGET})"

# 3. Determine Installation Target Directory (Default: Rootless User Space)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" 2>/dev/null && pwd || echo "")"
if [ "${INBOOST_SYSTEM:-0}" = "1" ] && [ -w "/usr/local/bin" ]; then
  INSTALL_DIR="/usr/local/bin"
else
  INSTALL_DIR="${HOME}/.local/bin"
  mkdir -p "$INSTALL_DIR" 2>/dev/null || true
fi
TARGET_BIN="${INSTALL_DIR}/inboost-proxy"

INSTALL_SUCCESS=0

# Helper: download using curl or wget
download_file() {
  local url="$1"
  local dest="$2"
  if command -v curl >/dev/null 2>&1; then
    curl -fsSL "$url" -o "$dest" 2>/dev/null
  elif command -v wget >/dev/null 2>&1; then
    wget -q "$url" -O "$dest" 2>/dev/null
  else
    return 1
  fi
}

# Helper: compute sha256
compute_sha256() {
  local file="$1"
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$file" | awk '{print $1}'
  elif command -v shasum >/dev/null 2>&1; then
    shasum -a 256 "$file" | awk '{print $1}'
  else
    return 1
  fi
}

# ------------------------------------------------------------------------------
# Method 0: Local Repository / Dist Artifacts (Fastest & Offline-First)
# ------------------------------------------------------------------------------
if [ -n "$SCRIPT_DIR" ]; then
  LOCAL_CANDIDATES=(
    "${SCRIPT_DIR}/dist/inboost-proxy-${OS_TARGET}-${ARCH_TARGET}"
    "${SCRIPT_DIR}/dist/inboost-proxy-${OS_TARGET}-amd64"
    "${SCRIPT_DIR}/dist/inboost-proxy-linux-x86_64"
    "${SCRIPT_DIR}/dist/inboost-proxy"
    "${SCRIPT_DIR}/bin/inboost-proxy-${OS_TARGET}-${ARCH_TARGET}"
    "${SCRIPT_DIR}/bin/inboost-proxy"
  )

  for CANDIDATE in "${LOCAL_CANDIDATES[@]}"; do
    if [ -f "$CANDIDATE" ] && [ -x "$CANDIDATE" ]; then
      echo -e "\n${COLOR_CYAN}Found local precompiled native binary:${COLOR_RESET} ${CANDIDATE}"
      cp "$CANDIDATE" "$TARGET_BIN"
      chmod 755 "$TARGET_BIN"
      if [ "$OS_TARGET" = "darwin" ]; then
        xattr -d com.apple.quarantine "$TARGET_BIN" 2>/dev/null || true
        if command -v codesign >/dev/null 2>&1; then
          codesign --force --sign - "$TARGET_BIN" 2>/dev/null || true
        fi
      fi
      INSTALL_SUCCESS=1
      break
    fi
  done

  # If binary not copied, check local npm tarball or CLI launcher
  if [ "$INSTALL_SUCCESS" -eq 0 ] && command -v npm >/dev/null 2>&1; then
    if [ -f "${SCRIPT_DIR}/dist/inboost-ai-proxy-${INBOOST_VERSION}.tgz" ]; then
      echo -e "\nAttempting installation via local npm tarball..."
      if npm install -g "${SCRIPT_DIR}/dist/inboost-ai-proxy-${INBOOST_VERSION}.tgz" 2>/dev/null || npm install -g --prefix="${HOME}/.local" "${SCRIPT_DIR}/dist/inboost-ai-proxy-${INBOOST_VERSION}.tgz" 2>/dev/null; then
        INSTALL_SUCCESS=1
      fi
    elif [ -f "${SCRIPT_DIR}/package.json" ]; then
      echo -e "\nAttempting installation via local npm package..."
      if npm install -g "${SCRIPT_DIR}" 2>/dev/null || npm install -g --prefix="${HOME}/.local" "${SCRIPT_DIR}" 2>/dev/null; then
        INSTALL_SUCCESS=1
      fi
    fi
  fi

  # Local Node CLI launcher fallback
  if [ "$INSTALL_SUCCESS" -eq 0 ] && [ -f "${SCRIPT_DIR}/bin/inboost-proxy.js" ] && command -v node >/dev/null 2>&1; then
    echo -e "\nInstalling via local Node CLI launcher..."
    cp "${SCRIPT_DIR}/bin/inboost-proxy.js" "$TARGET_BIN"
    chmod 755 "$TARGET_BIN"
    INSTALL_SUCCESS=1
  fi
fi

# ------------------------------------------------------------------------------
# Method 1: Verified Standalone Native Binary (Remote Release Download)
# ------------------------------------------------------------------------------
BINARY_NAME="inboost-proxy-${OS_TARGET}-${ARCH_TARGET}"
BINARY_URL="${RELEASE_BASE_URL}/${BINARY_NAME}"
CHECKSUMS_URL="${RELEASE_BASE_URL}/checksums.txt"

if [ "$INSTALL_SUCCESS" -eq 0 ] && [ "${INBOOST_INSTALL_METHOD:-binary}" = "binary" ] && [ "$OS_TARGET" != "unknown" ]; then
  echo -e "\nAttempting standalone native binary download for ${COLOR_CYAN}${OS_NORMALIZED} (${ARCH_TARGET})${COLOR_RESET}..."
  
  TMP_DIR="$(mktemp -d -t inboost-install.XXXXXX 2>/dev/null || mktemp -d)"
  trap 'rm -rf "$TMP_DIR"' EXIT INT TERM

  TEMP_BIN="${TMP_DIR}/${BINARY_NAME}"
  TEMP_CHECKSUMS="${TMP_DIR}/checksums.txt"

  if download_file "$CHECKSUMS_URL" "$TEMP_CHECKSUMS" && download_file "$BINARY_URL" "$TEMP_BIN"; then
    echo -e "Verifying cryptographic SHA-256 integrity..."
    EXPECTED_HASH="$(grep "  ${BINARY_NAME}$" "$TEMP_CHECKSUMS" | awk '{print $1}' || true)"
    
    if [ -n "$EXPECTED_HASH" ]; then
      ACTUAL_HASH="$(compute_sha256 "$TEMP_BIN" || true)"
      if [ "$ACTUAL_HASH" = "$EXPECTED_HASH" ]; then
        echo -e "${COLOR_GREEN}✓ SHA-256 Verified:${COLOR_RESET} ${ACTUAL_HASH}"
        
        # Install binary
        chmod 755 "$TEMP_BIN"
        mv "$TEMP_BIN" "$TARGET_BIN"

        # macOS specific security adjustments (quarantine removal and ad-hoc codesign)
        if [ "$OS_TARGET" = "darwin" ]; then
          xattr -d com.apple.quarantine "$TARGET_BIN" 2>/dev/null || true
          if command -v codesign >/dev/null 2>&1; then
            codesign --force --sign - "$TARGET_BIN" 2>/dev/null || true
          fi
        fi

        INSTALL_SUCCESS=1
      else
        echo -e "${COLOR_RED}✗ Checksum mismatch!${COLOR_RESET} Expected: ${EXPECTED_HASH}, Got: ${ACTUAL_HASH}"
      fi
    fi
  fi
fi

# ------------------------------------------------------------------------------
# Method 2: pipx (Isolated CLI for Python environments)
# ------------------------------------------------------------------------------
if [ "$INSTALL_SUCCESS" -eq 0 ] && command -v pipx >/dev/null 2>&1; then
  echo -e "Attempting installation via ${COLOR_CYAN}pipx${COLOR_RESET}..."
  if [ -n "$SCRIPT_DIR" ] && [ -f "${SCRIPT_DIR}/dist/inboost_ai_proxy-${INBOOST_VERSION}-cp312-cp312-linux_x86_64.whl" ]; then
    pipx install --force "${SCRIPT_DIR}/dist/inboost_ai_proxy-${INBOOST_VERSION}-cp312-cp312-linux_x86_64.whl" --pip-args="--no-deps" >/dev/null 2>&1 && INSTALL_SUCCESS=1 || true
  fi
  if [ "$INSTALL_SUCCESS" -eq 0 ]; then
    pipx install --force inboost-ai-proxy >/dev/null 2>&1 && INSTALL_SUCCESS=1 || true
  fi
fi

# ------------------------------------------------------------------------------
# Method 3: npm (Rootless user installation via --prefix)
# ------------------------------------------------------------------------------
if [ "$INSTALL_SUCCESS" -eq 0 ] && command -v npm >/dev/null 2>&1; then
  echo -e "Attempting rootless installation via ${COLOR_CYAN}npm${COLOR_RESET}..."
  npm install -g --prefix="${HOME}/.local" inboost-ai-proxy >/dev/null 2>&1 && INSTALL_SUCCESS=1 || true
fi

# ------------------------------------------------------------------------------
# Method 4: Python venv (Rootless isolated environment)
# ------------------------------------------------------------------------------
if [ "$INSTALL_SUCCESS" -eq 0 ] && command -v python3 >/dev/null 2>&1; then
  echo -e "Attempting rootless installation via isolated Python venv..."
  VENV_DIR="${HOME}/.inboost/venv"
  if python3 -m venv "$VENV_DIR" >/dev/null 2>&1; then
    if [ -n "$SCRIPT_DIR" ] && [ -f "${SCRIPT_DIR}/dist/inboost_ai_proxy-${INBOOST_VERSION}-cp312-cp312-linux_x86_64.whl" ]; then
      "$VENV_DIR/bin/pip" install fastapi uvicorn httpx pydantic cryptography pyyaml >/dev/null 2>&1 || true
      if "$VENV_DIR/bin/pip" install "${SCRIPT_DIR}/dist/inboost_ai_proxy-${INBOOST_VERSION}-cp312-cp312-linux_x86_64.whl" --no-deps >/dev/null 2>&1; then
        ln -sf "$VENV_DIR/bin/inboost-proxy" "$TARGET_BIN"
        INSTALL_SUCCESS=1
      fi
    fi
  fi
fi

# ------------------------------------------------------------------------------
# Installation Result, IDE Skill Setup & Auto-Start Daemon
# ------------------------------------------------------------------------------
if [ "$INSTALL_SUCCESS" -eq 1 ]; then
  echo -e "\n${COLOR_GREEN}✓ InBoost Proxy successfully installed!${COLOR_RESET}"
  
  # Ensure target directory is in PATH for the current shell session
  export PATH="${INSTALL_DIR}:${PATH}"

  # Configure PATH in shell config if needed
  if ! echo "$PATH" | tr ':' '\n' | grep -qx "$INSTALL_DIR"; then
    echo -e "${COLOR_YELLOW}Notice: ${INSTALL_DIR} was added to PATH.${COLOR_RESET}"
    for RC in "${HOME}/.bashrc" "${HOME}/.zshrc"; do
      if [ -f "$RC" ] && ! grep -q "$INSTALL_DIR" "$RC" 2>/dev/null; then
        echo "export PATH=\"${INSTALL_DIR}:\$PATH\"" >> "$RC"
      fi
    done
  fi

  # Auto-configure IDE skills & rules for Claude Code, Cursor, OpenHands, Cline, Aider
  if [ -x "$TARGET_BIN" ]; then
    echo -e "Configuring agent skills & IDE rules for Claude Code, Cursor, OpenHands..."
    (cd "$HOME" && "$TARGET_BIN" --install-skills >/dev/null 2>&1 || true)
  fi

  # Configure ANTHROPIC_BASE_URL & CLAUDE_CODE_AUTO_MODE_SERVER for Claude Code in shell profiles
  for RC in "${HOME}/.bashrc" "${HOME}/.zshrc"; do
    if [ -f "$RC" ] && ! grep -q "ANTHROPIC_BASE_URL.*8080" "$RC" 2>/dev/null; then
      echo 'export ANTHROPIC_BASE_URL="http://127.0.0.1:8080"' >> "$RC"
    fi
    if [ -f "$RC" ] && ! grep -q "CLAUDE_CODE_AUTO_MODE_SERVER" "$RC" 2>/dev/null; then
      echo 'export CLAUDE_CODE_AUTO_MODE_SERVER=0' >> "$RC"
    fi
  done

  # ----------------------------------------------------------------------------
  # Configuration Management: Store all default settings in ~/.inboost
  # ----------------------------------------------------------------------------
  INBOOST_HOME="${HOME}/.inboost"
  mkdir -p "${INBOOST_HOME}"
  DEFAULT_CONFIG="${INBOOST_HOME}/config.yaml"
  SILICONFLOW_CONFIG="${INBOOST_HOME}/config.siliconflow.yaml"
  PID_FILE="${INBOOST_HOME}/proxy.pid"
  LOG_FILE="${INBOOST_HOME}/proxy.log"
  PROXY_PORT="${INBOOST_PORT:-8080}"

  if [ -n "$SCRIPT_DIR" ] && [ -f "${SCRIPT_DIR}/configs/proxy_config.siliconflow.yaml" ]; then
    cp "${SCRIPT_DIR}/configs/proxy_config.siliconflow.yaml" "$SILICONFLOW_CONFIG"
  fi

  if [ ! -f "$DEFAULT_CONFIG" ]; then
    echo -e "Creating default configuration at ${COLOR_CYAN}${DEFAULT_CONFIG}${COLOR_RESET}..."
    if [ -n "$SCRIPT_DIR" ] && [ -f "${SCRIPT_DIR}/configs/proxy_config.yaml" ]; then
      cp "${SCRIPT_DIR}/configs/proxy_config.yaml" "$DEFAULT_CONFIG"
    else
      cat > "$DEFAULT_CONFIG" << 'EOF'
# InBoost AI Proxy Configuration (~/.inboost/config.yaml)
# https://inboost.pro/ai-proxy
server:
  host: '127.0.0.1'
  port: 8080

agent: 'claude-code'

# ==============================================================================
# Upstream Models Configuration (L1 Fast / L2 Deep)
# ==============================================================================
# Здесь задаются модели под уровни L1 и L2:
#   L1 (fast) - быстрая модель для чтения файлов, поиска и первичного анализа.
#   L2 (deep) - глубокая модель рассуждений для генерации хирургических патчей.

upstream:
  fast:
    name: 'Fast (L1)'
    provider_format: 'anthropic'
    base_url: 'https://api.anthropic.com/v1'
    model: 'claude-3-7-sonnet-20250219'
    api_key: '${ANTHROPIC_API_KEY}'
    timeout_sec: 60.0
  deep:
    name: 'Deep (L2)'
    provider_format: 'anthropic'
    base_url: 'https://api.anthropic.com/v1'
    model: 'claude-3-7-sonnet-20250219'
    api_key: '${ANTHROPIC_API_KEY}'
    timeout_sec: 120.0

arbiter:
  enforce_diff_budget: true
  enforce_inspection_gate: true
  enforce_loop_breaker: true

optimizer:
  enable_cache_aligner: true
  enable_smart_crusher: true
  crush_threshold_bytes: 256
  enable_synthetic_loopback: true
  enable_kv_lease: true
  kv_lease_ttl_sec: 180.0
EOF
    fi
  fi

  # ----------------------------------------------------------------------------
  # Provision IDE Skills
  # ----------------------------------------------------------------------------
  mkdir -p "${HOME}/.inboost/skills" "${HOME}/.claude/skills" 2>/dev/null || true
  if [ -n "$SCRIPT_DIR" ] && [ -d "${SCRIPT_DIR}/skills" ]; then
    cp -r "${SCRIPT_DIR}/skills/"* "${HOME}/.inboost/skills/" 2>/dev/null || true
    if [ -d "${SCRIPT_DIR}/skills/inboost-proxy" ]; then
      mkdir -p "${HOME}/.claude/skills/inboost-proxy"
      cp -r "${SCRIPT_DIR}/skills/inboost-proxy/"* "${HOME}/.claude/skills/inboost-proxy/" 2>/dev/null || true
    fi
  fi

  # ----------------------------------------------------------------------------
  # Auto-Start on Login Query & Configuration
  # ----------------------------------------------------------------------------
  AUTOSTART_ENABLED=1
  if [ -t 0 ] && [ -z "${INBOOST_AUTOSTART_ON_LOGIN:-}" ]; then
    echo ""
    read -r -p "Запускать InBoost Proxy автоматически при входе в систему (при логине)? [Y/n]: " USER_AUTOSTART_REPLY || USER_AUTOSTART_REPLY="y"
    case "${USER_AUTOSTART_REPLY}" in
      [nN][oO]|[nN]) AUTOSTART_ENABLED=0 ;;
      *) AUTOSTART_ENABLED=1 ;;
    esac
  else
    AUTOSTART_ENABLED="${INBOOST_AUTOSTART_ON_LOGIN:-1}"
  fi

  if [ "$AUTOSTART_ENABLED" = "1" ] || [ "$AUTOSTART_ENABLED" = "true" ]; then
    echo -e "Configuring automatic startup on login..."

    # 1. Systemd user service (for systemd-managed Linux environments)
    SYSTEMD_USER_DIR="${HOME}/.config/systemd/user"
    if mkdir -p "$SYSTEMD_USER_DIR" 2>/dev/null; then
      cat > "${SYSTEMD_USER_DIR}/inboost-proxy.service" << EOF
[Unit]
Description=InBoost AI Proxy Daemon
After=network.target

[Service]
Type=simple
ExecStart=${TARGET_BIN} --config ${DEFAULT_CONFIG} --port ${PROXY_PORT}
Restart=always
RestartSec=3s
Environment=PATH=${INSTALL_DIR}:/usr/local/bin:/usr/bin:/bin

[Install]
WantedBy=default.target
EOF
      if command -v systemctl >/dev/null 2>&1; then
        systemctl --user daemon-reload >/dev/null 2>&1 || true
        systemctl --user enable inboost-proxy.service >/dev/null 2>&1 || true
      fi
    fi

    # 2. Resilient Shell Login Hook (~/.profile, ~/.bashrc)
    LOGIN_HOOK="
# InBoost AI Proxy autostart on login
if ! curl -s -m 1 http://127.0.0.1:${PROXY_PORT}/health >/dev/null 2>&1; then
  if [ -x \"${TARGET_BIN}\" ]; then
    nohup \"${TARGET_BIN}\" --config \"${DEFAULT_CONFIG}\" --port ${PROXY_PORT} > \"${LOG_FILE}\" 2>&1 &
  fi
fi"

    for RC_FILE in "${HOME}/.profile" "${HOME}/.bashrc"; do
      if [ -f "$RC_FILE" ] && ! grep -q "InBoost AI Proxy autostart on login" "$RC_FILE" 2>/dev/null; then
        echo "$LOGIN_HOOK" >> "$RC_FILE"
      fi
    done
    echo -e "${COLOR_GREEN}✓ InBoost Proxy autostart on login configured!${COLOR_RESET}"
  fi

  # ----------------------------------------------------------------------------
  # Auto-Start: Launch InBoost Proxy Daemon in background & Verify Health
  # ----------------------------------------------------------------------------
  if curl -s -m 1 "http://127.0.0.1:${PROXY_PORT}/health" >/dev/null 2>&1; then
    echo -e "\n${COLOR_GREEN}✓ InBoost Proxy is already running on http://127.0.0.1:${PROXY_PORT}${COLOR_RESET}"
  else
    echo -e "\nStarting ${COLOR_CYAN}InBoost AI Proxy${COLOR_RESET} daemon on port ${PROXY_PORT} with config ${DEFAULT_CONFIG}..."
    nohup "$TARGET_BIN" --config "$DEFAULT_CONFIG" --port "$PROXY_PORT" > "$LOG_FILE" 2>&1 &
    PROXY_PID=$!
    echo "$PROXY_PID" > "$PID_FILE"

    echo -n "Waiting for proxy to become ready..."
    READY=0
    for i in {1..25}; do
      if curl -s -m 1 "http://127.0.0.1:${PROXY_PORT}/health" >/dev/null 2>&1; then
        READY=1
        break
      fi
      echo -n "."
      sleep 0.2
    done
    echo ""

    if [ "$READY" -eq 1 ]; then
      echo -e "${COLOR_GREEN}✓ InBoost Proxy daemon is RUNNING and HEALTHY!${COLOR_RESET}"
      echo -e "  PID:          ${COLOR_CYAN}${PROXY_PID}${COLOR_RESET} (saved to ${PID_FILE})"
      echo -e "  Log:          ${COLOR_CYAN}${LOG_FILE}${COLOR_RESET}"
      echo -e "  Config:       ${COLOR_CYAN}${DEFAULT_CONFIG}${COLOR_RESET}"
      echo -e "  Endpoint:     ${COLOR_CYAN}http://127.0.0.1:${PROXY_PORT}${COLOR_RESET}"
      echo -e "  Health Check: ${COLOR_CYAN}http://127.0.0.1:${PROXY_PORT}/health${COLOR_RESET}"
    else
      echo -e "${COLOR_YELLOW}Notice: Proxy was launched (PID ${PROXY_PID}). Initializing in background...${COLOR_RESET}"
      echo -e "Check status: curl -s http://127.0.0.1:${PROXY_PORT}/health"
      echo -e "Log file:     ${LOG_FILE}"
    fi
  fi

  echo -e "\n${COLOR_CYAN}┌────────────────────────────────────────────────────────┐${COLOR_RESET}"
  echo -e "${COLOR_CYAN}│  InBoost AI Proxy & Claude Code Quickstart             │${COLOR_RESET}"
  echo -e "${COLOR_CYAN}└────────────────────────────────────────────────────────┘${COLOR_RESET}"
  echo -e "📁 Конфигурация:  ${COLOR_CYAN}${DEFAULT_CONFIG}${COLOR_RESET} (Anthropic Claude 3.7)"
  echo -e "   • Профиль SiliconFlow: ${COLOR_CYAN}${SILICONFLOW_CONFIG}${COLOR_RESET}"
  echo -e "   • Модели L1 (быстрая) и L2 (глубокая) настраиваются в секциях:"
  echo -e "     - ${COLOR_GREEN}upstream.fast.model${COLOR_RESET} (L1: exploration / speed)"
  echo -e "     - ${COLOR_GREEN}upstream.deep.model${COLOR_RESET} (L2: deep reasoning / patch synthesis)"
  echo -e "\n1. Запустите Claude Code (прокси уже подключен через ~/.bashrc):"
  echo -e "   ${COLOR_GREEN}export ANTHROPIC_BASE_URL=\"http://127.0.0.1:${PROXY_PORT}\"${COLOR_RESET}"
  echo -e "   ${COLOR_GREEN}export ANTHROPIC_API_KEY=\"your-api-key\"${COLOR_RESET}"
  echo -e "   ${COLOR_GREEN}export CLAUDE_CODE_AUTO_MODE_SERVER=0${COLOR_RESET}"
  echo -e "   ${COLOR_GREEN}claude${COLOR_RESET}"
  echo -e "\n2. Проверка статуса и здоровья демона:"
  echo -e "   ${COLOR_CYAN}inboost-proxy status${COLOR_RESET} (or: curl -s http://127.0.0.1:${PROXY_PORT}/health)"
  echo -e "\n3. Управление фоновым демоном и автозапуском:"
  echo -e "   • Перезапуск в фоне:   ${COLOR_GREEN}inboost-proxy start -d${COLOR_RESET}"
  echo -e "   • Остановка прокси:    ${COLOR_YELLOW}inboost-proxy stop${COLOR_RESET}"
  echo -e "   • Управление сервисом: ${COLOR_CYAN}inboost-proxy service install${COLOR_RESET} / ${COLOR_YELLOW}service uninstall${COLOR_RESET}"
  echo -e "\nДокументация и портал: ${COLOR_GREEN}https://inboost.pro/ai-proxy${COLOR_RESET}"
  echo -e "GitHub репозиторий:   ${COLOR_CYAN}https://github.com/${GITHUB_REPO}${COLOR_RESET}"
  exit 0
else
  echo -e "\n${COLOR_RED}✗ Installation could not be completed.${COLOR_RED}"
  echo -e "Supported platforms: macOS (Apple Silicon arm64 / Intel x86_64), Linux (x86_64 / arm64)."
  echo -e "Please ensure you have network access or install via Python/Node:"
  echo -e "  - Direct release: https://github.com/${GITHUB_REPO}/releases"
  echo -e "  - Node.js:        npm install -g inboost-ai-proxy"
  echo -e "  - Python:         pipx install inboost-ai-proxy"
  echo -e "\nFor assistance, file an issue at: https://github.com/${GITHUB_REPO}/issues"
  exit 1
fi

