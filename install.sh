#!/bin/bash

# Check for root privileges 
if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root" 
    exit 1
fi

cp -p -r ./src/ /etc/server-status-indicator-api/

# Generate a key
key=$(openssl rand -base64 50 | tr -dc 'a-zA-Z0-9!@#$%^&*(-_=+)' | head -c50)

echo $key > /etc/server-status-indicator-api/.token

ln -s /etc/server-status-indicator-api/server-status-indicator-api.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now server-status-indicator-api.service

echo "This will be your TOKEN: "
echo $key