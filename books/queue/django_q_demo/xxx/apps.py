from django.apps import AppConfig
import os


class AppConfig(AppConfig):
    name = 'xxx'

    def ready(self):
        # execute twice
        print(os.getpid())
        print("run django-q")
