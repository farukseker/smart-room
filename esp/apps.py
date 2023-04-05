from django.apps import AppConfig


class EspConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'esp'

    def ready(self):
        from esp import signals
