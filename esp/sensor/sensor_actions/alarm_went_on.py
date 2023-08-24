from discord import SyncWebhook
from config.settings.base_settings import env
from datetime import datetime


ESP_USER_COM = env('ESP_USER_COM')


class AlarmOn:
    def action(self, *args, **kwargs):
        print(self, args, kwargs)
        webhook = SyncWebhook.from_url(ESP_USER_COM)
        webhook.send(f"Esp Trigger ")
