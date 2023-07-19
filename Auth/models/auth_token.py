from django.db import models
import uuid

from datetime import datetime
from datetime import timedelta


class AuthToken(models.Model):
    token = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('Account.CustomUserModel', on_delete=models.CASCADE, blank=True, null=True)
    life = models.DateTimeField(null=True,blank=True)
    usage = models.TextField(null=True, default='None')
    def __str__(self):
        return f'{self.token} |-> {self.user}'
