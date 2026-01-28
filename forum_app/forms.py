from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Branch, Message

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ['name', 'description', 'parent_branch']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'parent_branch': forms.Select(attrs={'style': 'width: 100%; padding: 6px;'})
        }

    def __init__(self, *args, **kwargs):
        parent_branch = kwargs.pop('parent_branch', None)
        super().__init__(*args, **kwargs)
        if parent_branch:
            self.fields['parent_branch'].initial = parent_branch
            self.fields['parent_branch'].widget = forms.HiddenInput()

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Напишите ваше сообщение...',
                'style': 'width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px;'
            })
        }        