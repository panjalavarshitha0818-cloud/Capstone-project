from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='planner/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('task/add/', views.add_task, name='add_task'),
    path('task/edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('task/delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('task/toggle/<int:task_id>/', views.toggle_task_completion, name='toggle_task_completion'),
    path('reset/', views.reset_planner, name='reset_planner'),
    path('api/tasks/', views.task_list_api, name='task_list_api'),
]
