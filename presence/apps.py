from django.apps import AppConfig


class PresenceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'presence'
    def ready(self):
        import presence  # Remplacer `your_app_name` par le nom de votre application

    