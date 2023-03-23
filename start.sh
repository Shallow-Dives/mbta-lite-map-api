#!/usr/bin/env bash

# Export environment vars for testing
set -a
source .env
set +a

# Start the server
gunicorn wsgi:app --bind 0.0.0.0:8080 --log-level=debug --workers=4