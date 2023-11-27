#!/bin/sh

#uvicorn main:app --host 0.0.0.0 --port 8000
#gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --timeout 2000

# First, run pytest
echo "Running tests..."
pytest
TEST_EXIT_CODE=$?

#Check if tests passed (exit code 0 means success)
if [ $TEST_EXIT_CODE -ne 0 ]; then
    echo "Tests failed, exiting."
    exit $TEST_EXIT_CODE
else
    echo "Tests passed, starting the FastAPI application..."
    echo "Starting the FastAPI application with Gunicorn"
    exec gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --timeout 2000
fi