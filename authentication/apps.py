from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'authentication'
    
    def ready(self):
        import authentication.signals
