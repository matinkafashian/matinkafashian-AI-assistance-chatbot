# AI Chatbot Backend

A Django-based backend service for the Matin Kafashian AI Assistant chatbot.

## Features

- Django REST Framework API
- OpenAI integration for AI responses
- Chat session management
- Knowledge base system
- WebSocket support with Django Channels
- Persian and English language support

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run migrations:
```bash
python manage.py migrate
```

3. Start the development server:
```bash
python manage.py runserver
```

## API Endpoints

- `GET /api/chatbot/health/` - Health check
- `POST /api/chatbot/create-session/` - Create new chat session
- `POST /api/chatbot/send-message/` - Send message to chatbot
- `GET /api/chatbot/session/{session_id}/` - Get chat session
- `GET /api/chatbot/knowledge/` - Get knowledge base entries
- `POST /api/chatbot/knowledge/search/` - Search knowledge base

## Environment Variables

- `SECRET_KEY` - Django secret key
- `DEBUG` - Debug mode (True/False)
- `ALLOWED_HOSTS` - Comma-separated list of allowed hosts
- `OPENAI_API_KEY` - OpenAI API key for AI responses

## Deployment

This backend is configured for deployment on Render.com with the following settings:
- Build Command: `pip install -r requirements.txt && python manage.py migrate`
- Start Command: `python manage.py runserver 0.0.0.0:$PORT`

