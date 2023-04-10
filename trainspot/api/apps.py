from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"

    def ready(self):
        from django.db.models.signals import post_save
        from api.signals import send_email_on_post
        post_save.connect(send_email_on_post)
