from flask import Flask, render_template, request
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from pinger import ping_websites

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

#Currently printing the responses from a single website
@app.route('/status', methods=['POST'])
def status():
    temp_website_dict = dict()
    temp_website_dict["url"] = request.form.get('url')
    temp_website_dict["freq"] = int(request.form.get('frequency'))
    ping_websites([temp_website_dict])

if __name__ == '__main__':
    app.run(debug=True)