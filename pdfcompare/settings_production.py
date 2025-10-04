from .settings import *
import os

# Vercel-specific settings
DEBUG = False

# Update allowed hosts for Vercel
ALLOWED_HOSTS = ['.vercel.app', '.now.sh', 'localhost', '127.0.0.1']

# CORS settings for Vercel
CORS_ALLOWED_ORIGINS = [
    "https://*.vercel.app",
]

# Database - Use SQLite but note that Vercel is read-only
# For production, you should use an external database like PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/tmp/db.sqlite3',  # Temporary directory on Vercel
    }
}

# Static files configuration for Vercel
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
] if os.path.exists(os.path.join(BASE_DIR, 'static')) else []

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
