from django.db import models
from esp.sensor.sensor_types import *


class SensorModel(models.Model):
    sensor_type_list: list = [
        ('MotionSensor', 'Motion Sensor'),
        ('MasterSwitchSensor', 'Master Hand Sensor'),
        ('SilentAlarmSensor', 'Silent Alarm Sensor'),
        ('AlarmSensor', 'Alarm Sensor'),
    ]

    sensor_type = models.CharField(choices=sensor_type_list, max_length=55)
    esp = models.ForeignKey('esp.ESP', on_delete=models.CASCADE, related_name='sensors', null=True, default=None)
    key = models.ForeignKey('esp.Key', on_delete=models.CASCADE, related_name='keys', null=True, default=None)
    isMaster = models.BooleanField(default=False)
    usage = models.BooleanField(default=False)

    def can_use_sensor(self):
        return self.usage

    def get_action(self, *args, **kwargs):
        if self.can_use_sensor():
            if s_class := globals().get(self.sensor_type):
                s_class(self).take_action(*args, **kwargs, sensor=self)
            else:

                # log
                pass

    def __str__(self):
        return f"{self.esp.name} >] {self.id} / {self.sensor_type}"
