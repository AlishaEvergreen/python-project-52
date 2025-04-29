from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
)

from task_manager.mixins import (
    CustomLoginRequiredMixin,
    UserPermissionMixin,
)
from task_manager.users.models import User
from task_manager.users.forms import (
    CustomUserCreationForm,
    CustomUserChangeForm,
)


class UserListView(ListView):
    model = User
    template_name = 'users/index.html'
    context_object_name = 'users'


class BaseUserView(SuccessMessageMixin):
    model = User
    template_name = 'users/registration_form.html'
    context_object_name = 'user'
    permission_denied_url = reverse_lazy('users:index')


class UserCreateView(BaseUserView, CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    success_message = _('User was registered successfully')
    extra_context = {
        'title': _('Sign Up'),
        'button_name': _('Register')
    }


class UserUpdateView(CustomLoginRequiredMixin, UserPermissionMixin,
                     BaseUserView, UpdateView):
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('users:index')
    success_message = _('User was updated successfully')
    permission_denied_message = _(
        "You don't have rights to change another user."
    )
    extra_context = {
        'title': _('Edit profile'),
        'button_name': _('Save changes')
    }
