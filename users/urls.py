from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views
from .views import register_user, user_login

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('login/api/', user_login, name='login_user'),
    path('login/test/', views.test_login_endpoint, name='test_login_endpoint'),
    path('register/', views.register_view, name='register'),
    path('register/api/', register_user, name='register_user'),
    path('register/test/', views.test_register_endpoint, name='test_register_endpoint'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
