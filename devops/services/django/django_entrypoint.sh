
# This script is used to start the django wep server

##   Boot Webserver   ##

echo "Starting webserver in $1 mode"

if [ "$1" = "runserver" ]; then
    echo "Starting django webserver"
    python manage.py migrate -
    python manage.py runserver 0.0.0.0:8000

elif [ "$1" = "runserver-debug" ]; then
    echo "Starting django webserver with debug mode enabled"
    python -m pip install debugpy
    python manage.py migrate
    python -m debugpy --listen  5678 manage.py runserver 0.0.0.0:8000

elif [ "$1" = "gunicorn" ]; then
    echo "Starting gunicorn server"
    gunicorn --bind :8000 --limit-request-line 0 --workers 2 --timeout 120 --graceful-timeout 30 domestic_finance_analytics.wsgi:application
else
    echo "Invalid argument. Please specify 'runserver' or 'gunicorn'."
    echo "Switching to default: Starting gunicorn server"
    gunicorn --bind :8000 --limit-request-line 0 --workers 2 --timeout 120 --graceful-timeout 30 domestic_finance_analytics.wsgi:application
fi

echo "Webserver startup completed"