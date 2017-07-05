from django.apps import AppConfig


class AppConfig(AppConfig):
    name = 'xxx'

    def ready(self):
        # execute twice
        print("run django-q")
