import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapps.settings')

import django
django.setup()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import mahjong.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            mahjong.routing.websocket_urlpatterns
        )
    ),
})