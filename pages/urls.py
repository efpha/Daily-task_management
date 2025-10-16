from django.urls import path
from . import views
from .views import dashboard_page

urlpatterns = [
    path('', views.home, name='home'), #home when not logged in
    path('dashboard/', views.dashboard_page, name='dashboard_page')
]
