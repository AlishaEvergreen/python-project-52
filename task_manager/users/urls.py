from django.urls import path
from task_manager.users import views

app_name = 'users'

urlpatterns = [
    path('create/', views.UserCreateView.as_view(), name='create'),
]
