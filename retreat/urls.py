from django.urls import path
from .views import retreat_home

app_name = 'retreat'

urlpatterns = [
    path('', retreat_home, name='home'),
]