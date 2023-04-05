import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from django.dispatch import receiver
from esp.models import Key
from esp.models import ESP

@receiver(post_save, sender=Key)
def send_message_to_socket(sender, instance, **kwargs):
    ESP.objects.get(keys__in=instance)
    # channel_layer = get_channel_layer()
    # print("esp ad")
    # async_to_sync(channel_layer.group_send)(
    #     "communication_b2c4b984-dd3b-4a66-9731-67754cc19fd1",
    #     {
    #         "type": "key_status",
    #         # "message": json.dumps({"status":instance.current})
    #         "status": "argos"
    #     }
    # )
