from django.forms import ModelForm

from task_manager.statuses.models import Status
from task_manager.mixins import FormStyleMixin


class StatusCreationForm(FormStyleMixin, ModelForm):
    class Meta:
        model = Status
        fields = ['name']
