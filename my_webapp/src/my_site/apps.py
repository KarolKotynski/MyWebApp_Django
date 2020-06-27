from django.apps import AppConfig


class MySiteConfig(AppConfig):
    name = 'my_site'

    def ready(self):
        ## Take signals from my_site project
        import my_site.signals