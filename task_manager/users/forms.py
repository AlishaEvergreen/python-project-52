from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _

from task_manager.mixins import FormStyleMixin
from task_manager.users.models import User


class BaseUserForm:
    """Base Meta settings for User forms."""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')
        help_texts = {
            'username': _(
                'Required. 150 characters or fewer. '
                'Letters, digits and @/./+/-/_ only.'
            ),
        }


class CustomUserCreationForm(FormStyleMixin, UserCreationForm):
    """User registration form with Bootstrap and password fields."""
    class Meta(BaseUserForm.Meta):
        fields = (*BaseUserForm.Meta.fields, 'password1', 'password2')
        help_texts = {
            **BaseUserForm.Meta.help_texts,
            'password1':
                _('Your password must contain at least 3 characters.'),
            'password2':
                _('Please enter your password again to confirm.'),
        }

    def clean(self):
        """Ensure passwords match and meet requirements."""
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2:
            if password1 != password2:
                self.add_error(
                    "password2",
                    _("Passwords don't match.")
                )

            if len(password1) < 3:
                self.add_error(
                    "password2",
                    _(
                        "This password is too short. "
                        "It must contain at least 3 characters."
                    ),
                )
        return cleaned_data


class CustomUserChangeForm(FormStyleMixin, UserChangeForm):
    """User update form with password change and Bootstrap styling."""
    password = forms.CharField(
        label=_("New Password"), widget=forms.PasswordInput, required=True,
        help_text=_("Your password must contain at least 3 characters."),
    )
    password_confirmation = forms.CharField(
        label=_("Confirm Password"), widget=forms.PasswordInput, required=True,
        help_text=_("Please enter your password again to confirm."),
    )

    class Meta(BaseUserForm.Meta):
        pass

    def clean(self):
        """Ensure passwords match."""
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        if password or password_confirmation:
            if password != password_confirmation:
                self.add_error(
                    "password_confirmation",
                    _("Passwords don't match.")
                )
            elif len(password) < 3:
                self.add_error(
                    "password_confirmation",
                    _(
                        "This password is too short. "
                        "It must contain at least 3 characters."
                    ),
                )
        return cleaned_data

    def save(self, commit=True):
        """Save user with new password if provided."""
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password and len(password) >= 3:
            user.set_password(password)
        if commit:
            user.save()
        return user
