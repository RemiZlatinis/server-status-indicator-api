#!/bin/bash

# Check for root privileges 
if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root" 
    exit 1
fi

systemctl disable --now server-status-indicator-api.service
rm -r /etc/server-status-indicator-api/
