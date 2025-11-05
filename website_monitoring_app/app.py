from flask import Flask, render_template, request, redirect, url_for
import sys, os, threading
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from pinger import ping_websites, add_website
from db_tools import *

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            add_website(request.form.get('website_name'), request.form.get('url'), request.form.get('frequency'))
        except sqlite3.IntegrityError:
            print("Warning, you might have entered the URL of a currently under monitor website")
        return redirect(url_for('home'))
    
    user_entered_data = get_user_entered_data()
    return render_template('home.html', urls = user_entered_data)

@app.route('/status', methods=['GET', 'POST'])
def status_of_website():
    if request.method == 'POST':
        selected_url = request.form.get('website_url')
    else:
        selected_url = request.args.get('website_url')
    log_of_website = get_log_of_website(selected_url)
    website_availability, website_name, average_response_time, current_status, total_count = get_website_availability_stats(selected_url)
    return render_template('status.html', url = selected_url, log_of_website = log_of_website, 
                           website_availability = website_availability, website_name=website_name,
                             average_response_time = average_response_time, current_status = current_status, total_count = total_count )

@app.route('/delete', methods=['POST'])
def delete_monitored_website():
    url = request.form.get('website_url')
    delete_website(url)
    return redirect(url_for('home')) 

if __name__ == '__main__':
    initialize_db()
    threading.Thread(target=ping_websites, daemon=True).start()
    app.run(debug=False, use_reloader=False)