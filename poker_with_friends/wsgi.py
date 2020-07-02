"""
WSGI config for poker_with_friends project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
import django
#from whitenoise.django import DjangoWhiteNoise
from channels.routing import get_default_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poker_with_friends.settings')

django.setup()
application = get_default_application()
#application = DjangoWhiteNoise(application)

