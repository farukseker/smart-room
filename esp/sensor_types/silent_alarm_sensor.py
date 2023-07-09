from esp import sensor_permissions
from esp import sensor_actions
from .base_sensor import SensorBase


class SilentAlarmSensor(SensorBase):
    permission_classes = [
        sensor_permissions.TimeRange,
    ]
    action_classes = [
        sensor_actions.ChangeCurrent,
    ]

    def take_action(self, *args, **kwargs):
        can = super().can_take_action()
        if not can:
            self.action_classes.append(sensor_actions.AlarmOn)
        super().action(*args, **kwargs)


