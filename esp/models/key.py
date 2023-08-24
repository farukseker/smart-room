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
        right_now_obj = datetime.now()
        right_now = right_now_obj.hour

        start_time_obj = datetime.combine(datetime.now(), self.start_time)
        start_time = start_time_obj.hour

        end_time_obj = datetime.combine(datetime.now(), self.end_time)
        end_time = end_time_obj.hour

        # if start_time > end_time:
        #     return end_time >= right_now >= end_time
        # else:
        #     return start_time >= right_now >= end_time

        if end_time > start_time:
            return start_time <= right_now <= end_time
        else:
            if end_time <= right_now and start_time <= right_now:
                return True
            if end_time < 24:
                return end_time >= right_now

    def __str__(self):
        return f"key : { self.name }|{ self.pin_name } @ { self.owner_esp }"
