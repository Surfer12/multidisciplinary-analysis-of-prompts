#!/bin/bash

# Kill any existing Xvfb processes
pkill Xvfb || true

# Start Xvfb with specific display and screen configuration
Xvfb :1 -screen 0 1920x1080x24 &

# Wait for Xvfb to start
sleep 1

# Start VNC server for debugging if needed
x11vnc -display :1 -nopw -listen localhost -xkb -forever &
