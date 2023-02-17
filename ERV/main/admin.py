from django.contrib import admin
from main.models import *

# Register your models here.
models_list=[Worker, Job, ERV]
admin.site.register(models_list)