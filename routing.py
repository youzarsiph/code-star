""" CodeStar Routing Configuration """

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.handlers.asgi import ASGIHandler
from django.urls import path

from code_star.chats.consumers import ChatConsumer
from code_star.completions.consumers import CompletionConsumer


# Create your routing here.
def app(application: ASGIHandler) -> ProtocolTypeRouter:
    """Setup routing"""

    return ProtocolTypeRouter(
        {
            "http": application,
            "websocket": AllowedHostsOriginValidator(
                AuthMiddlewareStack(
                    URLRouter(
                        [
                            path("ws/chats/<int:pk>/", ChatConsumer.as_asgi()),
                            path("ws/completions/", CompletionConsumer.as_asgi()),
                        ]
                    )
                )
            ),
        }
    )
