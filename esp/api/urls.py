from django.urls import path, include
from esp.api.views import ESPListView, KeyView


urlpatterns = [
    path('', ESPListView.as_view(), name="esp_list_view"),
    path('key/', KeyView.as_view(), name="esp_key_status_view"),
]

