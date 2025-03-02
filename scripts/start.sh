#!/bin/bash

# Set environment variables for deployment
export DEPLOYMENT=True
export DJANGO_SETTINGS_MODULE=sola_thomas_website.settings
export PYTHONPATH=/home/esolathomas/ws/sola_thomas_website:$PYTHONPATH

# Color codes for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

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

# Navigate to Django project
cd /home/esolathomas/ws/sola_thomas_website

# Function to test database connection
test_db_connection() {
    echo -e "${YELLOW}Testing database connection...${NC}"
    python /home/esolathomas/ws/scripts/db_check.py
    return $?
}

# Try to connect to the database, with retries
max_retries=5
retry_count=0
db_ready=false

while [ $retry_count -lt $max_retries ] && [ "$db_ready" = false ]; do
    if test_db_connection; then
        db_ready=true
    else
        retry_count=$((retry_count+1))
        echo -e "${YELLOW}Retrying database connection $retry_count/$max_retries${NC}"
        sleep 5
    fi
done

if [ "$db_ready" = false ]; then
    echo -e "${RED}Failed to connect to database after $max_retries attempts. Continuing anyway but may fail later.${NC}"
fi

# Create migrations for the clientportal app
echo -e "${YELLOW}Creating migrations for clientportal app...${NC}"
python manage.py makemigrations clientportal
MAKEMIGRATIONS_STATUS=$?

if [ $MAKEMIGRATIONS_STATUS -ne 0 ]; then
    echo -e "${RED}Failed to create migrations for clientportal app. Continuing anyway but may fail later.${NC}"
fi

# Run migrations and ensure they complete successfully
echo -e "${YELLOW}Applying database migrations...${NC}"
python manage.py migrate --no-input
MIGRATION_STATUS=$?

if [ $MIGRATION_STATUS -ne 0 ]; then
    echo -e "${RED}Database migrations failed with status $MIGRATION_STATUS. Cannot continue with superuser creation.${NC}"
    # Still continue with server startup, but skip superuser creation
else
    echo -e "${GREEN}Database migrations completed successfully.${NC}"
    
    # Verify that the auth_user table exists before creating a superuser
    echo -e "${YELLOW}Verifying database schema...${NC}"
    python -c "
import os, sys, django
sys.path.append('/home/esolathomas/ws/sola_thomas_website')
os.environ['DJANGO_SETTINGS_MODULE'] = 'sola_thomas_website.settings'
os.environ['DEPLOYMENT'] = 'True'

django.setup()

from django.db import connection

tables = connection.introspection.table_names()
if 'auth_user' in tables:
    print('${GREEN}auth_user table exists, proceeding with superuser check${NC}')
    from django.contrib.auth import get_user_model
    User = get_user_model()
    if not User.objects.filter(username='esolathomas').exists():
        print('${GREEN}Creating superuser...${NC}')
        User.objects.create_superuser('esolathomas', 'ernesto@solathomas.com', 'my_generic_passsword1234')
        print('${GREEN}Superuser created successfully!${NC}')
    else:
        print('${YELLOW}Superuser already exists, skipping creation${NC}')
else:
    print('${RED}auth_user table does not exist! Migrations may not have completed correctly.${NC}')
    exit(1)
" || echo -e "${RED}Failed to create superuser. Will continue without it.${NC}"
fi

# Collect static files with clear flag to ensure fresh copy
echo -e "${YELLOW}Collecting static files...${NC}"
python manage.py collectstatic --no-input --clear

# Start nginx
echo -e "${YELLOW}Starting Nginx...${NC}"
sudo service nginx start

echo -e "${GREEN}Starting Gunicorn server...${NC}"

# Start gunicorn in the foreground
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