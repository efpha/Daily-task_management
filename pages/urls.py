from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_status, name='api_status'),
]
