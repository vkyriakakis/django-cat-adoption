from django.apps import AppConfig


class AdoptConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'adopt'

    def ready(self):
        from . import signals