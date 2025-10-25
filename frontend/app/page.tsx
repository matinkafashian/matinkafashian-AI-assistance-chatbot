'use client'

import { useState, useEffect, useRef } from 'react'
import { Send, Loader2, ExternalLink, Copy, Check } from 'lucide-react'
import { ChatService } from '@/lib/chatService'
import { Message } from '@/types/chat'

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([])
  const [inputMessage, setInputMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [language, setLanguage] = useState<'en' | 'fa'>('en')
  const [copiedMessageId, setCopiedMessageId] = useState<string | null>(null)
  const [isLangOpen, setIsLangOpen] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const chatService = useRef(new ChatService())

  useEffect(() => {
    // Initialize chat session
    const initSession = async () => {
      try {
        const newSessionId = await chatService.current.createSession(language)
        setSessionId(newSessionId)
        
        // Add welcome message
        setMessages([{
          id: 'welcome',
          content: language === 'fa'
            ? 'سلام! من دستیار هوش مصنوعی متین کفاشیان هستم. می‌تونم در برنامه‌نویسی پایتون، مفاهیم هوش مصنوعی و اطلاعات دوره‌هام کمک‌تون کنم. از کجا شروع کنیم؟'
            : "Hello! I'm Matin Kafashian AI assistant. I can help you with Python programming, AI concepts, and my course information. How can I assist you today?",
          type: 'assistant',
          timestamp: new Date().toISOString(),
          responseTime: 0
        }])
      } catch (error) {
        console.error('Failed to initialize session:', error)
      }
    }

    initSession()
  }, [language])

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const handleSendMessage = async () => {
    console.log('handleSendMessage called:', { inputMessage, isLoading, sessionId, language })
    if (!inputMessage.trim() || isLoading || !sessionId) {
      console.log('Message not sent:', { hasMessage: !!inputMessage.trim(), isLoading, hasSession: !!sessionId })
      return
    }

    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputMessage,
      type: 'user',
      timestamp: new Date().toISOString(),
      responseTime: 0
    }

    setMessages(prev => [...prev, userMessage])
    setInputMessage('')
    setIsLoading(true)

    try {
      console.log('Sending message to backend:', inputMessage)
      const response = await chatService.current.sendMessage(inputMessage, sessionId)
      console.log('Backend response:', response)
      
      const assistantMessage: Message = {
        id: response.message_id.toString(),
        content: response.response,
        type: 'assistant',
        timestamp: new Date().toISOString(),
        responseTime: response.response_time,
        sources: response.sources
      }

      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      console.error('Failed to send message:', error)
      const errorMessage: Message = {
        id: Date.now().toString(),
        content: language === 'fa' ? "متأسفم، خطایی رخ داد. لطفاً دوباره تلاش کنید." : "I'm sorry, I encountered an error. Please try again.",
        type: 'assistant',
        timestamp: new Date().toISOString(),
        responseTime: 0
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  const handleCopyMessage = async (messageId: string, content: string) => {
    try {
      await navigator.clipboard.writeText(content)
      setCopiedMessageId(messageId)
      setTimeout(() => setCopiedMessageId(null), 2000)
    } catch (err) {
      console.error('Failed to copy message:', err)
    }
  }

  const extractLinks = (text: string) => {
    const urlRegex = /(https?:\/\/[^\s]+)/g
    return text.split(urlRegex).map((part, index) => {
      if (urlRegex.test(part)) {
        return (
          <a
            key={index}
            href={part}
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-300 hover:text-blue-200 underline break-all"
            style={{ wordBreak: 'break-all' }}
          >
            {part}
          </a>
        )
      }
      return part
    })
  }

  const handleLanguageChange = async (lang: 'en' | 'fa') => {
    if (language === lang) return
    setLanguage(lang)
    // Clear previous chat and start fresh session; init effect will create new session
    setMessages([])
    setSessionId(null)
  }

  // Close language selector when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (isLangOpen && !(event.target as Element).closest('.language-selector')) {
        setIsLangOpen(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [isLangOpen])

  return (
    <div className={`min-h-screen flex items-center justify-center p-4 relative z-10 ${language === 'fa' ? 'rtl' : ''}`} dir={language === 'fa' ? 'rtl' : 'ltr'}>
      {/* Main Chat Container */}
      <div className="w-full max-w-4xl mx-auto">
        {/* Language Selector - Top Right */}
        <div className="fixed top-1 right-1 sm:top-4 sm:right-4 md:top-6 md:right-6 z-50 language-selector">
          <div className="relative">
            <button
              onClick={() => setIsLangOpen(!isLangOpen)}
              className="flex items-center gap-1 md:gap-3 px-1.5 md:px-6 py-1 md:py-4 bg-white/95 backdrop-blur-md rounded-2xl shadow-2xl hover:shadow-3xl hover:bg-white transition-all duration-300 border border-gray-200/50 min-w-[80px] md:min-w-[180px]"
            >
              <span className="text-sm md:text-3xl">
                {language === 'en' ? '🇺🇸' : '🇮🇷'}
              </span>
              <span className="font-bold text-xs md:text-lg">
                {language === 'en' ? 'English' : 'فارسی'}
              </span>
              <svg 
                className={`w-3 h-3 md:w-5 md:h-5 transition-transform duration-200 ${isLangOpen ? 'rotate-180' : ''}`} 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            </button>
            
            {isLangOpen && (
              <div className="absolute top-full right-0 mt-3 bg-white/98 backdrop-blur-md rounded-2xl shadow-2xl overflow-hidden min-w-[100px] md:min-w-[180px] border border-gray-200/50">
                <button
                  onClick={() => { handleLanguageChange('en'); setIsLangOpen(false) }}
                  className={`w-full flex items-center gap-2 md:gap-4 px-2 md:px-6 py-2 md:py-4 hover:bg-blue-50 transition-all duration-200 ${language === 'en' ? 'bg-blue-100' : ''}`}
                >
                  <span className="text-xl md:text-2xl">🇺🇸</span>
                  <span className="font-bold text-base md:text-lg">English</span>
                  {language === 'en' && <span className="ml-auto text-blue-600">✓</span>}
                </button>
                <div className="border-t border-gray-200/50"></div>
                <button
                  onClick={() => { handleLanguageChange('fa'); setIsLangOpen(false) }}
                  className={`w-full flex items-center gap-2 md:gap-4 px-2 md:px-6 py-2 md:py-4 hover:bg-blue-50 transition-all duration-200 ${language === 'fa' ? 'bg-blue-100' : ''}`}
                >
                  <span className="text-xl md:text-2xl">🇮🇷</span>
                  <span className="font-bold text-base md:text-lg">فارسی</span>
                  {language === 'fa' && <span className="ml-auto text-blue-600">✓</span>}
                </button>
              </div>
            )}
          </div>
        </div>

        {/* Header */}
        <div className="text-center mb-8 pt-20 sm:pt-24 md:pt-28 lg:pt-32">
          <h1 className="text-xl sm:text-2xl md:text-3xl lg:text-4xl font-bold text-gray-800 mb-2 px-4">
            {language === 'fa' ? 'دستیار هوش مصنوعی متین کفاشیان' : 'Matin Kafashian AI Assistant'}
          </h1>
        </div>

        {/* Chat Box */}
        <div className="bg-white/90 backdrop-blur-sm rounded-3xl shadow-2xl overflow-hidden">
          {/* Message Area */}
          <div className="h-96 md:h-[500px] overflow-y-auto p-6 space-y-4">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${
                  language === 'fa' 
                    ? (message.type === 'user' ? 'justify-start' : 'justify-end')
                    : (message.type === 'user' ? 'justify-end' : 'justify-start')
                } message-fade-in`}
              >
                <div
                  className={`max-w-[80%] rounded-2xl px-4 py-3 pr-12 break-words relative ${
                    message.type === 'user'
                      ? 'bg-gray-100 text-black'
                      : 'bg-gradient-to-r from-purple-500 to-blue-500 text-white'
                  }`}
                  style={{ borderRadius: '16px', wordWrap: 'break-word', overflowWrap: 'break-word' }}
                >
                  <div className={`flex items-start justify-between gap-2 ${language === 'fa' ? 'flex-row-reverse' : ''}`}>
                    <div className="flex-1">
                      <p className={`whitespace-pre-wrap text-base md:text-lg break-words ${language === 'fa' ? 'text-right' : 'text-left'}`} dir={language === 'fa' ? 'rtl' : 'ltr'} style={{ wordWrap: 'break-word', overflowWrap: 'break-word' }}>
                        {message.type === 'assistant' ? extractLinks(message.content) : message.content}
                      </p>
                      
                      {/* Show sources if available */}
                      {message.sources && message.sources.length > 0 && (
                        <div className={`mt-2 opacity-75 ${language === 'fa' ? 'text-right text-sm font-bold' : 'text-left text-xs'}`}>
                          <p>📚 {language === 'fa' ? 'منابع:' : 'Sources:'} {message.sources.join(', ')}</p>
                        </div>
                      )}
                      
                    </div>
                    
                    {/* Copy button for assistant messages */}
                    {message.type === 'assistant' && message.id !== 'welcome' && (
                      <button
                        onClick={() => handleCopyMessage(message.id, message.content)}
                        className="opacity-60 hover:opacity-100 transition-opacity p-1 rounded absolute top-2 right-2"
                        title={language === 'fa' ? 'کپی پیام' : 'Copy message'}
                      >
                        {copiedMessageId === message.id ? (
                          <Check className="w-4 h-4" />
                        ) : (
                          <Copy className="w-4 h-4" />
                        )}
                      </button>
                    )}
                  </div>
                </div>
              </div>
            ))}
            
            {/* Enhanced Loading indicator */}
            {isLoading && (
              <div className={`flex message-fade-in ${language === 'fa' ? 'justify-end' : 'justify-start'}`}>
                <div className="bg-gradient-to-r from-purple-500 to-blue-500 text-white rounded-2xl px-4 py-3 max-w-[80%]">
                  <div className={`flex items-center ${language === 'fa' ? 'gap-2' : 'gap-2'}`}>
                    <div className={`flex items-center ${language === 'fa' ? 'gap-1' : 'gap-1'}`}>
                      <div className="w-2 h-2 bg-white rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                      <div className="w-2 h-2 bg-white rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                      <div className="w-2 h-2 bg-white rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                    </div>
                    <span className={`opacity-75 ${language === 'fa' ? 'text-sm font-bold' : 'text-xs'}`}>
                      {language === 'fa' ? 'هوش مصنوعی در حال فکر کردن...' : 'AI is thinking...'}
                    </span>
                  </div>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>

          {/* Enhanced Input Area */}
          <div className="border-t border-gray-200 bg-gray-50/50 p-4">
            <div className={`flex items-center ${language === 'fa' ? 'flex-row-reverse gap-3' : 'gap-3'}`}>
              <div className="flex-1 relative">
                <input
                  type="text"
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder={language === 'fa' ? 'درباره پایتون، هوش مصنوعی یا دوره‌هام بپرسید...' : "Ask me about Python, AI, or our courses..."}
                  className={`w-full px-4 py-3 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200 ${language === 'fa' ? 'text-lg font-bold' : ''}`}
                  disabled={isLoading}
                  dir={language === 'fa' ? 'rtl' : 'ltr'}
                />
                {inputMessage.trim() && (
                  <div className={`absolute top-1/2 transform -translate-y-1/2 text-xs text-gray-400 ${language === 'fa' ? 'left-3' : 'right-3'}`}>
                    {inputMessage.length}/500
                  </div>
                )}
              </div>
              <button
                onClick={handleSendMessage}
                disabled={!inputMessage.trim() || isLoading}
                className="bg-gradient-to-r from-purple-500 to-blue-500 text-white w-12 h-12 rounded-full hover:from-purple-600 hover:to-blue-600 disabled:opacity-50 disabled:cursor-not-allowed send-button-glow transition-all duration-200 relative flex items-center justify-center"
              >
                {isLoading ? (
                  <Loader2 className="w-5 h-5 animate-spin" />
                ) : (
                  <Send className="w-5 h-5" />
                )}
              </button>
            </div>
            
            {/* Quick suggestions */}
            <div className={`mt-2 flex flex-wrap gap-2 ${language === 'fa' ? 'justify-end' : 'justify-start'}`}>
              {(language === 'fa' ? [
                "قیمت دوره چقدره؟",
                "شماره تماس شما چیه؟",
                "دوره هوش مصنوعی؟",
                "پروژه‌های AI؟"
              ] : [
                "Course pricing?",
                "Contact info?",
                "AI course?",
                "AI projects?"
              ]).map((suggestion, index) => (
                <button
                  key={index}
                  onClick={() => setInputMessage(suggestion)}
                  className="px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded-full transition-colors text-xs sm:text-sm"
                  disabled={isLoading}
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

