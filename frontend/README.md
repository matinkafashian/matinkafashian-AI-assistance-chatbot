# AI Chatbot Frontend

A Next.js-based frontend for the Matin Kafashian AI Assistant chatbot.

## Features

- Modern React with Next.js 14
- Tailwind CSS for styling
- Persian and English language support
- Real-time chat interface
- Responsive design
- TypeScript support

## Setup

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

3. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Environment Variables

- `NEXT_PUBLIC_API_URL` - Backend API URL (default: http://localhost:8000)
- `NODE_ENV` - Environment (development/production)

## Deployment

This frontend is configured for deployment on Render.com with the following settings:
- Build Command: `npm install && npm run build`
- Start Command: `npm start`

## Tech Stack

- Next.js 14
- React 18
- TypeScript
- Tailwind CSS
- Axios for API calls
- Lucide React for icons
