#!/bin/bash

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python3.11 manage.py collectstatic --noinput --clear

echo "Running migrations..."
python3.11 manage.py migrate --noinput

echo "Setting up social auth..."
python3.11 setup_social_auth.py

echo "Build completed!"
