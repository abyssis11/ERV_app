from django.urls import path
from . import views 

app_name = 'main'

urlpatterns = [
    path('homepage', views.homepage, name='homepage'),
    path('upload_form', views.upload_form, name='upload_form'),
    path('upload_csv', views.upload_csv, name='upload_csv')
]
