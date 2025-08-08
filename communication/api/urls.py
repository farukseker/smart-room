from django.urls import path
from .views import AccessesRequestView, send_discord


urlpatterns = [
    path('socket_accesses/', AccessesRequestView.as_view(), name='accesses_request'),
    path("temp-hook", send_discord, name="send_discord")
]

