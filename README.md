# AI Assistance Chatbot

A full-stack chatbot project with a Django REST backend and a Next.js frontend. The backend documentation describes OpenAI integration, chat sessions, a knowledge base, Persian/English support and Django Channels.

## Explore the project

- `backend/chatbot/`: API views, models, serializers and AI service code.
- `backend/chatbot_backend/`: Django settings and application entry points.
- `backend/README.md`: backend setup, environment variables and endpoint descriptions.
- `frontend/app/`: Next.js interface.
- `frontend/lib/chatService.ts`: frontend service integration.
- [Frontend demo](https://matinkafashian-ai-chatbot.vercel.app/).

The demo interface has been observed loading; end-to-end model responses, uptime and capacity have not been validated in this documentation review. This repository should be reviewed on its own contents; it is not evidence for the separate multi-channel publishing/RAG project described in the author's resume.

## Local development

Use an isolated Python environment for the backend and a compatible Node.js environment for the frontend. The original runtime combination has not been reproduced in this review.

```sh
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Before starting, review the selected Django settings and configure your own credentials. The backend README documents `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS` and `OPENAI_API_KEY`; confirm how the selected settings file reads them. Use placeholders in shared examples, never real credentials.

```sh
cd frontend
npm ci
npm run dev
```

Check the API destination in `frontend/lib/chatService.ts` before testing against your local backend. The frontend declares Next.js 14.0.4 and React 18; backend dependencies are pinned in `backend/requirements.txt`.

## Verification and limits

Start with `GET /api/chatbot/health/`, then create a session and test a message using the endpoint contracts in the backend README. A successful health response alone does not verify the model connection or response quality.

No claim is made here of unlimited usage, millions of daily requests, benchmark superiority or production readiness. A fresh setup test, documented API examples, backend connectivity check, response-quality evaluation and load test remain useful next steps. Development-server commands above are for local use, not a production deployment recipe.
