import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django_asgi_app = get_asgi_application()

from chat.routing import websocket_urlpatterns


application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})




# import os

# from django.core.asgi import get_asgi_application

# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.sessions import SessionMiddlewareStack
# from channels.auth import AuthMiddlewareStack

# django_asgi_app = get_asgi_application()


# from chat.routing import websocket_urlpatterns



# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

# application = ProtocolTypeRouter({
#     'http': django_asgi_app,
#     'websocket': AuthMiddlewareStack(
#         URLRouter(websocket_urlpatterns)
#     )
# })

# # application = ProtocolTypeRouter({
# #     'http': get_asgi_application(),
# #     'websocket':AuthMiddlewareStack(URLRouter(routing.ASGI_urlpatterns)) 
# # })



