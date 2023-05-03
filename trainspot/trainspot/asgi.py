import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path

import trainspot.settings
from . import consumers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trainspot.settings')

application = get_asgi_application()