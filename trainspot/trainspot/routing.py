from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from trainspot import consumers

application = ProtocolTypeRouter(
    {
        'websocket': URLRouter(
            [
                path('ws/signaling/', consumers.SignalingConsumer.as_asgi()),
            ]
        ),
    }
)