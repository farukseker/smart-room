class OpenCurrent:

    def action(self, *args, **kwargs):
        sensor = kwargs.get('sensor', None)
        master = kwargs.get('master', None)
        current = kwargs.get('current', None)
        if self.is_valid(sensor, master, current):
            sensor.key.set_current(current=current, master=master)

    @staticmethod
    def is_valid(*args):
        return not any([arg is None for arg in args])

