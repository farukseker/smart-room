import json

import redis
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
        print(f"signal if block :to : {instance.owner_esp}" )
        try:
            channel_layer = async_to_sync(get_channel_layer)()
            print("channel_layer get")
            async_to_sync(channel_layer.group_send)(
                "communication_%s" % instance.owner_esp.esp_id,
                {
                    "type": "key_status",
                    "pin": instance.pin_name,
                    "status": instance.current
                }
            )
        except Exception as e:
            print("Exception FROM Signals")
            raise e
    else:
        print("esp not vailedet : ", instance, is_create_signal)
        # pn = Key.objects.get(name='test')
        # print("time rangs")
        # print(pn.time_range.now_in_time_range())
