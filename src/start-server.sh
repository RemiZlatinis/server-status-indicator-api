#!/bin/bash

if ! command -v flask &> /dev/null; then
    echo "Flask is not installed."
    exit 1
fi

if ! command -v gunicorn &> /dev/null; then
    echo "Gunicorn is not installed."
    exit 1
fi

cd /etc/server-status-indicator-api/
export API_TOKEN=$(cat .token) 
export DATABASE_UPDATE_MIN_INTERVAL=$(cat .min_interval) 
gunicorn -b 0.0.0.0:{PORT} wsgi:app --log-level=info --log-file=/var/log/gunicorn.log
