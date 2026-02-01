"""
Vercel build script - runs after dependencies are installed
"""
import os
import subprocess

def run_command(cmd):
    """Run a shell command and print output"""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result.returncode

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom.settings')

# Run migrations
print("=" * 50)
print("Running migrations...")
run_command("python manage.py migrate --noinput")

# Load data
print("=" * 50)
print("Loading initial data...")
run_command("python manage.py loaddata datadabse.json")

# Setup social auth
print("=" * 50)
print("Setting up social auth...")
run_command("python setup_social_auth.py")

# Collect static files
print("=" * 50)
print("Collecting static files...")
run_command("python manage.py collectstatic --noinput --clear")

print("=" * 50)
print("Build completed successfully!")
