from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
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


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    template_name = "users/registration_form.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    success_message = _('User was successfully registered')
