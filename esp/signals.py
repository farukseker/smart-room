import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from django.dispatch import receiver
from esp.models import Key
from esp.models import ESP


@receiver(post_save, sender=Key)
def send_message_to_socket(sender, instance, **kwargs):
    is_create_signal = kwargs.get("created")
    if not is_create_signal and not instance.last_updater_is_esp:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "communication_%s" % instance.owner_esp.esp_id,
            {
                "type": "key_status",
                "pin": instance.pin_name,
                "status":instance.current
            }
        )
        # async_to_sync(channel_layer.disconnect)()
