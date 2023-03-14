from django.urls import path
from . import views 

app_name = 'main'

urlpatterns = [
    path('homepage', views.homepage, name='homepage'),
    path('worker_list/', views.worker_list, name="worker_list"),
]

htmx_urlpatterns = [
    path('search-worker/', views.search_worker, name='search-worker'),
]

urlpatterns += htmx_urlpatterns