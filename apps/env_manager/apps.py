from django.apps import AppConfig


class EnvManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.env_manager'
    def ready(self):
        import apps.env_manager.signals