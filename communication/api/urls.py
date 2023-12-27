from django.urls import path
from .views import AccessesRequestView


urlpatterns = [
    path('socket_accesses/', AccessesRequestView.as_view(), name='accesses_request'),
]

