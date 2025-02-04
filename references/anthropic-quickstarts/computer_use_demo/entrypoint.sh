#!/bin/bash

# Start monitoring if enabled
if [ "$ENABLE_MONITORING" = "true" ]; then
    echo "Starting monitoring services..."
    python -c "from prometheus_client import start_http_server; start_http_server($PROMETHEUS_PORT)" &
fi

# Start X server
Xvfb :$DISPLAY_NUM -screen 0 ${WIDTH}x${HEIGHT}x24 &
export DISPLAY=:$DISPLAY_NUM

# Wait for X server to start
sleep 1

# Start window manager
mutter --sm-disable --replace --x11 &

# Start noVNC
/opt/noVNC/utils/novnc_proxy --vnc localhost:5900 --listen 6080 &

# Start VNC server
x11vnc -display :$DISPLAY_NUM -nopw -listen localhost -xkb -forever &

# Start tint2 panel
tint2 &

# Keep container running
tail -f /dev/null
