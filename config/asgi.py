# ASGI

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

# Ortam değişkenini belirterek Django ayarlarını yükle.
# Bu, Uvicorn'un ayarlar dosyanızı bulmasını sağlar.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.product")

# Django'nun varsayılan ASGI uygulamasını başlat.
django_asgi_app = get_asgi_application()

# WebSocket yönlendirme dosyanızı içe aktar.
from communication import routing

# Protokol tiplerine göre yönlendirme yapısını kur.
# HTTP istekleri Django'nun varsayılan uygulamasına giderken,
# WebSocket istekleri AuthMiddlewareStack ile korunarak yönlendirilir.
application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AuthMiddlewareStack(
            URLRouter(routing.websocket_urlpatterns)
        ),
    }
)
