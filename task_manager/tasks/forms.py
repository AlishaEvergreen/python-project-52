from django.forms import ModelForm

from task_manager.tasks.models import Task
from task_manager.mixins import FormStyleMixin


class TaskCreationForm(FormStyleMixin, ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
