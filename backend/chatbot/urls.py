from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health_check, name='health_check'),
    path('send-message/', views.send_message, name='send_message'),
    path('session/<str:session_id>/', views.get_session, name='get_session'),
    path('create-session/', views.create_session, name='create_session'),
    path('sessions/', views.get_sessions, name='get_sessions'),
    path('rate-message/<int:message_id>/', views.rate_message, name='rate_message'),
    path('knowledge/', views.get_knowledge_base, name='get_knowledge_base'),
    path('knowledge/add/', views.add_knowledge_entry, name='add_knowledge_entry'),
    path('knowledge/search/', views.search_knowledge, name='search_knowledge'),
]
