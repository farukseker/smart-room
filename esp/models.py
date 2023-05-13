from django.db import models
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model

import uuid

user_model = get_user_model()


class ESP(models.Model):
    user = models.ForeignKey(user_model,on_delete=models.CASCADE,default=None,blank=True,null=True)
    name = models.TextField()
    esp_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    api_key = models.UUIDField(default=uuid.uuid4, editable=True)
    keys = models.ManyToManyField("Key",blank=True,default=None)
    is_connected = models.BooleanField(default=False)

    def get_keys(self):
        return self.keys.all()

    def __str__(self):
        return f"{self.name}|{self.esp_id}"


class Key(models.Model):
    owner_esp = models.ForeignKey("ESP",on_delete=models.CASCADE,default=None,blank=True,null=True)
    pin_name = models.TextField(default="")
    name = models.TextField()
    current = models.BooleanField(default=False)
    last_updater_is_esp = models.BooleanField(default=False)

    def __str__(self):
        return f"key : {self.name}|{self.pin_name} @ {self.owner_esp}"


class Mood(models.Model):
    name = models.TextField()

