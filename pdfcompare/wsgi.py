import os
from django.core.wsgi import get_wsgi_application

# Use production settings for Vercel
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pdfcompare.settings')

application = get_wsgi_application()

# Vercel serverless function handler
app = application
