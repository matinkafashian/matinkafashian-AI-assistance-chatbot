from rest_framework import serializers
from .models import ChatSession, Message, KnowledgeBaseEntry, ChatbotConfiguration


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'message_type', 'content', 'timestamp', 'is_helpful', 'response_time']


class ChatSessionSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = ChatSession
        fields = ['id', 'session_id', 'created_at', 'updated_at', 'is_active', 'messages']


class KnowledgeBaseEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = KnowledgeBaseEntry
        fields = ['id', 'title', 'content', 'category', 'keywords', 'created_at', 'updated_at', 'is_active', 'priority']


class ChatbotConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatbotConfiguration
        fields = ['id', 'name', 'value', 'description', 'created_at', 'updated_at']


class ChatMessageSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=1000)
    session_id = serializers.CharField(max_length=100, required=False)
    context = serializers.JSONField(required=False)


class ChatResponseSerializer(serializers.Serializer):
    response = serializers.CharField()
    session_id = serializers.CharField()
    message_id = serializers.IntegerField()
    response_time = serializers.FloatField()
    sources = serializers.ListField(child=serializers.CharField(), required=False)
