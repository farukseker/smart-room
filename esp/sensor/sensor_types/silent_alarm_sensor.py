from .. import sensor_actions, sensor_permissions
from .base_sensor import SensorBase


class SilentAlarmSensor(SensorBase):
    permission_classes = [
        sensor_permissions.TimeRange,
    ]
    action_classes = [
        sensor_actions.ChangeCurrent,
    ]

    alarm_classes = [
        sensor_actions.AlarmOn,
    ]

    def take_action(self, *args, **kwargs):
        print("taken")
        can = super().can_take_action()
        print("can")
        if not can:
            print("in")
            super().action(*args, **kwargs)
            self.action_classes = self.alarm_classes
        print('set')
        super().action(*args, **kwargs)


class AlarmSensor(SensorBase):
    alarm_classes = [
        sensor_actions.AlarmOn,
    ]

    def take_action(self, *args, **kwargs):
        can = super().can_take_action()
        if not can:
            self.action_classes = self.alarm_classes
        super().action(*args, **kwargs)


