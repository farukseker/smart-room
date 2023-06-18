from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework import status
from esp.models import ESP, Key
from mobil_service.api.serializers import EspSerializer, KeySerializer, KeyCurrentSerializer


class ESPListView(ListAPIView):
    serializer_class = EspSerializer

    def get_queryset(self):
        user = self.request.user
        return ESP.objects.filter(user=user)


class KeyView(UpdateAPIView):
    serializer_class = KeyCurrentSerializer
    lookup_field = 'pk'
    queryset = Key

    def put(self, request, *args, **kwargs):
        return super().put(request, args, kwargs)

