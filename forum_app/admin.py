from django.contrib import admin
from .models import Branch, Topic, Message

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_branch', 'created_at')
    list_filter = ('parent_branch',)
    search_fields = ('name',)

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'branch', 'author', 'created_at')
    list_filter = ('branch', 'author')
    search_fields = ('title',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('topic', 'author', 'created_at')
    list_filter = ('topic', 'author')
    search_fields = ('content',)