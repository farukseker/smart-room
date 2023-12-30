import json
from asgiref.sync import async_to_sync,sync_to_async
from channels.generic.websocket import WebsocketConsumer, AsyncJsonWebsocketConsumer
from channels.db import SyncToAsync,database_sync_to_async, DatabaseSyncToAsync
from datetime import datetime
from channels.exceptions import DenyConnection, RequestAborted
from django.contrib.auth.models import AnonymousUser

from esp.models import ESP
from esp.models import Key
import asyncio
from esp.api.serializers import EspSerializer
from rest_framework.authtoken.models import Token
from communication.models import WebSocketConsumerAccessesModel


class CommunicationEspManagerClientConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.socket_accesses_token = None

    async def get_session(self, accesses_token):
        @sync_to_async()
        def wrapper():
            accesses = WebSocketConsumerAccessesModel.objects.filter(accesses_token=accesses_token).first()
            if accesses and accesses.user.is_active:
                return accesses.user
        return await wrapper()

    async def remove_session(self, accesses_token):
        @sync_to_async()
        def wrapper():
            (
             WebSocketConsumerAccessesModel
             .objects.filter(accesses_token=accesses_token)
             .first().delete()
             )
        return await wrapper()


    async def change_key_status_request(self, *args, **kwargs):
        user = self.scope["user"]

        @sync_to_async
        def wrapper():
            key = Key.objects.filter(id=args[0].get('key_id')).first()
            if ESP.objects.filter(user=user, key=key).first():
                key.set_current(args[0].get('status'))

        return await wrapper()

    async def connect(self):
        try:
            accesses_token = self.scope['url_route']['kwargs'].get("accesses_token", None)
            if session_user := await self.get_session(accesses_token):
                self.socket_accesses_token = accesses_token
                self.scope['user'] = session_user
                self.room_name = str(self.scope["user"].username) + '_' + str(self.scope["user"].id)
                self.room_group_name = "communication_%s" % self.room_name

                await self.channel_layer.group_add(
                    self.room_group_name, self.channel_name
                )
                await self.accept()
                await self.send_esp_device_list()
        except Exception as er:
            print('er')
            print(er)

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )
        await self.remove_session(self.socket_accesses_token)

    async def send_hello_esp(self):
        await self.send(text_data=json.dumps({"message": "hi ESP!"}))

    @database_sync_to_async
    def get_esp_device_list(self):  # -> list[dict]
        user = self.scope["user"]
        return [EspSerializer(esp).data for esp in ESP.objects.filter(user=user).order_by('name')]

    async def send_esp_device_list(self, *args, **kwargs):
        esp_list = await self.get_esp_device_list()
        data = {"type": "esp_sync", "esp_list": esp_list}
        return await self.send(text_data=json.dumps(data))

    # Receive message from WebSocket
    async def receive(self, *args, **kwargs):
        if data := kwargs.get('text_data', None):
            data = json.loads(data)

            await self.channel_layer.group_send(
                self.room_group_name, data
            )