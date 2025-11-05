import requests, sqlite3, datetime, time
from db_tools import *

#Send an GET request to a given URL
def ping(url):
    try:
        response = requests.get(url)
        response_time = response.elapsed.total_seconds()
        log_availability(url, response.status_code, response_time)
    except Exception as e:
        print(f"Error {url}: {e}")
        log_availability(url, 0, 0.0)

#Repeated pinging for given websites with specific frequency
def ping_websites():
    websites = get_user_entered_data()
    next_pings = {website["url"]: time.time() for website in websites}

    while True:
        now = time.time()

        # Refresh list every 10 seconds
        if int(now) % 10 == 0:
            websites = get_user_entered_data()
            for website in websites:
                if website["url"] not in next_pings:
                    next_pings[website["url"]] = now

        for website in websites:
            if now >= next_pings[website["url"]]:
                ping(website["url"])
                next_pings[website["url"]] = now + website["frequency"]

        time.sleep(0.5)