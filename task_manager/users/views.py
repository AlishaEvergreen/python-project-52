from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    # DeleteView,
    # DetailView,
    # ListView,
    # UpdateView,
)

from task_manager.users.models import User
from task_manager.users.forms import CustomUserCreationForm


class UserCreateView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = "form.html"
    # success_url = reverse_lazy("users:login")
