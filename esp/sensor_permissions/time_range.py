
class TimeRange:
    def __init__(self, sensor):
        self.sensor = sensor

    def can(self):
        if self.sensor.key.use_time_range:
            return self.sensor.key.now_in_time_range()
        else:
            return True

