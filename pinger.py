import requests, sqlite3, datetime, time
from db_tools import *

#Send an GET request to a given URL
def ping(url):
    try:
        response = requests.get(url)
        response_time = response.elapsed.total_seconds()
        log_availability(url, response.status_code, response_time)
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        print(url, current_time)
    except Exception as e:
        print(f"Error {url}: {e}")

#Repeated pinging for given websites with specific frequency
def ping_websites():
    websites = get_all_websites_from_db()
    next_pings = {w["url"]: time.time() for w in websites}

    while True:
        now = time.time()

        # Refresh list every 10 seconds
        if int(now) % 10 == 0:
            websites = get_all_websites_from_db()
            for w in websites:
                if w["url"] not in next_pings:
                    next_pings[w["url"]] = now

        for w in websites:
            if now >= next_pings[w["url"]]:
                ping(w["url"])
                next_pings[w["url"]] = now + w["frequency"]

        time.sleep(0.5)