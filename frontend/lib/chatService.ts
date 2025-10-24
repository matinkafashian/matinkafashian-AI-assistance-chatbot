import axios from 'axios'
import { ChatResponse, ChatSession } from '@/types/chat'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

class ChatService {
  private api = axios.create({
    baseURL: `${API_BASE_URL}/api/chatbot`,
    headers: {
      'Content-Type': 'application/json',
    },
  })

  async createSession(language: 'en' | 'fa' = 'en'): Promise<string> {
    try {
      const response = await this.api.post('/create-session/', { language })
      return response.data.session_id
    } catch (error) {
      console.error('Failed to create session:', error)
      throw error
    }
  }

  async sendMessage(message: string, sessionId: string): Promise<ChatResponse> {
    try {
      const response = await this.api.post('/send-message/', {
        message,
        session_id: sessionId,
      })
      return response.data
    } catch (error) {
      console.error('Failed to send message:', error)
      throw error
    }
  }

  async getSession(sessionId: string): Promise<ChatSession> {
    try {
      const response = await this.api.get(`/session/${sessionId}/`)
      return response.data
    } catch (error) {
      console.error('Failed to get session:', error)
      throw error
    }
  }

  async rateMessage(messageId: number, isHelpful: boolean): Promise<void> {
    try {
      await this.api.post(`/rate-message/${messageId}/`, {
        is_helpful: isHelpful,
      })
    } catch (error) {
      console.error('Failed to rate message:', error)
      throw error
    }
  }

  async getKnowledgeBase() {
    try {
      const response = await this.api.get('/knowledge/')
      return response.data
    } catch (error) {
      console.error('Failed to get knowledge base:', error)
      throw error
    }
  }

  async searchKnowledge(query: string) {
    try {
      const response = await this.api.get('/knowledge/search/', {
        params: { q: query },
      })
      return response.data
    } catch (error) {
      console.error('Failed to search knowledge:', error)
      throw error
    }
  }
}

export { ChatService }
