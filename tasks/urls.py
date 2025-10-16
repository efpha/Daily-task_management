from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_task, name='create_task'),
path('all/', views.get_tasks, name='get_tasks'),
    path('<int:pk>/', views.get_task_by_id, name='get_task_by_id'),
    path('update/<int:pk>/', views.update_task, name='update_task'),
    path('delete/<int:pk>/', views.delete_task, name='delete_task')
]