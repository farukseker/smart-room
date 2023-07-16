from .. import sensor_actions, sensor_permissions
from .base_sensor import SensorBase


class CoolerFan(SensorBase):
    permission_classes: list = [
        sensor_permissions.Master
    ]
    action_classes: list = [
        sensor_actions.ChangeCurrent
    ]
