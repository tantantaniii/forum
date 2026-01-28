# forum_app/models.py

from django.db import models
from django.contrib.auth.models import User

class Branch(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    parent_branch = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='subbranches',
        verbose_name="Родительская ветка"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Автор"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создана")

    class Meta:
        verbose_name = "Ветка"
        verbose_name_plural = "Ветки"

    def __str__(self):
        return self.name

    def is_topic(self):
        """Возвращает True, если это подветка (т.е. тема)"""
        return self.parent_branch is not None

class Message(models.Model):
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name="Тема/Подветка",
        null=True,      # ← разрешаем NULL
        blank=True      # ← разрешаем пустое значение в форме
    )
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return f"Сообщение в '{self.branch}' от {self.author}"