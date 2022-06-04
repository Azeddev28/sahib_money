from django.apps import AppConfig


class AuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.authentication'

    def ready(self):
        # Import signals to activate signal handler.
        from . import signals
