from django import dispatch
from django.apps import apps
from django.conf import settings
from django.contrib import auth
from django.db import models


@dispatch.receiver(models.signals.post_save, sender=auth.get_user_model())
def create_aai_data(sender, instance, created, **kwargs):
    if created:
        data_model = settings.AAI_DATA_MODEL
        apps.get_model(data_model).objects.create(user=instance)
