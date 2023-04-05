from django.db import models
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import uuid


class ESP(models.Model):
    name = models.TextField()
    esp_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    api_key = models.UUIDField(default=uuid.uuid4, editable=True)
    keys = models.ManyToManyField("Key",blank=True,default=None)
    def __str__(self):
        return f"{self.name}|{self.esp_id}"


class Key(models.Model):
    owner_esp = models.ForeignKey("ESP",on_delete=models.CASCADE,default=None,blank=True,null=True)
    pin_name = models.TextField(default="")
    name = models.TextField()
    current = models.BooleanField(default=False)
    last_updater_is_esp = models.BooleanField(default=False)
