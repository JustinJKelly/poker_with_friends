# mysite/routing.py
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import poker.routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': 
        URLRouter(
            poker.routing.websocket_urlpatterns
        )
})