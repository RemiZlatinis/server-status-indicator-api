import json
import subprocess
import threading
import time

from database import save_services


def update_database(service_filepath):
    """
    Runs all the check scripts from the given service file
    and updates the database.
    """
    print("updating the database")

    # Read the list of services and their check scripts
    services_file = service_filepath
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

    # Updates the list of services along with there status in database
    save_services(data)
    print("update finished.")


def schedule_task(interval: float, task, *args):
    """
    Runs the given function in loop and waits
    [interval] seconds between each execution.
    """
    def task_wrapper():
        while True:
            task(*args)
            time.sleep(interval)

    thread = threading.Thread(target=task_wrapper)
    thread.daemon = True
    thread.start()
