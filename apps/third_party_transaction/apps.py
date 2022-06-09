from django.apps import AppConfig


class ThirdPartyAuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.third_party_transaction'

    def ready(self):
        # Import signals to activate signal handler.
        from . import signals
