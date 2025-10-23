from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views
from .views import register_user, user_login, logout_user

urlpatterns = [
    #template pages
    path('login/page/', views.login_page, name='login_page'),
    path('register/page/', views.register_page, name='register_page'),
    path('logout/', views.logout_user, name='logout_user'),

    #API endpoints
    path('register/', views.register_user, name='register_user_api'),
    path('login/', views.user_login, name='user_login_api'),

    #JWT token refresh
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('login/test/', views.login_test, name='login_test'),
]
