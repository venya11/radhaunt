#!/bin/bash

# ROOT PRIV #
if [ "$EUID" -ne 0 ]; then
    echo "Error: Execute script with sudo! (sudo ./install.sh)"
    exit 1
fi

### START  ###
echo "Starting Radhaunt EDR installation..."

# PATH #
ROOT_DIRECTORY=$(pwd)
AGENT_DIR="${ROOT_DIRECTORY}/radhaunt_agent"

echo "📂 Path to agent determined as: ${ROOT_DIRECTORY}"

# CLEANUP OLD VERSION IF EXISTS #
if [ -f "/etc/systemd/system/radhaunt_agent.service" ]; then
    echo "🧹 Found old service instance. Cleaning up..."
    systemctl stop radhaunt_agent.service 2>/dev/null
    systemctl disable radhaunt_agent.service 2>/dev/null
    rm -f /etc/systemd/system/radhaunt_agent.service
    systemctl daemon-reload
    systemctl reset-failed
fi

# VENV #
echo "📦 Creating isolated Python virtual environment..."
if ! python3 -m venv --help &>/dev/null; then
    echo "❌ Error: python3-venv is not installed! Install it for your distro (details - in the README file...)"
    exit 1
fi

python3 -m venv "${ROOT_DIRECTORY}/.venv"
echo "Installing python dependencies inside venv..."

"${ROOT_DIRECTORY}/.venv/bin/pip" install --upgrade pip
"${ROOT_DIRECTORY}/.venv/bin/pip" install -r "${ROOT_DIRECTORY}/requirements.txt"
echo "Dependencies successfully installed in isolated environment."

# .ENV #
read -p "🔑 Enter your telegram bot token (from BotFather): " API_TOKEN
read -p "👤 Enter your telegram user id (check it in user_id bot): " ADMIN_ID

cat <<EOF > "${ROOT_DIRECTORY}/.env"
RADHAUNT_TELEGRAM_API_TOKEN=${API_TOKEN}
ADMIN_TELEGRAM_ID=${ADMIN_ID}
EOF

echo ".env file successfully generated."

# USER #
if ! id "radhaunt_agent" &>/dev/null; then
    echo "Creating user radhaunt_agent..."
    useradd -r -s /bin/false radhaunt_agent
else
    echo "User radhaunt_agent already exists."
fi

# .SERVICE #
echo "⚙️ Generating systemd configuration..."

cat <<EOF > /etc/systemd/system/radhaunt_agent.service
[Unit]
Description=Radhaunt EDR Telegram Agent
After=network.target

[Service]
User=radhaunt_agent
Group=radhaunt_agent
WorkingDirectory=${AGENT_DIR}
ExecStart=${ROOT_DIRECTORY}/.venv/bin/python3 ${AGENT_DIR}/main.py
Restart=always
RestartSec=5
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF

# PRIV #
echo "🔒 Configuring privileges..."
chown -R radhaunt_agent:radhaunt_agent "${ROOT_DIRECTORY}"
chmod 600 "${ROOT_DIRECTORY}/.env"
cat <<EOF > /etc/sudoers.d/radhaunt_agent
radhaunt_agent  ALL = (root) NOPASSWD: /usr/sbin/shutdown
EOF
chmod 0440 /etc/sudoers.d/radhaunt_agent

### STARTING BOT ###
echo "Activating service..."
systemctl daemon-reload
systemctl enable radhaunt_agent.service

echo "Starting Radhaunt..."
systemctl start radhaunt_agent.service
echo "✅ Installation completed! Check status with: sudo systemctl status radhaunt_agent.service"
