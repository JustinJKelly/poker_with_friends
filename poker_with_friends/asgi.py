"""
ASGI config for poker_with_friends project.
It exposes the ASGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

#localhost
'''import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poker_with_friends.settings')

application = get_asgi_application()'''

#prodcution
import os
#import django
#from channels.routing import get_default_application
from django.core.asgi import get_asgi_application
#from channels.layers import get_channel_layer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poker_with_friends.settings')

#django.setup()
#channel_layer = get_channel_layer()
#application = get_default_application()
application = get_asgi_application()