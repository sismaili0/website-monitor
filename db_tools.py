import sqlite3
from datetime import datetime, timezone

def initialize_db():
    conn = sqlite3.connect('website_monitor.db', timeout=5)
    cursor = conn.cursor()

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS websites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                url TEXT UNIQUE NOT NULL,
                frequency INTEGER NOT NULL DEFAULT 60
            )
    ''')

        # Create ping_logs table for storing results
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS ping_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                website_id INTEGER NOT NULL,
                status TEXT,
                response_time REAL,
                requested_at TEXT,
                FOREIGN KEY (website_id) REFERENCES websites (id)
            )
    ''')
    conn.commit()
    conn.close()

#TODO Check later what happends if same url is entered again (prob. error)
def add_website(name, url, frequency):
    conn = sqlite3.connect('website_monitor.db', timeout=5)
    cursor = conn.cursor()
    cursor.execute(
        f"INSERT INTO websites (name, url, frequency) VALUES (?, ?, ?)", 
        (name, url, frequency)
    )
    conn.commit()
    conn.close()

#Log the ping with website_id, response status, time and timestamp
def log_availability(url, status, response_time):
    conn = sqlite3.connect('website_monitor.db', timeout=5)
    cursor = conn.cursor()
     # Get website_id from websites table
    cursor.execute("SELECT id FROM websites WHERE url = ?", (url,))
    row = cursor.fetchone()
    if row is None:
        conn.close()
        return

    website_id = row[0]
    requested_at = datetime.now(timezone.utc).isoformat()

    # Insert into ping_logs
    cursor.execute(
        """
        INSERT INTO ping_logs (website_id, status, response_time, requested_at) 
        VALUES (?, ?, ?, ?)
        """,
        (website_id, status, response_time, requested_at)
    )

    conn.commit()
    conn.close()

# Helps refresh the data when new entrys
def get_user_entered_data():
    conn = sqlite3.connect('website_monitor.db', timeout=5)

    cursor = conn.cursor()
    cursor.execute("SELECT name, url, frequency FROM websites")
    rows = cursor.fetchall()
    
    websites = [{"name": row[0], "url": row[1], "frequency": row[2], "current_status" : get_website_current_status(row[1])} for row in rows]
    
    conn.close()
    return websites

#Status gets updated every time the homepage is reloaded or a new user data is entered (WebSocket could solve real time update)
def get_website_current_status(url):
    conn = sqlite3.connect('website_monitor.db', timeout=5)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM websites WHERE url = ?", (url,))
    row = cursor.fetchone()
    if row is None:
        return "no data"

    website_id = row[0]

    cursor.execute(
        """
        SELECT status FROM ping_logs 
        WHERE website_id = ? 
        ORDER BY requested_at DESC 
        LIMIT 1
        """,
        (website_id,)
    )
    last_status_row = cursor.fetchone()

    conn.close()

    if last_status_row is None:
        return "no data"

    last_status = last_status_row[0]

    if last_status == "200":
        return "online"
    else:
        return "warning"

#Delete the website and all its logs
def delete_website(url):
    conn = sqlite3.connect('website_monitor.db', timeout=5)
    cursor = conn.cursor()

    # Find website id for the given URL
    cursor.execute('SELECT id FROM websites WHERE url = ?', (url,))
    result = cursor.fetchone()

    if result:
        website_id = result[0]
        cursor.execute('DELETE FROM ping_logs WHERE website_id = ?', (website_id,))
        cursor.execute('DELETE FROM websites WHERE id = ?', (website_id,))
        conn.commit()
    
    conn.close()

#Get all logs of the given URL
def get_log_of_website(url):
    conn = sqlite3.connect('website_monitor.db', timeout=5)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM websites WHERE url = ?", (url,))
    row = cursor.fetchone()
    if not row:
        logs = []
    else:
        website_id = row[0]
        # Fetch ping logs for the website
        cursor.execute("SELECT status, response_time, requested_at FROM ping_logs WHERE website_id = ?", (website_id,))
        logs = cursor.fetchall()
    conn.close()

    return logs

#Calculate website availability (available = 1xx/2xx/3xx Status Code), avarage response time, total checks and current status
def get_website_availability_stats(url):
    conn = sqlite3.connect('website_monitor.db', timeout=5)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM websites WHERE url = ?", (url,))
    row = cursor.fetchone()
    if not row:
        logs = []
        success_ratio = 0
        average_response_time = 0
        website_name = None
    else:
        website_id, website_name = row
        cursor.execute("SELECT status, response_time, requested_at FROM ping_logs WHERE website_id = ?", (website_id,))
        logs = cursor.fetchall()

        success_count = sum(1 for log in logs if str(log[0]).startswith('1') or str(log[0]).startswith('2') or str(log[0]).startswith('3'))
        total_count = len(logs)
        success_ratio = str(round((success_count / total_count) * 100, 4)) + "%" if total_count > 0 else 0

        if total_count > 0:
            total_response_time = sum(log[1] for log in logs if log[1] is not None)
            average_response_time = round(total_response_time / total_count, 4)
        else:
            average_response_time = 0

    conn.close()
    current_status = get_website_current_status(url)

    return success_ratio, website_name, average_response_time, current_status, total_count
