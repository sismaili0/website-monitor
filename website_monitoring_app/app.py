from flask import Flask, render_template, request
import sys, os, threading
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from pinger import ping_websites, add_website
from db_tools import initialize_db

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        add_website(request.form['url'], request.form['frequency'])
    return render_template('home.html')

if __name__ == '__main__':
    initialize_db()
    threading.Thread(target=ping_websites, daemon=True).start()
    app.run(debug=True, use_reloader=False)