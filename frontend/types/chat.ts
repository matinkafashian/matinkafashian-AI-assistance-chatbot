export interface Message {
  id: string
  content: string
  type: 'user' | 'assistant' | 'system'
  timestamp: string
  responseTime?: number
  isHelpful?: boolean
  sources?: string[]
}

export interface ChatSession {
  id: number
  session_id: string
  created_at: string
  updated_at: string
  is_active: boolean
  messages: Message[]
}

export interface ChatResponse {
  response: string
  session_id: string
  message_id: number
  response_time: number
  sources?: string[]
}

export interface KnowledgeBaseEntry {
  id: number
  title: string
  content: string
  category: 'python' | 'ai' | 'course_info' | 'instructor_info' | 'general'
  keywords: string
  created_at: string
  updated_at: string
  is_active: boolean
  priority: number
}
