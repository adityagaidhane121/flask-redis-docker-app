from flask import Flask, render_template
from redis import Redis
import time
from functools import wraps

app = Flask(__name__)

# 1. Custom Retry Decorator with Exponential Backoff
def retry_with_backoff(max_retries=5, initial_delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"[Attempt {attempt}/{max_retries}] Redis not ready yet: {e}")
                    if attempt == max_retries:
                        print("Max retries reached. Application failing safely.")
                        raise e
                    print(f"Retrying connection in {delay} seconds...")
                    time.sleep(delay)
                    delay *= 2  # Exponential backoff logic
        return wrapper
    return decorator

# 2. Wrapped Connection Logic to eliminate Docker container startup race conditions
@retry_with_backoff(max_retries=5, initial_delay=1)
def connect_to_redis():
    # 'redis' is the service hostname mapped automatically by Docker Compose
    client = Redis(host='redis', port=6379)
    client.ping()  # Forces a connection test to trigger the retry layer if needed
    return client

# Initialize the resilient connection layer
redis = connect_to_redis()

@app.route('/')
def home():
    # Increment the persistent hit counter in Redis
    hits = redis.incr('hits')
    
    # Customized project team context
    project_team = [
        {"name": "Aditya", "role": "Cloud & DevOps Engineer", "status": "Active"},
        {"name": "Ajay", "role": "Backend Developer", "status": "Active"}
    ]
    
    return render_template('index.html', team=project_team, count=hits)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
