from django import forms
from .models import Branch, Topic, Message

class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ['name', 'description', 'parent_branch']
        labels = {
            'name': 'Название ветки',
            'description': 'Описание',
            'parent_branch': 'Родительская ветка (если подветка)'
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        parent_branch = kwargs.pop('parent_branch', None)
        super().__init__(*args, **kwargs)
        if parent_branch:
            self.fields['parent_branch'].initial = parent_branch
            self.fields['parent_branch'].widget = forms.HiddenInput()


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'branch']
        labels = {
            'title': 'Заголовок темы',
            'branch': 'Ветка'
        }
        widgets = {
            'branch': forms.HiddenInput()  
        }    

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        labels = {
            'content': 'Сообщение'
        }
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Напишите ваше сообщение...'
            })
        }

    def __init__(self, *args, **kwargs):
        self.topic = kwargs.pop('topic', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        message = super().save(commit=False)
        message.topic = self.topic
        message.author = self.instance.author if self.instance.pk else None  # если редактируем
        if commit:
            message.save()
        return message    