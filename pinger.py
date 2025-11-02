from apscheduler.schedulers.background import BackgroundScheduler
import requests

#Send an GET request to a given URL
def ping(url):
    try:
        response = requests.get(url)
        print(f"{url} - Status: {response.status_code}")
    except Exception as e:
        print(f"Error {url}: {e}")

#Repeated pinging for given websites with specific intervals
def ping_websites(websites_list):
    scheduler = BackgroundScheduler()
    print(websites_list)
    for website in websites_list:
        scheduler.add_job(ping, 'interval', seconds=website['freq'], args=[website['url']])

    scheduler.start()

    try:
        import time
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()