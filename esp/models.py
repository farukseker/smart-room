from django.db import models
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from datetime import datetime, time

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
    # time_range = models.ForeignKey('TimeRanger', blank=True, default=None, null=True,on_delete=models.SET_NULL)
    use_time_range = models.BooleanField(default=False)
    start_time = models.TimeField(default=None, null=True)
    end_time = models.TimeField(default=None, null=True)

    # Convert the time argument to a datetime object
    def now_in_time_range(self):


        right_now = datetime.now()
        # Convert start_time and end_time to datetime objects
        start_time_obj = datetime.combine(datetime.now(), self.start_time)
        end_time_obj = datetime.combine(datetime.now(), self.end_time)
        # Check if time_obj is within the range
        if start_time_obj > end_time_obj:
            return end_time_obj.hour <= right_now.hour <= start_time_obj.hour
        else:
            return start_time_obj.hour <= right_now.hour <= end_time_obj.hour

    def __str__(self):
        return f"key : {self.name}|{self.pin_name} @ {self.owner_esp}"

    def save(self, *args, **kwargs):
        print(self)
        print(args)
        print(kwargs)
        if self.use_time_range:
            pass


class TimeRanger(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    def now_in_time_range(self):
        # Convert the time argument to a datetime object
        right_now = datetime.now()
        # Convert start_time and end_time to datetime objects
        start_time_obj = datetime.combine(datetime.now(), self.start_time)
        end_time_obj = datetime.combine(datetime.now(), self.end_time)
        # Check if time_obj is within the range
        if start_time_obj > end_time_obj:
            return end_time_obj.hour <= right_now.hour <= start_time_obj.hour
        else:
            return start_time_obj.hour <= right_now.hour <= end_time_obj.hour


class Mood(models.Model):
    name = models.TextField()

