from django.apps import AppConfig

class InvexConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'invex'

    def ready(self):
        import invex.signals

        