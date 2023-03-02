import sqlite3

DATABASE = 'services.db'

# Initialize the database
try:
    _conn = sqlite3.connect(DATABASE)
    _c = _conn.cursor()
    _c.execute('''CREATE TABLE services (name text, status text)''')
    _conn.commit()
    _conn.close()
except sqlite3.OperationalError as e:
    print(f"Error on database initialize: {e}")


def save_services(services: dict):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM services")
        for service in services:
            name = service['name']
            status = service['status']
            conn.execute(
                "INSERT INTO services (name, status) VALUES (?, ?)", (name, status))
        conn.commit()
    except:
        print(f"Error on save services")
    finally:
        conn.close()


def get_services() -> dict:
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT name, status FROM services")
    rows = cursor.fetchall()
    services = {}
    for row in rows:
        name, status = row
        services[name] = status
    conn.close()
    return services
