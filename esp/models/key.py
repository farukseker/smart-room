from django.db import models
from datetime import datetime, time


class Key(models.Model):
    """
    if start_time_obj > end_time_obj:
        return end_time_obj.hour <= right_now.hour <= start_time_obj.hour
    else:
        return start_time_obj.hour <= right_now.hour <= end_time_obj.hour
    """
    owner_esp = models.ForeignKey("ESP", on_delete=models.CASCADE, default=None, blank=True, null=True)
    pin_name = models.TextField(default="")
    name = models.TextField()
    current = models.BooleanField(default=False)
    last_updater_is_esp = models.BooleanField(default=False)

    use_time_range = models.BooleanField(default=False)
    start_time = models.TimeField(default=None, null=True)
    end_time = models.TimeField(default=None, null=True)

    def set_current(self, current: bool, master: bool = False):
        self.last_updater_is_esp = master
        self.current = bool(current)

        self.save()

    # Convert the time argument to a datetime object
    def now_in_time_range(self):
        right_now = datetime.now()

        start_time_obj = datetime.combine(datetime.now(), self.start_time)
        end_time_obj = datetime.combine(datetime.now(), self.end_time)

        return end_time_obj.hour <= right_now.hour <= start_time_obj.hour if start_time_obj > end_time_obj else start_time_obj.hour <= right_now.hour <= end_time_obj.hour

    def __str__(self):
        return f"key : { self.name }|{ self.pin_name } @ { self.owner_esp }"
