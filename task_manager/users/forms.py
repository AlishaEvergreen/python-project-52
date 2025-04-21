from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from task_manager.users.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', *UserCreationForm.Meta.fields)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        config = {
            'username': (
                _('Username'),
                _('Required. 150 characters or fewer. '
                  'Letters, digits and @/./+/-/_ only.')
            ),
            'first_name': (_('First Name'), ''),
            'last_name': (_('Last Name'), ''),
            'password1': (
                _('Password'),
                _('Your password must contain at least 3 characters.')
            ),
            'password2': (
                _('Password confirmation'),
                _('Please enter your password again to confirm.')
            ),
        }
        for name, (label, help_text) in config.items():
            if name in self.fields:
                field = self.fields[name]
                field.label, field.help_text = label, help_text
                field.widget.attrs.update({
                    'class': 'form-control bg-secondary bg-opacity-50 '
                             'border-secondary',
                    'placeholder': label,
                })
