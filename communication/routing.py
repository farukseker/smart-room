from django.urls import re_path,path


from communication import consumers as communication_consumers
websocket_urlpatterns = [
    re_path(r"ws/communication/esp/(?P<esp_id>[A-Za-z0-9_-]+)", communication_consumers.CommunicationConsumer.as_asgi()),
    # re_path(r"ws/communication/$", communication_consumers.CommunicationConsumer.as_asgi()),
]