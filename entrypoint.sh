#!/bin/sh

echo "🔁 Skipping wait-for-Postgres — assuming Supabase is live..."

# Apply database migrations
echo "🚀 Applying database migrations..."
python manage.py migrate --noinput

# Create superuser if it doesn't exist
echo "👤 Creating superuser if not exists..."
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='${DJANGO_SUPERUSER_USERNAME:-admin}').exists():
    User.objects.create_superuser(
        '${DJANGO_SUPERUSER_USERNAME:-admin}',
        '${DJANGO_SUPERUSER_EMAIL:-admin@example.com}',
        '${DJANGO_SUPERUSER_PASSWORD:-admin}'
    )
"

# Set up the production Site object
echo "🌐 Configuring Site object..."
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

# Set up Google OAuth SocialApp
echo "🔐 Setting up Google OAuth SocialApp..."
python manage.py shell -c "
from allauth.socialaccount.models import SocialApp;
from django.contrib.sites.models import Site;

SocialApp.objects.all().delete()

google_app = SocialApp.objects.create(
    provider='google',
    name='Google',
    client_id='${SOCIAL_AUTH_GOOGLE_OAUTH2_KEY}',
    secret='${SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET}'
)

site = Site.objects.get(id=4)
google_app.sites.add(site)
"

# Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

# Start Gunicorn server
echo "🚀 Starting Gunicorn server..."
gunicorn ecom.wsgi:application --bind 0.0.0.0:8000
