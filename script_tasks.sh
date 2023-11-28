#!/bin/bash
# source ve2/bin/activate &
# Start the Redis server (Replace the path with the correct one if necessary)
redis-server &
# Start the Celery worker (Assuming your Celery tasks are defined in tasks.py)
celery -A run.celery worker -B --loglevel=info &&
# Start the Celery Beat scheduler (Assuming your Celery tasks are defined in tasks.py)
# celery -A folder1.celery beat --loglevel=info

celery -A run.celery worker --loglevel=info
