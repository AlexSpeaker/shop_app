from django.apps import AppConfig


class ProductAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "product_app"

    def ready(self) -> None:
        import product_app.signals
