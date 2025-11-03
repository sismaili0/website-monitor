import sqlite3, datetime

def initialize_db():
    conn = sqlite3.connect('website_monitor.db')
    cursor = conn.cursor()

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS websites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
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
def add_website(url, frequency):
    conn = sqlite3.connect('website_monitor.db')
    cursor = conn.cursor()
    cursor.execute(
        f"INSERT INTO websites (url, frequency) VALUES (?, ?)", 
        (url, frequency)
    )
    conn.commit()
    conn.close()

#Log the ping with website_id, response status, time and timestamp
def log_availability(url, status, response_time):
    conn = sqlite3.connect('website_monitor.db')
    cursor = conn.cursor()
     # Get website_id from websites table
    cursor.execute("SELECT id FROM websites WHERE url = ?", (url,))
    row = cursor.fetchone()
    if row is None:
        conn.close()
        return

    website_id = row[0]
    requested_at = datetime.datetime.utcnow().isoformat()

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

# Helps refresh the database when user enters new url
def get_all_websites_from_db():
    conn = sqlite3.connect('website_monitor.db')
    cursor = conn.cursor()
    cursor.execute("SELECT url, frequency FROM websites")
    rows = cursor.fetchall()
    conn.close()
    # Convert each row to a dictionary
    websites = [{"url": row[0], "frequency": row[1]} for row in rows]
    return websites

