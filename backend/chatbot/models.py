from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class ChatSession(models.Model):
    """Represents a chat session between user and chatbot"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    context_window = models.JSONField(blank=True, default=dict)
    conversation_summary = models.TextField(blank=True, null=True)
    language = models.CharField(max_length=10, default='en')
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Session {self.session_id}"


class Message(models.Model):
    """Represents individual messages in a chat session"""
    MESSAGE_TYPES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
        ('system', 'System'),
    ]
    
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_helpful = models.BooleanField(null=True, blank=True)  # User feedback
    response_time = models.FloatField(null=True, blank=True)  # Time taken to generate response
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.message_type}: {self.content[:50]}..."


class KnowledgeBaseEntry(models.Model):
    """Represents entries in the knowledge base"""
    CATEGORIES = [
        ('python', 'Python Programming'),
        ('ai', 'Artificial Intelligence'),
        ('course_info', 'Course Information'),
        ('instructor_info', 'Instructor Information'),
        ('general', 'General'),
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORIES)
    keywords = models.TextField(blank=True, help_text="Comma-separated keywords for search")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    priority = models.IntegerField(default=0, help_text="Higher priority entries are preferred")
    
    class Meta:
        ordering = ['-priority', '-created_at']
    
    def __str__(self):
        return self.title


class ChatbotConfiguration(models.Model):
    """Configuration settings for the chatbot"""
    name = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name}: {self.value}"
