from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('machine_data', views.machine_data, name='machine_data'),
]
