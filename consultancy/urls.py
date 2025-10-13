from django.urls import path
from .views import homepage, service_list, service_detail

app_name = 'consultancy'

urlpatterns = [
    path('', homepage, name='consultancy'),
    path('services/', service_list, name='service_list'),
    path('<slug:slug>/', service_detail, name='service_detail'),
]