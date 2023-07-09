

from django.contrib.auth import get_user_model
import uuid
from django.db import models

user_model = get_user_model()


class ESP(models.Model):
    user = models.ForeignKey(user_model, on_delete=models.CASCADE, default=None, blank=True, null=True)
    name = models.TextField()
    esp_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    api_key = models.UUIDField(default=uuid.uuid4, editable=True)
    keys = models.ManyToManyField("Key", blank=True, default=None)
    is_connected = models.BooleanField(default=False)

    def get_keys(self):
        return self.keys.all()

    def __str__(self):
        return f"{self.name}|{self.esp_id}"

