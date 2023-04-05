import json

from asgiref.sync import async_to_sync,sync_to_async
from channels.generic.websocket import WebsocketConsumer,AsyncJsonWebsocketConsumer
from channels.db import SyncToAsync,database_sync_to_async,DatabaseSyncToAsync
from channels.exceptions import DenyConnection,RequestAborted
from esp.models import ESP
from esp.models import Key

class CommunicationConsumer(AsyncJsonWebsocketConsumer):

    @database_sync_to_async
    def verify_esp_id(self,id):
        try:
            ESP.objects.get(esp_id=id)
            return True
        except:
            pass

    def get_esp_device(self):
        try:
            return ESP.objects.get(esp_id=self.room_name)
        except:
            pass

    async def connect(self):
        print("connnect talp edildi".upper())
        user = self.scope["user"]
        print(self)
        # print(self.scope["url_route"]["kwargs"])

        esp_id = self.scope['url_route']['kwargs'].get("esp_id",None)

        vid = self.verify_esp_id(esp_id)
        if vid:
            self.room_name = esp_id
            self.room_group_name = "communication_%s" % self.room_name

            await self.channel_layer.group_add(
                self.room_group_name, self.channel_name
            )



            await self.accept()
        else:
            raise DenyConnection
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self,*args,**kwargs):
        print(args,kwargs)
        __type = kwargs.get('type',None)

        await self.channel_layer.group_send(
            # self.room_group_name, {"type": "communication_message", "message": args[0]}
            self.room_group_name, {"type": "set_master_key","pin":"LAMBA_PIN", "status": True}
        )

    # Receive message from room group
    async def communication_message(self, event):
        message = event["message"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))

    async def send_hello_esp(self):
        await self.send(text_data=json.dumps({"message":"hi ESP!"}))


    async def key_status(self,*args,**kwargs):
        print("key statusssss".upper())

    @database_sync_to_async
    def set_master_key(self,*args,**kwargs):
        print("geldiii ****")
        try:
            esp_device = self.get_esp_device()
            key = esp_device.keys.get(pin_name="D3")
            key.last_updater_is_esp = True
            key.current = False
            key.save()
        except:
            pass
            # errlog alert type crtical
        # await self.send(text_data=json.dumps(kwargs))

