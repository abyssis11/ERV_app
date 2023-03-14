from django.urls import path
from . import views 

app_name = 'main'

urlpatterns = [
    path('homepage', views.homepage, name='homepage'),
    path('upload_CSV', views.upload_CSV, name='upload_CSV'),
    path('upload', views.upload, name='upload')
]
