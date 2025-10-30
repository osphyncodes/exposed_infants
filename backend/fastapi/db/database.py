# main.py
# fastapi/db/database.py
import os
import django

# Adjust this to your Django settings path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()
