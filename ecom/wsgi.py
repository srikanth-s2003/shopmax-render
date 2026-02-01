"""
WSGI config for ecom project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path

# Add the project directory to Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecom.settings")

# Run one-time setup on cold start
def setup_database():
    """Initialize database on first run"""
    from django.core.management import execute_from_command_line
    try:
        # Run migrations
        execute_from_command_line(['manage.py', 'migrate', '--noinput'])
        # Load initial data
        execute_from_command_line(['manage.py', 'loaddata', 'datadabse.json'])
        # Setup social auth
        import subprocess
        subprocess.run([sys.executable, 'setup_social_auth.py'], check=False)
    except Exception as e:
        print(f"Setup error (may be expected): {e}")

# Only run setup once
if not os.environ.get('VERCEL_SETUP_DONE'):
    setup_database()
    os.environ['VERCEL_SETUP_DONE'] = '1'

application = get_wsgi_application()

# Vercel requires 'app' variable
app = application
