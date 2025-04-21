from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    # DeleteView,
    # DetailView,
    ListView,
    # UpdateView,
)

from task_manager.users.models import User
from task_manager.users.forms import CustomUserCreationForm


class UserListView(ListView):
    model = User
    template_name = 'users/index.html'
    context_object_name = 'users'


class UserCreateView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = "form.html"
    # success_url = reverse_lazy("users:login")
