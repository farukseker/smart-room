from rest_framework import serializers
from esp.models import ESP, Key


class KeySerializer(serializers.ModelSerializer):
    class Meta:
        model = Key
        fields = '__all__'


class KeyCurrentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Key
        fields = ('current', )


class EspSerializer(serializers.ModelSerializer):
    keys = KeySerializer(many=True)

    class Meta:
        model = ESP
        fields = '__all__'
