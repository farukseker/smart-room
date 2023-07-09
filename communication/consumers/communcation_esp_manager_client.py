import json
import time

from asgiref.sync import async_to_sync,sync_to_async
from channels.generic.websocket import WebsocketConsumer,AsyncJsonWebsocketConsumer
from channels.db import SyncToAsync,database_sync_to_async,DatabaseSyncToAsync
from channels.exceptions import DenyConnection,RequestAborted
from esp.models import ESP
from esp.models import Key
import asyncio


class CommunicationEspManagerClientConsumer(AsyncJsonWebsocketConsumer):

    @database_sync_to_async
    def get_esp_device(self):
        try:
            return ESP.objects.get(esp_id=self.room_name)
        except:
            pass

    @database_sync_to_async
    def set_sync_key_status(self, esp_device: ESP):
        for key in esp_device.get_keys():
            key.last_updater_is_esp = False
            key.save()

    # @database_sync_to_async
    # def set_esp_connect_status(self, device, status: bool):
    #     device.is_connected = status
    #     device.save()

    async def connect(self):
        try:
            # user = self.scope["user"]
            esp_id = self.scope['url_route']['kwargs'].get("esp_id", None)
            # vid = await self.verify_esp_id(esp_id)
            self.room_name = esp_id
            self.room_group_name = "communication_%s" % self.room_name

            await self.channel_layer.group_add(
                self.room_group_name, self.channel_name
            )

            await self.accept()
            esp_device = await self.get_esp_device()
            await self.set_esp_connect_status(esp_device, True)
            await self.set_sync_key_status(esp_device)
        except Exception as er:
            print(er)

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

        esp_device = await self.get_esp_device()
        await self.set_esp_connect_status(esp_device, False)

    # Receive message from WebSocket
    async def receive(self, *args, **kwargs):
        print(args, kwargs)
        if data := kwargs.get('text_data', None):
            data = json.loads(data)

            print(data)
            await self.channel_layer.group_send(
                # self.room_group_name, {"type": "communication_message", "message": args[0]}
                # self.room_group_name, {"type": "set_master_key", "pin": "LAMBA_PIN", "status": True}
                self.room_group_name, data
            )
            # await self.channel_layer.group_send(
            #     # self.room_group_name, {"type": "communication_message", "message": args[0]}
            #     self.room_group_name, kwargsw
            # )
