from django.urls import path
from . import views 

app_name = 'main'

urlpatterns = [
    path('homepage', views.homepage, name='homepage'),
    path('upload_form', views.upload_form, name='upload_form'),
    path('upload_csv', views.upload_csv, name='upload_csv'),
    path('add_erv', views.add_erv, name='add_erv'),
    path('add_worker', views.add_worker, name='add_worker'),
    path("erv_table/", views.ErvTable.as_view(), name="erv_table"),
    path('swap_erv_table/', views.SwapErvTable.as_view(), name='swap_erv_table'),
    path('erv_table/jobs', views.Jobs.as_view(), name='jobs'),
    path('edit_erv/<int:pk>/', views.edit_erv, name='edit_erv'),
    path('remove_erv/<int:pk>/', views.remove_erv, name='remove_erv'),
    path('bar_graph/<int:pk>/<str:year>/<str:month>/', views.bar_graph, name='bar_graph'),
    path('pie/<int:pk>/<str:year>/<str:month>/', views.pie, name='pie')
]
