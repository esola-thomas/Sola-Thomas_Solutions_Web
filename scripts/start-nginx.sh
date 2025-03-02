#!/bin/bash

# Start Nginx service
sudo service nginx start

# Check if Nginx started correctly
if sudo service nginx status > /dev/null; then
    echo "Nginx started successfully"
else
    echo "Failed to start Nginx"
    exit 1
fi

# Keep script running to keep container alive
tail -f /dev/null
