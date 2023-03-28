import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer,AsyncJsonWebsocketConsumer


class CommunicationConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)

    def connect(self):
        user = self.scope["user"]
        # user
        self.room_name = user.username
        self.room_group_name = "communication_%s" % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self,*args,**kwargs):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "communication_message", "message": args[0]}
        )

    # Receive message from room group
    def communication_message(self, event):
        message = event["message"]
        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))