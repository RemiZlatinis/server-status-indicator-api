#!/bin/bash

if ! command -v flask &> /dev/null; then
    echo "Flask is not installed. Installing..."
    pip3 install flask
fi

if ! command -v gunicorn &> /dev/null; then
    echo "Gunicorn is not installed. Installing..."
    pip3 install gunicorn
fi

cd /etc/server-status-indicator-api/
export API_TOKEN=$(cat .token) 
gunicorn -b 0.0.0.0:{PORT} wsgi:app --log-level=info --log-file=/var/log/gunicorn.log
