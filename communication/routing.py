from django.urls import re_path
from communication.consumers import *


websocket_urlpatterns = [
    re_path(r"ws/communication/esp/(?P<esp_id>[A-Za-z0-9_-]+)", CommunicationEspClientConsumer.as_asgi()),
    re_path(r"ws/communication/user/(?P<accesses_token>[A-Za-z0-9_-]+)", CommunicationEspManagerClientConsumer.as_asgi()),
    # re_path(r"ws/communication/user/", CommunicationEspManagerClientConsumer.as_asgi()),
    # re_path(r"ws/communication/$", communication_consumers.CommunicationConsumer.as_asgi()),
]

