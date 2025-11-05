import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db_tools import initialize_db, add_website, get_log_of_website
from pinger import ping

def pinger_test():
    initialize_db()

    test_name = "Website"
    test_url = "https://website.com"
    test_frequency = 10

    add_website(test_name, test_url, test_frequency)

    ping(test_url)

    logs = get_log_of_website(test_url)
    if not logs:
        print("Warning: No logs found for", test_url)
    else:
        print(f"Logs found: {len(logs)} entries")

if __name__ == "__main__":
    pinger_test()
