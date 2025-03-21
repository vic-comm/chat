"""
ASGI config for djangochat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
import django
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import rooms.routing
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangochat.settings")
django.setup()
application = ProtocolTypeRouter({
    'http':get_asgi_application(),
    'websocket':AuthMiddlewareStack(
        URLRouter(rooms.routing.websocket_urlpatterns)
    ),
})