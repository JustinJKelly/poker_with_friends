# mysite/routing.py
from channels.auth import AuthMiddlewareStack
from django.contrib.auth.middleware import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import poker.routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            poker.routing.websocket_urlpatterns
        )
    ),
})