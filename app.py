from flask import Flask, render_template
from redis import Redis
import os

app = Flask(__name__)
# Technical Note: 'redis' is the HOST name. 
# Docker Compose will map this name to the database container automatically.
redis = Redis(host='redis', port=6379)

@app.route('/')
def home():
    # Increment the counter in Redis
    hits = redis.incr('hits')
    
    project_team = [
        {"name": "Alice", "role": "Developer", "status": "Active"},
        {"name": "Bob", "role": "Designer", "status": "Away"}
    ]
    
    return render_template('index.html', team=project_team, count=hits)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
