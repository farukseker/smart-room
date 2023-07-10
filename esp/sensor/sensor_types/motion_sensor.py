from .. import sensor_actions, sensor_permissions
from esp.sensor.sensor_types.base_sensor import SensorBase


class MotionSensor(SensorBase):
    action_classes = [
        sensor_actions.ChangeCurrent
    ]

    permission_classes = [
        sensor_permissions.TimeRange
    ]

