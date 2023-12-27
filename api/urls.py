from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('auth/', include("Auth.api.urls")),
    path('esp/', include("esp.api.urls")),
    path('ws/', include("communication.api.urls")),
]
