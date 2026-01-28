from django.contrib import admin
from .models import Branch, Message

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_branch', 'author', 'created_at')
    list_filter = ('parent_branch', 'author')
    search_fields = ('name', 'description')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('content_short', 'branch', 'author', 'created_at')
    list_filter = ('branch', 'author')
    search_fields = ('content', 'branch__name')

    def content_short(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_short.short_description = 'Сообщение'