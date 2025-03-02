#!/bin/bash

# Set environment variable for deploymentt
export DEPLOYMENT=True
export DJANGO_SETTINGS_MODULE=sola_thomas_website.settings
# Create logs directories with timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)imestamp
RUNNER_LOG_DIR="/home/esolathomas/out/runner_logs"
mkdir -p ${RUNNER_LOG_DIR}athomas/out/runner_logs"
mkdir -p /home/esolathomas/out
chmod 755 /home/esolathomas/out
touch /home/esolathomas/out/django.log
chmod 666 /home/esolathomas/out/django.log
chmod 666 /home/esolathomas/out/django.log
# Create Django logs
mkdir -p /home/esolathomas/ws/sola_thomas_website/logs
touch /home/esolathomas/ws/sola_thomas_website/logs/django.log
chmod 666 /home/esolathomas/ws/sola_thomas_website/logs/django.log
chmod 666 /home/esolathomas/ws/sola_thomas_website/logs/django.log
# Activate the virtual environment
source /home/esolathomas/stsol/bin/activate
source /home/esolathomas/stsol/bin/activate
# Color codes for output
GREEN='\033[0;32m'output
RED='\033[0;31m'm'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color
NC='\033[0m' # No Color
# Navigate to Django project
cd /home/esolathomas/ws/sola_thomas_website
cd /home/esolathomas/ws/sola_thomas_website
# Function to test database connection
test_db_connection() {abase connection
    echo -e "${YELLOW}Testing database connection...${NC}"
    python /home/esolathomas/ws/scripts/db_check.pyYELLOW}Testing database connection...${NC}"
    return $?n -c "
}

# Try to connect to the database, with retries
max_retries=5LE'] = 'sola_thomas_website.settings'
retry_count=0
db_ready=falseproperly

while [ $retry_count -lt $max_retries ] && [ "$db_ready" = false ]; do
    if test_db_connection; thenconnection
        db_ready=true
    else.db.utils import OperationalError
        retry_count=$((retry_count+1))
        echo -e "${YELLOW}Retrying database connection ($retry_count/$max_retries)${NC}"
        sleep 5   db_conn = connections['default']
    fi    db_conn.cursor()
doneful${NC}')

if [ "$db_ready" = false ]; thenionalError as e:
    echo -e "${RED}Failed to connect to database after $max_retries attempts. Continuing anyway but may fail later.${NC}"ED}Database connection failed: %s${NC}' % str(e))
fi    exit(1)

# Run migrations regardless of connection test result' % str(e))
echo -e "${YELLOW}Applying database migrations...${NC}"
python manage.py migrate --no-input

# Create superuser if it doesn't exist
echo -e "${YELLOW}Checking superuser...${NC}"
python -c "to connect to the database, with retries
from django.contrib.auth import get_user_modelretries=5
User = get_user_model()retry_count=0
if not User.objects.filter(username='esolathomas').exists():
    print('${GREEN}Creating superuser...${NC}')
    User.objects.create_superuser('esolathomas', 'ernesto@solathomas.com', 'my_generic_passsword1234')ile [ $retry_count -lt $max_retries ] && [ "$db_ready" = false ]; do
    print('${GREEN}Superuser created successfully!${NC}')    if test_db_connection; then
else:
    print('${YELLOW}Superuser already exists, skipping creation${NC}')
"1))
        echo -e "${YELLOW}Retrying database connection ($retry_count/$max_retries)${NC}"
# Collect static files
echo -e "${YELLOW}Collecting static files...${NC}"
python manage.py collectstatic --no-input

echo -e "${GREEN}Starting Gunicorn server...${NC}"e ]; then
retries attempts. Continuing anyway but may fail later.${NC}"
# Start gunicorn in the foreground
exec gunicorn \
    --pid /home/esolathomas/gunicorn.pid \
    --bind 0.0.0.0:8000 \-e "${YELLOW}Applying database migrations...${NC}"
    --workers 1 \
    --worker-class sync \
    --worker-connections 100 \# Create superuser if it doesn't exist
    --timeout 120 \king superuser...${NC}"
    --keep-alive 5 \
    --max-requests 200 \
    --max-requests-jitter 50 \import django
    --log-level info \
    --access-logfile - \os.environ['DJANGO_SETTINGS_MODULE'] = 'sola_thomas_website.settings'
    --error-logfile - \
    --capture-output \ango properly
    sola_thomas_website.wsgi:applicationpython manage.py collectstatic --no-input

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