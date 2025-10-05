import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing  # Make sure this exists

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobportal_project.settings')

application = ProtocolTypeRouter({
    # Handles normal HTTP requests
    "http": get_asgi_application(),

    # Handles WebSocket connections for chat
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
