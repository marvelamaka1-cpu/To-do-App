from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Task


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "category",
            "priority",
            "due_date",
            "due_time",
            "done",
        ]

        widgets = {

    "title": forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Task title"
    }),

    "description": forms.Textarea(attrs={
        "class": "form-control",
        "rows": 4,
        "placeholder": "Task description"
    }),

    "category": forms.Select(attrs={
        "class": "form-select"
    }),

    "priority": forms.Select(attrs={
        "class": "form-select"
    }),

    "due_date": forms.DateInput(attrs={
        "type": "date",
        "class": "form-control"
    }),

    "due_time": forms.TimeInput(attrs={
        "type": "time",
        "class": "form-control"
    }),

    "done": forms.CheckboxInput(attrs={
        "class": "form-check-input"
    }),
}


class RegisterForm(UserCreationForm):

    class Meta:

        model = User

        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )

        widgets = {

            "username": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Choose a username"
            }),

            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your email"
            }),

        }

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Create password"
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Confirm password"
        })
    )