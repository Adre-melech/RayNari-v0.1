from django.urls import path
from . import views

app_name = 'resort'

urlpatterns = [
    path('', views.home, name='home'),
]