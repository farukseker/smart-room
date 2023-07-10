from rest_framework import serializers
from esp.models import ESP, Key, SensorModel


class KeySerializer(serializers.ModelSerializer):
    class Meta:
        model = Key
        # fields = '__all__'
        exclude = ('owner_esp',)


class EspSerializer(serializers.Serializer):

    class Meta:
        model = ESP
        fields = '__all__'
        # fields = ['user', 'name', 'esp_id', 'api_key', 'keys', 'is_connected']
        read_only_fields = ['esp_id',]

    esp_id = serializers.UUIDField(format='hex', read_only=True)
    keys = KeySerializer(many=True)
    name = serializers.CharField(read_only=True)
    is_connected = serializers.BooleanField(read_only=True)
    # api_key = serializers.UUIDField(format='hex', read_only=True)