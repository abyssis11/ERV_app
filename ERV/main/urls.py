from django.urls import path
from . import views 

app_name = 'main'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('worker_list/', views.worker_list, name="worker_list"),
    path('filter/', views.filter, name="filter")
]

htmx_urlpatterns = [
    path('search-worker/', views.search_worker, name='search-worker'),
    path('category_list/', views.category_list, name='category_list'),
]

urlpatterns += htmx_urlpatterns