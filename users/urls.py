from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [
    path('register/', views.register_user, name='register_user_api'),
    path('login/', views.user_login, name='user_login_api'),
    path('logout/', views.logout_user, name='logout_user'),

    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/test/', views.login_test, name='login_test'),
]
