from django.urls import path
from . import views


app_name = 'capital'

urlpatterns = [
    path('', views.home, name='home'),
]