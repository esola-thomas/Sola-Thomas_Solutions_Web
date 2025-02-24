#!/bin/bash

# Function to terminate GitHub Actions Runner
terminate_runner() {
    echo "Terminating GitHub Actions Runner..."
    if [ -f ~/actions-runner.pid ]; then
        RUNNER_PID=$(cat ~/actions-runner.pid)
        echo "Shutting down runner process ${RUNNER_PID} at $(date)" >> $(ls -t /home/esolathomas/out/runner_logs/runner_*.log | head -1)
        if [ -f /home/esolathomas/actions-runner/.runner ]; then
            cd /home/esolathomas/actions-runner
            ./config.sh remove --token "${RUNNER_TOKEN}"
        fi
        kill ${RUNNER_PID} 2>/dev/null || true
    fi
    
    # Kill any remaining runner processes
    pkill -f actions-runner
    pkill -f Runner.Worker
    
    # Wait for processes to terminate
    sleep 5
    
    # Force kill if still running
    pkill -9 -f actions-runner
    pkill -9 -f Runner.Worker
}

# Function to terminate Gunicorn
terminate_gunicorn() {
    echo "Terminating Gunicorn..."
    if [ -f /home/esolathomas/gunicorn.pid ]; then
        kill -TERM $(cat /home/esolathomas/gunicorn.pid) 2>/dev/null || true
    fi
    pkill -f gunicorn
}

# Main shutdown sequence
echo "Starting graceful shutdown..."
terminate_runner
terminate_gunicorn
echo "Shutdown complete"
