class Permission:
    def __init__(self, sensor):
        self.sensor = sensor

    def can(self) -> bool | None:
        return None