"""
ASGI config for poker_with_friends project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os
from channels.layers import get_channel_layer
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poker_with_friends.settings')

application = get_asgi_application()
channel_layer = get_channel_layer()
