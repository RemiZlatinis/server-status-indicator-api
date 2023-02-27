#!/bin/bash

# Determine the package manager
if [ -x "$(command -v pacman -h)" ]; then
    # Arch-based distribution
    PM="pacman"
elif [ -x "$(command -v apt-get)" ]; then
    # Debian-based distribution
    PM="apt-get"
else
    echo "Unsupported distribution."
    exit 1
fi

# Refresh the package list
sudo $PM update 2>&1

# Get the number of available updates
if [ $PM = "pacman" ]; then
    NUM_UPDATES=$(sudo pacman -Qu | wc -l)
else
    NUM_UPDATES=$(sudo apt-get -s upgrade | grep -c ^Inst)
fi

# If there are no updates available, exit the script
if [ $NUM_UPDATES -eq 0 ]; then
    echo "ok"
    exit 0
fi
echo "update"
