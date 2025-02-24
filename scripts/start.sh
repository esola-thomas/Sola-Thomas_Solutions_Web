#!/bin/bash

# Create logs directories with timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RUNNER_LOG_DIR="/home/esolathomas/out/runner_logs"
mkdir -p ${RUNNER_LOG_DIR}
mkdir -p /home/esolathomas/out
chmod 755 /home/esolathomas/out
touch /home/esolathomas/out/django.log
chmod 666 /home/esolathomas/out/django.log

# Create Django logs
mkdir -p /home/esolathomas/ws/sola_thomas_website/logs
touch /home/esolathomas/ws/sola_thomas_website/logs/django.log
chmod 666 /home/esolathomas/ws/sola_thomas_website/logs/django.log

# Activate the virtual environment
source /home/esolathomas/stsol/bin/activate

# Start gunicorn in the foreground
cd /home/esolathomas/ws/sola_thomas_website
exec gunicorn \
    --pid /home/esolathomas/gunicorn.pid \
    --bind 0.0.0.0:8000 \
    --workers 1 \
    --worker-class sync \
    --worker-connections 100 \
    --timeout 120 \
    --keep-alive 5 \
    --max-requests 200 \
    --max-requests-jitter 50 \
    --log-level info \
    --access-logfile - \
    --error-logfile - \
    --capture-output \
    sola_thomas_website.wsgi:application