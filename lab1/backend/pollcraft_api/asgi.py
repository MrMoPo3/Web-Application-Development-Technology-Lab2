import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pollcraft_api.settings")

django_asgi_app = get_asgi_application()

from collaboration.middleware import TokenAuthMiddleware
from collaboration.routing import websocket_urlpatterns


application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": TokenAuthMiddleware(URLRouter(websocket_urlpatterns)),
    }
)
