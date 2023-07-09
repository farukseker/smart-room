import json
import time

from asgiref.sync import async_to_sync,sync_to_async
from channels.generic.websocket import WebsocketConsumer,AsyncJsonWebsocketConsumer
from channels.db import SyncToAsync,database_sync_to_async,DatabaseSyncToAsync
from channels.exceptions import DenyConnection,RequestAborted
from esp.models import ESP
from esp.models import Key
import asyncio
from esp.api.serializers import EspSerializer


class CommunicationEspManagerClientConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        try:
            user = self.scope["user"]
            print("connect")
            if user.is_authenticated:
                self.room_name = str(self.scope["user"].username) + '_' + str(self.scope["user"].id)
                print("mrb3")

                self.room_group_name = "communication_%s" % self.room_name

                print("mrb2")

                await self.channel_layer.group_add(
                    self.room_group_name, self.channel_name
                )
                await self.accept()
                print("mrb")
                await self.send_esp_device_list()
                print("con ok")
        except Exception as er:
            print('er')
            print(er)

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    async def send_hello_esp(self):
        await self.send(text_data=json.dumps({"message": "hi ESP!"}))

    @database_sync_to_async
    def get_esp_device_list(self) -> list[dict]:
        user = self.scope["user"]
        return [EspSerializer(esp).data for esp in ESP.objects.filter(user=user)]

    async def send_esp_device_list(self):
        esp_list = await self.get_esp_device_list()

        data = {"type": "esp_sync", "esp_list": esp_list}
        print(data)
        return await self.send(text_data=json.dumps(data))

    # Receive message from WebSocket
    async def receive(self, *args, **kwargs):
        print(args, kwargs)
        if data := kwargs.get('text_data', None):
            data = json.loads(data)

            await self.channel_layer.group_send(
                self.room_group_name, data
            )

