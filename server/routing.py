from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from core.consumers import DeviceConsumer

application = ProtocolTypeRouter({
    # WebSocket
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/device/", DeviceConsumer.as_asgi()),
        ])
    ),
})
