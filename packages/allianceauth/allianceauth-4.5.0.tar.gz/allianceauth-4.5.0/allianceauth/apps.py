from django.apps import AppConfig
from django.core.checks import Warning, Error, register


class AllianceAuthConfig(AppConfig):
    name = 'allianceauth'

    def ready(self) -> None:
        import allianceauth.checks # noqa
