from django.apps import AppConfig


class SupportConfig(AppConfig):
    name = "zs_utils.base_support"
    label = "base_support"

    def ready(self) -> None:
        import zs_utils.base_support.signals  # noqa
