from esp.sensor_permissions.base_permission import Permission


class Master(Permission):

    def can(self) -> bool | None:
        return True

