import json


class ChangeCurrent:

    def action(self, *args, **kwargs):
        sensor = kwargs.get('sensor', None)
        current = kwargs.get('status', None)
        if self.is_valid(sensor, current):
            sensor.key.set_current(current=bool(int(current)), master=sensor.isMaster)

    @staticmethod
    def is_valid(*args):
        return not any([arg is None for arg in args])

