This project demonstrates a containerized Python Flask web application integrated with a Redis database. It is designed to show proficiency in Docker orchestration, production-grade web serving with Gunicorn, and state management in a microservices environment.
Language: Python 3.9

Tool used:
Framework: Flask
Production Server: Gunicorn
Database: Redis (NoSQL)
Orchestration: Docker & Docker Compose

app.py: A Python Flask backend that includes a resilient retry mechanism. If the Redis container isn't ready immediately on startup, the app won't crash; it waits and retries.

Dockerfile: Built using python:3.9-slim to minimize the attack surface and image footprint. I optimized the build by copying requirements.txt first to leverage Docker Layer Caching.

docker-compose.yaml: Manages the bridge network and service discovery, alowing the Web tier to communicate with the Data tier using simple hostnames.

requirements.txt: Defined Python dependencies for environment consistency.

templates/ & static/: Directory structure for frontend rendering and asset management.
1. Application Architecture & Resilience
The core of this project is a Python Flask application designed with cloud-native principles in mind.

State Management: I integrated Redis as a high-performance, in-memory data store to handle the visitor counter, moving away from static delivery to a dynamic, stateful application.

Resilience Logic: Recognizing that distributed systems often face startup race conditions, I implemented a custom retry loop in app.py. This ensures the web tier waits for the Redis service to become healthy rather than failing on the first connection attempt.

2. Dependency Management
To ensure environment parity across different stages of development, all dependencies are strictly defined in requirements.txt:

Flask & Redis: Core framework and database drivers.

Gunicorn: Included as a production-grade WSGI server, replacing the Flask development server for better handling of concurrent requests.

3. Optimized Containerization
The Dockerfile was crafted following industry best practices for security and speed:

Base Image: Utilized python:3.9-slim to significantly reduce the attack surface and final image size.

Layer Caching: I structured the build to copy requirements.txt and install dependencies before copying the source code. This tactical placement utilizes Docker Layer Caching, drastically reducing rebuild times during code updates.

Production Entrypoint: The container is configured to boot directly into Gunicorn, ensuring the app is "production-ready" out of the box.

4. Multi-Service Orchestration
Using Docker Compose, I managed the lifecycle of both the Web and Database tiers as a unified stack.

Service Discovery: I established a bridge network that enables the Flask app to resolve the Redis instance via its service name (redis), eliminating the need for hardcoded IP addresses.

Workflow Automation: The entire environment—including networking and volume mounting—is automated through a single docker-compose up --build command.
5. Version Control & Repository Hygiene
Git Management: I utilized a .gitignore to maintain a clean workspace, specifically excluding Python artifacts (__pycache__) and runtime system files (like the gunicorn.ctl socket
. Handling Runtime Artifacts (gunicorn.ctl)
The Issue: While attempting to push the project to GitHub, I encountered a fatal error: error: open("gunicorn.ctl"): Function not implemented. This was caused by Gunicorn creating a Unix domain socket file within the working directory.

The Insight: Git is designed to track source code, not active system sockets or runtime artifacts.

The Resolution: I implemented a robust .gitignore strategy to exclude gunicorn.ctl, __pycache__, and other ephemeral files. This ensured a clean repository and prevented environment-specific system files from interfering with version control.

2. Startup Race Conditions (Service Dependencies)
The Issue: In a distributed environment, the Web container often starts faster than the Redis database container, leading to immediate connection failures.

The Resolution: Instead of relying solely on Docker Compose's depends_on, I implemented a Python-level retry loop with exponential backoff. This makes the application "self-healing," as it gracefully waits for the database to be healthy before attempting to serve traffic.

3. Environment Parity (Windows vs. Linux)
The Issue: Moving between Git Bash (Windows) and the Linux-based Docker containers often causes line-ending issues (LF vs. CRLF).

The Resolution: I configured Git to handle line-ending conversions automatically, ensuring that scripts remain executable inside the Linux container regardless of the host OS.
