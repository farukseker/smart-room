from django.db import models
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from datetime import datetime, time
from importlib import import_module
import uuid
from esp import sensor_action

from esp.sensor_types import *


class Sensor(models.Model):
    sensor_type_list: list = [
        ('MotionSensor', 'Motion Sensor'),
    ]
    sensor_type = models.CharField(choices=sensor_type_list, max_length=55)
    esp = models.ForeignKey('esp.ESP', on_delete=models.CASCADE, related_name='sensors', null=True, default=None)
    key = models.ForeignKey('esp.Key', on_delete=models.CASCADE, related_name='keys', null=True, default=None)
    isMaster = models.BooleanField(default=False)
    usage = models.BooleanField(default=False)

    def can_use_sensor(self):
        return self.usage

    def get_action(self):
        if self.can_use_sensor():
            if s_class := globals().get(self.sensor_type):
                s_class(self).take_action()
            else:
                # log
                pass

#
# class MotionSensor:
#
#     def __init__(self, sensor):
#         self.sensor: Sensor = sensor
#         self.can_action_classes: list = [
#             sensor_action.TimeRange,
#         ]
#
#     def open_current(self):
#         self.sensor.key.current = True
#         self.sensor.save()
#
#     def action(self):
#         self.open_current()
#
#     def can_take_action(self):
#         return all([s_class(self.sensor).can() for s_class in self.can_action_classes ])
#
#     def take_action(self):
#         if self.can_take_action():
#             self.action()
#
