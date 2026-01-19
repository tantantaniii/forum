from django.db import models
from django.contrib.auth.models import User

class Branch(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название ветки")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    parent_branch = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True,
        related_name='subbranches', verbose_name="Родительская ветка"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создана")

    class Meta:
        verbose_name = "Ветка"
        verbose_name_plural = "Ветки"

    def __str__(self):
        return self.name

    def get_full_path(self):
        """Возвращает полный путь ветки через ->"""
        if self.parent_branch:
            return f"{self.parent_branch.get_full_path()} -> {self.name}"
        return self.name


class Topic(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок темы")
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='topics', verbose_name="Ветка")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Автор")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создана")

    class Meta:
        verbose_name = "Тема"
        verbose_name_plural = "Темы"

    def __str__(self):
        return self.title


class Message(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='messages', verbose_name="Тема")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Автор")
    content = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата")

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return f"Сообщение от {self.author} в теме {self.topic}"
