from django.db import models
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class ESP(models.Model):
    name = models.TextField()
    api_key = models.TextField(default=None,null=True)


class Key(models.Model):
    boss_esp = models.ForeignKey("ESP",on_delete=models.CASCADE,default=None)
    name = models.TextField()
    current = models.BooleanField(default=False)
