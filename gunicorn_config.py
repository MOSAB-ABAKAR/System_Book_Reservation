# Gunicorn configuration for BookStore Flask app

# Bind to address and port
bind = "0.0.0.0:8000"

# Number of worker processes
workers = 4

# Worker class (sync is fine for most Flask apps)
worker_class = "sync"

# Timeout for worker processes (seconds)
timeout = 120

# Maximum requests a worker can handle before restart
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Preload app for better memory efficiency with fork()
preload_app = True
