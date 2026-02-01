#!/usr/bin/env python
"""
Script to set up Google OAuth for django-allauth
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom.settings')
django.setup()

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

# Update or create the site
site, created = Site.objects.get_or_create(
    id=1,
    defaults={
        'domain': '127.0.0.1:8000',
        'name': 'localhost'
    }
)
if not created:
    site.domain = '127.0.0.1:8000'
    site.name = 'localhost'
    site.save()
print(f'Site {"created" if created else "updated"}: {site.domain}')

# Create Google OAuth app
app, created = SocialApp.objects.get_or_create(
    provider='google',
    defaults={
        'name': 'Google OAuth',
        'client_id': 'your-google-client-id.apps.googleusercontent.com',
        'secret': 'your-google-client-secret',
    }
)
print(f'SocialApp {"created" if created else "exists"}: {app.name}')

# Associate with site
if site not in app.sites.all():
    app.sites.add(site)
    print(f'Associated SocialApp with site: {site.domain}')
else:
    print(f'SocialApp already associated with site: {site.domain}')

print('\n✅ Setup complete!')
print('Note: Update the client_id and secret in Django admin if you have real Google OAuth credentials.')
