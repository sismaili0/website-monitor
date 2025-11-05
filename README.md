# website-monitor

## Description

This project is a website monitoring tool that periodically sends HTTP GET requests (pings) to user-specified URLs at defined intervals. Each check is stored in a database, enabling users to view detailed insights including availability percentage, average response time, current status, total checks performed, and a complete log history.

The logs are displayed in a filterable table, allowing users to easily analyze performance and uptime data for any monitored website.

## Usage
1. Create and activate an environment:
 ``` bash
 python -m venv venv
 source venv/bin/activate
```

2. Install dependencies:
 ``` bash
 pip install -r requirements.txt
```

3. Run the Flask app: 
``` bash
 python app.py
```