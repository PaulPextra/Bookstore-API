from django.apps import AppConfig


class OrderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'order'
    
    def ready(self):
        
        # import signal handlers
        import order.signals

