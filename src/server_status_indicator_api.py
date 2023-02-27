import json
import subprocess
import os
import sys


from flask import Flask, jsonify, request

TOKEN = os.environ.get("API_TOKEN", None)
SERVICES_FILE_PATH = '/etc/server-status-indicator-api/services.json'


def create_app():
    """Service Status indicator API"""
    app = Flask(__name__)

    if not TOKEN:
        print("API_TOKEN environment variable not set")
        sys.exit(1)

    @app.route('/services')
    def services():
        # Check if is an authenticated request
        token = request.headers.get('Authorization')
        if token != f'Token {TOKEN}':
            return jsonify({'error': 'Unauthorized access'}), 401

        # Read the list of services and their check scripts
        services_file = SERVICES_FILE_PATH
        with open(services_file, encoding='utf-8') as file:
            services = json.load(file)

        data = []
        for service in services:
            check_script = service['check-script']

            # Execute the check script and get the service status
            try:
                status = subprocess.check_output(
                    ['bash', check_script]).decode('utf-8').strip().splitlines()[-1]
                data.append({'name': service['name'], 'status': status})
            except:
                print('Invalid script output')

        # Return the list of services along with there status
        return jsonify(data)

    return app


if __name__ == '__main__':
    create_app().run()
