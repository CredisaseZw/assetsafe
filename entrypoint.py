#!/usr/bin/env python3
import os
import socket
import sys
import time
from subprocess import run, PIPE
from urllib.parse import urlparse


def get_db_host():
    if os.getenv('DEVELOPMENT','false').lower() == 'false':
        if production_db_host := os.getenv('PRODUCTION_DATABASE_URL'):
            parsed = urlparse(production_db_host)
            return parsed.hostname.replace('-pooler', ''), parsed.port or 5432
    return os.getenv('DB_HOST'), os.getenv('DB_PORT', 5432)
    
def db_ready():
    """Check if the database is ready to accept connections."""
    db_host , db_port = get_db_host()
    
    if not db_host or not db_port:
        print("Error: DB_HOST or DB_PORT environment variables are not set.")
        return False
    
    print(f"Waiting for database connection at {db_host}:{db_port}...")
    
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((db_host, int(db_port)))
            sock.close()
            if result == 0:
                print("Database is ready!")
                return True
        except Exception as e:
            print(f"Database connection error: {e}")
        time.sleep(1)

def create_superuser():
    """Create a superuser if it doesn't exist."""
    print("Creating superuser 'admin' if it does not exist...")
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        if not User.objects.filter(email='admin@admin.com').exists():
            User.objects.create_superuser('admin', 'admin@admin.com', 'admin')
            print("Superuser created.")
        else:
            print("Superuser already exists.")
    except Exception as e:
        print(f"Error creating superuser: {e}")

def check_seeding_needed():
    """Check if database seeding is needed."""
    print("Checking if seeding is needed...")
    try:
        from apps.common.models.models import Country

        if Country.objects.exists():
            print(f"Country table contains {Country.objects.count()} records - skipping seeding")
        else:
            print("Country table is empty - running seeding script...")
            seed_script = "/app/seed_db.sh"
            dos2unix_cmd = "dos2unix /app/seed_db.sh"
            if os.path.exists(seed_script):
                run([dos2unix_cmd], check=True, shell=True)
                run([seed_script], check=True, shell=True)
            else:
                print(f"Seed script not found at {seed_script}")
    except Exception as e:
        print(f"Error checking Country table: {e}")

def main():
    if "gunicorn" in sys.argv:
        # Wait for database
        db_ready()
        
        # Apply database migrations
        print("Applying database migrations...")
        run(["python", "manage.py", "migrate", "--noinput"], check=True)
        
        # Create superuser
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
        import django
        django.setup()
        
        create_superuser()
        check_seeding_needed()
        
        # Collect static files
        print("Collecting static files...")
        run(["python", "manage.py", "collectstatic", "--noinput"], check=True)
    
    # Execute the command passed to the script
    if len(sys.argv) > 1:
        os.execvp(sys.argv[1], sys.argv[1:])
    else:
        print("No command provided.")
        sys.exit(1)

if __name__ == "__main__":
    main()
