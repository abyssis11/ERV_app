from django.apps import AppConfig


class AaiIntegrationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'aai_integration'

    def ready(self):
        import django.conf
        if not hasattr(django.conf.settings, 'AAI_DATA_MODEL'):
            django.conf.settings.AAI_DATA_MODEL = 'aai_integration.AAIData'

        if not hasattr(django.conf.settings, 'AAI_DATA_RELATED_NAME'):
            django.conf.settings.AAI_DATA_RELATED_NAME = 'aai_data'

        if not hasattr(django.conf.settings, 'AAI_PRIVILEGED_ATTRIBUTES'):
            django.conf.settings.AAI_DATA_RELATED_NAME = {}

        import aai_integration.signals
