from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import models
from .models import ChatSession, Message, KnowledgeBaseEntry
from .serializers import (
    ChatSessionSerializer, 
    MessageSerializer, 
    ChatMessageSerializer,
    ChatResponseSerializer,
    KnowledgeBaseEntrySerializer
)
from .ai_service import AIService
import uuid


@api_view(['GET'])
def health_check(request):
    """Health check endpoint for Render.com"""
    return Response({'status': 'healthy', 'service': 'AI Chatbot Backend'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def send_message(request):
    """Send a message to the chatbot and get response"""
    serializer = ChatMessageSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    user_message = serializer.validated_data['message']
    session_id = serializer.validated_data.get('session_id')
    language = serializer.validated_data.get('language', 'en')
    
    # Get or create session
    if session_id:
        try:
            session = ChatSession.objects.get(session_id=session_id)
            # Update session language if provided
            if language != 'en':
                session.language = language
                session.save()
        except ChatSession.DoesNotExist:
            session = ChatSession.objects.create(session_id=session_id, language=language)
    else:
        session = ChatSession.objects.create(session_id=str(uuid.uuid4()), language=language)
    
    # Save user message
    user_msg = Message.objects.create(
        session=session,
        message_type='user',
        content=user_message
    )
    
    # Get AI response
    ai_service = AIService()
    ai_response = ai_service.generate_response(user_message, session.session_id, language)
    
    # Save AI response
    ai_msg = Message.objects.create(
        session=session,
        message_type='assistant',
        content=ai_response['response'],
        response_time=ai_response['response_time']
    )
    
    # Return response
    response_serializer = ChatResponseSerializer({
        'response': ai_response['response'],
        'session_id': session.session_id,
        'message_id': ai_msg.id,
        'response_time': ai_response['response_time'],
        'sources': ai_response.get('sources', [])
    })
    
    return Response(response_serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_session(request, session_id):
    """Get chat session with all messages"""
    session = get_object_or_404(ChatSession, session_id=session_id)
    serializer = ChatSessionSerializer(session)
    return Response(serializer.data)


@api_view(['POST'])
def create_session(request):
    """Create a new chat session"""
    preferred_language = request.data.get('language', 'en')
    if preferred_language not in ['en', 'fa']:
        preferred_language = 'en'
    session = ChatSession.objects.create(
        session_id=str(uuid.uuid4()),
        context_window={},
        conversation_summary="",
        language=preferred_language
    )
    serializer = ChatSessionSerializer(session)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_sessions(request):
    """Get all chat sessions"""
    sessions = ChatSession.objects.all().order_by('-created_at')
    serializer = ChatSessionSerializer(sessions, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def rate_message(request, message_id):
    """Rate a message as helpful or not helpful"""
    message = get_object_or_404(Message, id=message_id)
    is_helpful = request.data.get('is_helpful')
    
    if is_helpful is not None:
        message.is_helpful = is_helpful
        message.save()
        return Response({'status': 'success'})
    
    return Response({'error': 'is_helpful field is required'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_knowledge_base(request):
    """Get all knowledge base entries"""
    entries = KnowledgeBaseEntry.objects.filter(is_active=True)
    serializer = KnowledgeBaseEntrySerializer(entries, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def add_knowledge_entry(request):
    """Add a new knowledge base entry"""
    serializer = KnowledgeBaseEntrySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def search_knowledge(request):
    """Search knowledge base entries"""
    query = request.GET.get('q', '')
    if not query:
        return Response({'error': 'Query parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    entries = KnowledgeBaseEntry.objects.filter(
        is_active=True
    ).filter(
        models.Q(title__icontains=query) | 
        models.Q(content__icontains=query) |
        models.Q(keywords__icontains=query)
    )
    
    serializer = KnowledgeBaseEntrySerializer(entries, many=True)
    return Response(serializer.data)
