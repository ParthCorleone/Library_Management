from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Book , BookRequest ,Task

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'role')

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'quantity']

class BookRequestForm(forms.ModelForm):
    class Meta:
        model = BookRequest
        fields = []

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['staff', 'task_description']

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['staff'].queryset = CustomUser.objects.filter(role='Staff')
