from django.apps import AppConfig


class MatchmakingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.matchmaking'

    def ready(self) -> None:
       from . import signals