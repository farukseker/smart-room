from esp.sensor.sensor_permissions.base_permission import Permission


class Master(Permission):

    def can(self) -> bool:
        return True

