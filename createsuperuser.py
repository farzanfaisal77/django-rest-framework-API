import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Pull secrets securely from the environment, use safe defaults for local testing
username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "farzan")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "farzanfaisal77@gmail.com")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "admin123")

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f"Superuser '{username}' created successfully!")
else:
    print(f"Superuser '{username}' already exists.")