from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    due_time = forms.TimeField(
        required=False,
        widget=forms.TimeInput(attrs={'type': 'time'})
    )

    class Meta:
        model = Task
        fields = ['title', 'due_time', 'done']