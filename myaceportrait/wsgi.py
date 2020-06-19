"""
WSGI config for myaceportrait project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os, sys
from django.core.wsgi import get_wsgi_application

#path = '/root/myACEportrait/myaceportrait'
#if path not in sys.path:
#	sys.path.append(path)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'myaceportrait.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

application = get_wsgi_application()
