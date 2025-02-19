if ! command -v curl &> /dev/null; then
    echo "curl command not found, cannot perform health check."
    exit 1
fi

local_check=false
prod_check=false

if curl -s http://localhost:8000/health/ > /dev/null; then
    echo "Application is running successfully (Local)"
    local_check=true
fi

sleep 5

if curl -s http://new.solathomas.com/health/ > /dev/null; then
    echo "Application is running successfully (Production)"
    prod_check=true
fi

if [ "$local_check" = true ] && [ "$prod_check" = true ]; then
    echo "Both endpoints are accessible"
elif [ "$local_check" = true ]; then
    echo "Only Local endpoint (localhost:8000) is accessible"
elif [ "$prod_check" = true ]; then
    echo "Only Production endpoint (new.solathomas.com) is accessible"
else
    echo "Both endpoints failed to respond"
    exit 1
fi

exit 0