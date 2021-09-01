# from channels import include
#
# # The channel routing defines what channels get handled by what consumers,
# # including optional matching on message attributes. In this example, we match
# # on a path prefix, and then include routing from the chat module.
# channel_routing = [
#     # Include sub-routing from an app.
#     include("chatbot_tutorial.sub_routing.websocket_routing", path=r"^/chat/stream"),
#
#     # Custom handler for message sending (see Room.send_message).
#     # Can't go in the include above as it's not got a `path` attribute to match on.
#     include("chatbot_tutorial.sub_routing.custom_routing"),
#
#     # A default "http.request" route is always inserted by Django at the end of the routing list
#     # that routes all unmatched HTTP requests to the Django view system. If you want lower-level
#     # HTTP handling - e.g. long-polling - you can do it here and route by path, and let the rest
#     # fall through to normal views.
# ]

from django.urls import re_path
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
import judge.routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                judge.routing.websocket_urlpatterns
            )
        )
    ),
})