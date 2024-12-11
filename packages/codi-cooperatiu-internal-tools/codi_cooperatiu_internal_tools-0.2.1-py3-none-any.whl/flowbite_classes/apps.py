from django.apps import AppConfig
from django.conf import settings


class FlowbiteClassesConfig(AppConfig):
    name = "flowbite_classes"

    def ready(self):
        if getattr(settings, "CODI_COOP_ENABLE_MONKEY_PATCH", False):
            self.apply_monkey_patch()

    @staticmethod
    def apply_monkey_patch():
        import flowbite_classes.monkey_patch  # noqa: F401
