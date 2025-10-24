from django.contrib import admin
from .models import ChatSession, Message, KnowledgeBaseEntry, ChatbotConfiguration


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'user', 'created_at', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['session_id', 'user__username']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['session', 'message_type', 'content_preview', 'timestamp', 'is_helpful']
    list_filter = ['message_type', 'timestamp', 'is_helpful']
    search_fields = ['content', 'session__session_id']
    
    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'


@admin.register(KnowledgeBaseEntry)
class KnowledgeBaseEntryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'priority', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['title', 'content', 'keywords']
    ordering = ['-priority', '-created_at']


@admin.register(ChatbotConfiguration)
class ChatbotConfigurationAdmin(admin.ModelAdmin):
    list_display = ['name', 'value_preview', 'description', 'updated_at']
    search_fields = ['name', 'description']
    
    def value_preview(self, obj):
        return obj.value[:50] + "..." if len(obj.value) > 50 else obj.value
    value_preview.short_description = 'Value Preview'
