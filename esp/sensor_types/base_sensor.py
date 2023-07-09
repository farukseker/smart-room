
class SensorBase:
    permission_classes: list = []
    action_classes: list = []

    def __init__(self, sensor):
        self.sensor = sensor

    def get_permission_classes(self):
        assert self.permission_classes is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method."
            % self.__class__.__name__
        )
        return self.permission_classes

    def get_action_classes(self):
        assert self.action_classes is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method."
            % self.__class__.__name__
        )
        return self.action_classes

    def can_take_action(self):
        return all([s_class(self.sensor).can() for s_class in self.get_permission_classes()])

    def action(self, *args, **kwargs):
        for action_class in self.get_action_classes():
            action_class().action(*args, **kwargs)

    def take_action(self, *args, **kwargs):
        if self.can_take_action():
            self.action(*args, **kwargs)
