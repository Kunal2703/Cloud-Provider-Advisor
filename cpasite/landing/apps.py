from django.apps import AppConfig
import os
class LandingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "landing"

    def ready(self):
        from jobs import updater
        if os.environ.get('RUN_MAIN'):
            updater.start()