from django.contrib import admin
from main.models import *

# Register your models here.
models_list=[Worker, Job, ERV, Marker]
admin.site.register(models_list)