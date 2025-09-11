from django.apps import AppConfig


class tachesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'taches'



    def ready(self):
        import taches.signals 
