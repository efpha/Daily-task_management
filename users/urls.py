from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views
from .views import register_user, user_login

urlpatterns = [
    path('login/', user_login, name='login_user'),
    path('register/', register_user, name='register_user'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
