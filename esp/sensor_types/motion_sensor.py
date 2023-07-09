from esp import sensor_action
from esp.models import Sensor


class MotionSensor:

    def __init__(self, sensor):
        self.sensor: Sensor = sensor
        self.can_action_classes: list = [
            sensor_action.TimeRange,
        ]

    def open_current(self):
        self.sensor.key.current = True
        self.sensor.save()

    def action(self):
        self.open_current()

    def can_take_action(self):
        return all([s_class(self.sensor).can() for s_class in self.can_action_classes])

    def take_action(self):
        if self.can_take_action():
            self.action()

