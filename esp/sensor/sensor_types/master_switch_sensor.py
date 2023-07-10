from .. import sensor_actions, sensor_permissions
from .base_sensor import SensorBase


class MasterSwitchSensor(SensorBase):
    permission_classes = [
        sensor_permissions.Master,
    ]
    action_classes = [
        sensor_actions.ChangeCurrent,
    ]

