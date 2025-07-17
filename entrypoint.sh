#!/bin/sh

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL..."
while ! nc -z db 5432; do
    sleep 0.1
done
echo "PostgreSQL is ready!"

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Create superuser if not exists
echo "Creating superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='${DJANGO_SUPERUSER_USERNAME:-admin}').exists():
    User.objects.create_superuser('${DJANGO_SUPERUSER_USERNAME:-admin}', '${DJANGO_SUPERUSER_EMAIL:-admin@example.com}', '${DJANGO_SUPERUSER_PASSWORD:-admin}')
"

# Create or update the production site
echo "Setting up site configuration..."
python manage.py shell -c "
from django.contrib.sites.models import Site;
Site.objects.update_or_create(
    id=4,
    defaults={
        'domain': 'shopmax-render.onrender.com',
        'name': 'Production'
    }
)
"

# Set up Google OAuth
echo "Setting up Google OAuth..."
python manage.py shell -c "
from allauth.socialaccount.models import SocialApp;
from django.contrib.sites.models import Site;

# Delete all existing social apps
SocialApp.objects.all().delete()

# Create new social app
app = SocialApp.objects.create(
    provider='google',
    name='google',
    client_id='${GOOGLE_CLIENT_ID}',
    secret='${GOOGLE_CLIENT_SECRET}'
)

# Add the production site
production_site = Site.objects.get(id=4)
app.sites.add(production_site)
"

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start server
echo "Starting server..."
gunicorn ecom.wsgi:application --bind 0.0.0.0:8000 