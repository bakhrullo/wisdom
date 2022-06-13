from django.apps import AppConfig


class WisappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wisapp'

    def ready(self):
        import wisapp.signals
