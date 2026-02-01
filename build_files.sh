#!/bin/bash

echo "Installing dependencies..."
if [ -f requirements-vercel.txt ]; then
    pip install -r requirements-vercel.txt
else
    pip install -r requirements.txt
fi

echo "Running migrations..."
python manage.py migrate --noinput

echo "Loading initial data..."
python manage.py loaddata datadabse.json || echo "Data already loaded or file not found"

echo "Setting up social auth..."
python setup_social_auth.py || echo "Social auth setup skipped"

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Build completed!"
