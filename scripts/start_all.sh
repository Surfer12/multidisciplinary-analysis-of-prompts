#!/bin/bash

# Start Xvfb
./start_xvfb.sh &

# Wait for Xvfb to start
sleep 2

# Start window manager
DISPLAY=:1 tint2 &

# Start Streamlit application
streamlit run computer_use_demo/streamlit.py --server.port=8501 --server.address=0.0.0.0
