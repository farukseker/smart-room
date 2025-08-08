# esp/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from .models import ESP, Key


@receiver(post_save, sender=ESP)
def send_esp_data_update(sender, instance, **kwargs):
    """
    ESP modelinde bir değişiklik olduğunda, bunu WebSocket üzerinden ilgili gruba gönderir.
    """
    channel_layer = get_channel_layer()
    group_name = "esp_data"

    # WebSocket mesajını oluştur
    message = {
        "type": "esp_data_message",
        "message": json.dumps({
            "esp_id": instance.id,
            "status": instance.status,
            "user_id": str(instance.user.id) if instance.user else None
        })
    }

    # Mesajı eş zamanlı (sync) olarak gönder
    async_to_sync(channel_layer.group_send)(group_name, message)


@receiver(post_save, sender=Key)
def send_message_to_socket(sender, instance, **kwargs):
    is_create_signal = kwargs.get("created")
    channel_layer = get_channel_layer()

    if not is_create_signal and not instance.last_updater_is_esp:
        print(f"signal if block :to : {instance.owner_esp}")
        try:
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
    try:
        async_to_sync(channel_layer.group_send)(
            f"communication_{instance.owner_esp.user.username}_{instance.owner_esp.user.id}",
            {
                "type": "send_esp_device_list",
            }
        )
    except Exception as e:
        print("Exception FORM signals with user")
    else:
        print("esp not vailedet : ", instance, is_create_signal)
        # pn = Key.objects.get(name='test')
        # print("time rangs")
        # print(pn.time_range.now_in_time_range())
