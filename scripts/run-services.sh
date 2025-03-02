#!/bin/bash

# Start Nginx
echo "Starting Nginx..."
sudo service nginx start

# Start Django/Gunicorn in the background
echo "Starting Gunicorn..."
cd /home/esolathomas/ws/sola_thomas_website
source /home/esolathomas/stsol/bin/activate
gunicorn \
    --pid /home/esolathomas/gunicorn.pid \
    --bind 0.0.0.0:8000 \
    --workers 1 \
    --daemon \
    sola_thomas_website.wsgi:application

# Keep container running and monitor services
echo "All services started, monitoring..."
while true; do
    sleep 10
    # Check if nginx is running
    if ! pgrep -x "nginx" > /dev/null; then
        echo "Nginx stopped, restarting..."
        sudo service nginx start
    fi
    
    # Check if gunicorn is running
    if ! pgrep -x "gunicorn" > /dev/null; then
        echo "Gunicorn stopped, restarting..."
        cd /home/esolathomas/ws/sola_thomas_website
        source /home/esolathomas/stsol/bin/activate
        gunicorn \
            --pid /home/esolathomas/gunicorn.pid \
            --bind 0.0.0.0:8000 \
            --workers 1 \
            --daemon \
            sola_thomas_website.wsgi:application
    fi
done
