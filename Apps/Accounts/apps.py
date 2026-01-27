from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Apps.Accounts'

    def ready(self):
        # Import signals to ensure they are registered when the app starts
        import Apps.Accounts.signals