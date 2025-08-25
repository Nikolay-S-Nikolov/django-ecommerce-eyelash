from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lash_store.accounts'
    
    def ready(self):
        import lash_store.accounts.signals