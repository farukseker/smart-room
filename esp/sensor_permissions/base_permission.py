from logging import getLogger


class Permission:
    def __init__(self, sensor):
        self.sensor = sensor

    def can(self) -> bool:
        getLogger('Permission').info("Built in Permission class always return {'False'}, please replace with overhead")
        return False

