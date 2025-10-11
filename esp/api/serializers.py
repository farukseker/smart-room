from rest_framework import serializers
from esp.models import ESP, Key, SensorModel


class KeySerializer(serializers.ModelSerializer):
    class Meta:
        model = Key
        # fields = '__all__'
        exclude = ('owner_esp',)


class EspSerializer(serializers.ModelSerializer):
    keys = KeySerializer(many=True, read_only=True)

    class Meta:
        model = ESP
        fields = ['esp_id', 'name', 'keys', 'is_connected']
        read_only_fields = ['esp_id', 'is_connected']