"""
WSGI config for drf_server project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drf_server.settings')

application = get_wsgi_application()

os.environ['SECRET_KEY'] = 'django-insecure-f=lwn+2gad%(3dsd^#pm+a&q0$5+dlegyf#%0bd#8s@i_nx108'