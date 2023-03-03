import os
import sys


from flask import Flask, jsonify, request


from database import get_services
from scheduler import schedule_task, update_database

TOKEN = os.environ.get("API_TOKEN", None)
DATABASE_UPDATE_MIN_INTERVAL = int(os.environ.get(
    "DATABASE_UPDATE_MIN_INTERVAL", 60))
SERVICES_FILE_PATH = '/etc/server-status-indicator-api/services.json'


def create_app():
    """Service Status indicator API"""
    app = Flask(__name__)

    if not TOKEN:
        print("API_TOKEN environment variable not set")
        sys.exit(1)

    print("Initialize scheduler")
    # Creates a scheduler to periodically update the services status
    schedule_task(DATABASE_UPDATE_MIN_INTERVAL,
                  update_database, SERVICES_FILE_PATH)

    print("Listening")

    @app.route('/services')
    def services():
        # Check if is an authenticated request
        token = request.headers.get('Authorization')
        if token != f'Token {TOKEN}':
            return jsonify({'error': 'Unauthorized access'}), 401

        # Return the list of services along with there status
        return jsonify(get_services())

    return app


if __name__ == '__main__':
    create_app().run()
