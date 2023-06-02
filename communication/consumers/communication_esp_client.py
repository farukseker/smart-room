import json
import time

from asgiref.sync import async_to_sync,sync_to_async
from channels.generic.websocket import WebsocketConsumer,AsyncJsonWebsocketConsumer
from channels.db import SyncToAsync,database_sync_to_async,DatabaseSyncToAsync
from channels.exceptions import DenyConnection,RequestAborted
from esp.models import ESP
from esp.models import Key
import asyncio


class CommunicationEspClientConsumer(AsyncJsonWebsocketConsumer):

    @database_sync_to_async
    def verify_esp_id(self,id):
        try:
            ESP.objects.get(esp_id=id)
            return True
        except:
            pass

    @database_sync_to_async
    def get_esp_device(self):
        try:
            return ESP.objects.get(esp_id=self.room_name)
        except:
            pass

    @database_sync_to_async
    def set_sync_key_status(self, esp_device: ESP):
        for key in esp_device.get_keys():
            key.save()

    @database_sync_to_async
    def set_esp_connect_status(self, device: ESP, status: bool):
        device.is_connected = status
        device.save()

    async def connect(self):
        try:
            # user = self.scope["user"]
            esp_id = self.scope['url_route']['kwargs'].get("esp_id",None)
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


    # else:
    #     raise DenyConnection

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

        esp_device = await self.get_esp_device()
        await self.set_esp_connect_status(esp_device, False)

    # Receive message from WebSocket
    async def receive(self,*args,**kwargs):
        print(args,kwargs)


        await self.channel_layer.group_send(
            # self.room_group_name, {"type": "communication_message", "message": args[0]}
            self.room_group_name, {"type": "set_master_key","pin":"LAMBA_PIN", "status": True}
        )
        # await self.channel_layer.group_send(
        #     # self.room_group_name, {"type": "communication_message", "message": args[0]}
        #     self.room_group_name, kwargs
        # )

    # Receive message from room group
    async def communication_message(self, event):
        message = event["message"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))

    async def send_hello_esp(self):
        await self.send(text_data=json.dumps({"message":"hi ESP!"}))

    async def key_status(self,*args,**kwargs):
        __dict = args[0]
        pin = __dict.get("pin",None)
        status = __dict.get("status",None)
        if pin != None and status != None:
            await self.send(text_data=json.dumps({"type": "key_update","pin":pin,"status":status}))

    async def key_status_update_from_esp(self,*args,**kwargs):
        __dict = args[0]
        pin = __dict.get("pin",None)
        status = __dict.get("status",None)
        if pin != None and status != None:
            await self.send(text_data=json.dumps({"type": "key_update","pin":pin,"status":status}))

    @database_sync_to_async
    def set_master_key(self,*args,**kwargs):
        print("set master key")
        try:

            esp_device = async_to_sync(self.get_esp_device())()
            key = esp_device.keys.get(pin_name="D3")
            # key.last_updater_is_esp = True
            key.current = False
            key.save()
        except:
            pass
            # @errlog alert type crt*2
        # await self.send(text_data=json.dumps(kwargs))
