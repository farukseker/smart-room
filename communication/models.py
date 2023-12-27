from django.db import models
import uuid


class WebSocketConsumerAccessesModel(models.Model):
    user = models.ForeignKey('Account.CustomUserModel', on_delete=models.CASCADE)
    accesses_create_time = models.DateTimeField(auto_now_add=True)
    accesses_token = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    def __str__(self):

        return f'@{self.user.username}=[{self.accesses_token}]'

