from esp import sensor_permissions
from esp import sensor_actions
from .base_sensor import SensorBase


class MasterSwitchSensor(SensorBase):
    permission_classes = [
        sensor_permissions.Master,
    ]
    action_classes = [
        sensor_actions.ChangeCurrent,
    ]

