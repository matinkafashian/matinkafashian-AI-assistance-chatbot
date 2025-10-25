import openai
import os
import time
import re
from typing import List, Dict, Optional, Tuple
from django.conf import settings
from .models import KnowledgeBaseEntry, ChatSession
import json

# Try to import advanced RAG service, fallback to basic if not available
try:
    from .advanced_rag_service import AdvancedRAGService
    ADVANCED_RAG_AVAILABLE = True
except ImportError:
    ADVANCED_RAG_AVAILABLE = False
    print("Advanced RAG service not available, using basic implementation")


class AIService:
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        if ADVANCED_RAG_AVAILABLE:
            self.rag_service = AdvancedRAGService()
        else:
            self.rag_service = None
        self.system_prompt = self._get_system_prompt()
        
        # Intent patterns for better understanding
        self.intent_patterns = {
            'course_info': [
                r'\b(course|class|training|program|semester|duration|schedule|pricing|cost|price|fee|tuition)\b',
                r'\b(how much|what cost|enrollment|registration|join|enroll)\b'
            ],
            'contact': [
                r'\b(contact|telegram|phone|number|email|linkedin|instagram|youtube|reach|get in touch)\b',
                r'\b(where|how to contact|contact info|contact details)\b'
            ],
            'instructor': [
                r'\b(who are you|about you|your background|experience|education|matin|instructor|teacher)\b',
                r'\b(tell me about yourself|your profile|your details)\b'
            ],
            'technical': [
                r'\b(python|programming|code|function|class|variable|ai|artificial intelligence|machine learning)\b',
                r'\b(deep learning|neural network|data science|pandas|numpy|tensorflow|pytorch)\b'
            ],
            'projects': [
                r'\b(project|portfolio|freelance|earning|money|income|client|work|job)\b',
                r'\b(yolo|computer vision|nlp|rag|saas|automation)\b'
            ],
            'support': [
                r'\b(help|support|problem|issue|question|confused|stuck|difficulty)\b',
                r'\b(how to|what is|explain|tutorial|guide|learn)\b'
            ]
        }
    
    def _get_system_prompt(self):
        """Get the comprehensive system prompt with complete academy information"""
        base_instructions = (
            "Default to concise answers. Prefer 2-5 short sentences or tight bullet points. "
            "Avoid long paragraphs and unnecessary preambles. Include links or numbers only when directly useful."
        )
        try:
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            en_path = os.path.join(project_root, 'myinfo.txt')
            with open(en_path, 'r', encoding='utf-8') as f:
                en_info = f.read()
        except Exception:
            en_info = ""
        return f"""You are the official AI assistant for Matin Kafashian AI Academy - "From Zero to AI Mastery — Learn. Build. Earn."

STYLE & LENGTH:
{base_instructions}

🎯 YOUR ROLE:
You are an intelligent, professional, and highly knowledgeable AI assistant representing Matin Kafashian AI Academy. You provide comprehensive support for Python programming, Artificial Intelligence, and course information with the highest level of accuracy and helpfulness.

Academy Information:
{en_info}

🎯 YOUR RESPONSE STYLE:
1. Be professional, encouraging, and clear
2. Keep responses brief (2-5 short sentences) unless the user asks for more
3. Use bullet points for lists; avoid long paragraphs
4. Offer a short next step when helpful
5. Maintain the academy's professional brand and values

🚫 SCOPE LIMITATIONS:
ONLY answer questions related to:
- Python programming (all levels)
- Artificial Intelligence and Machine Learning
- Matin Kafashian AI Academy courses and information
- Instructor background and expertise
- Contact information and enrollment
- Technical concepts related to programming and AI
- Career guidance and freelancing advice

For unrelated topics, politely redirect: "I'm specialized in Python programming, AI, and our academy courses. How can I help you with Python, AI concepts, or our training program instead?"

Remember: You represent a premium AI education brand. Provide exceptional service that reflects the academy's commitment to excellence and student success."""

    def _get_system_prompt_fa(self) -> str:
        """Persian system prompt loaded from myinfo-farsi.txt with concise style instructions"""
        base_instructions = (
            "پاسخ‌ها کوتاه، روشن و حرفه‌ای باشند (۲ تا ۵ جمله کوتاه یا بولت). "
            "از حاشیه‌روی خودداری کن. فقط درباره پایتون، هوش مصنوعی و اطلاعات دوره پاسخ بده."
        )
        try:
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            fa_path = os.path.join(project_root, 'myinfo-farsi.txt')
            with open(fa_path, 'r', encoding='utf-8') as f:
                fa_info = f.read()
        except Exception:
            fa_info = ""
        return f"""تو دستیار رسمی آکادمی هوش مصنوعی متین کفاشیان هستی.
{base_instructions}

اطلاعات آکادمی:
{fa_info}

قواعد:
- پاسخ را به زبان فارسی و مختصر ارائه بده.
- اگر سؤال نامرتبط بود، محترمانه به موضوعات مجاز هدایت کن.
- در صورت نیاز از بولت‌های کوتاه استفاده کن.
- برای سوالات تماس، همیشه شماره تلگرام +49 15731518417 و ایمیل kafashianmatin@gmail.com را ارائه بده.
"""

    def _get_relevant_knowledge(self, query: str, limit: int = 5) -> List[Dict]:
        """Retrieve relevant knowledge base entries"""
        # Simple keyword matching - in production, use vector search
        entries = KnowledgeBaseEntry.objects.filter(is_active=True)
        relevant_entries = []
        
        query_lower = query.lower()
        for entry in entries:
            score = 0
            if query_lower in entry.title.lower():
                score += 3
            if query_lower in entry.content.lower():
                score += 2
            if entry.keywords:
                for keyword in entry.keywords.split(','):
                    if keyword.strip().lower() in query_lower:
                        score += 1
            
            if score > 0:
                relevant_entries.append({
                    'title': entry.title,
                    'content': entry.content,
                    'category': entry.category,
                    'score': score
                })
        
        # Sort by score and return top entries
        relevant_entries.sort(key=lambda x: x['score'], reverse=True)
        return relevant_entries[:limit]

    def _is_question_in_scope(self, question: str, language: str = 'en') -> bool:
        """Check if the question is within the scope of Python/AI/course topics (EN/FA)"""
        
        # For Farsi, be much more lenient - almost any reasonable question should be in scope
        if (language or 'en').lower() == 'fa':
            # Strip question marks and normalize
            question_lower = question.lower().strip('؟?').strip()
            
            # If it's a very short question (less than 3 characters), might be incomplete
            if len(question_lower) < 3:
                return False
                
            # For Farsi, be very permissive - any reasonable question should be in scope
            # Only exclude obvious non-related questions
            excluded_patterns = [
                'سلام', 'خداحافظ', 'بای', 'خداحافظی', 'خداحافظی کردن',
                'چطوری', 'حالت چطوره', 'چطوری', 'حال شما چطوره',
                'آب و هوا', 'هوا چطوره', 'باران', 'برف', 'گرما', 'سرما',
                'سیاست', 'سیاسی', 'حکومت', 'دولت', 'انتخابات',
                'ورزش', 'فوتبال', 'بسکتبال', 'تنیس', 'والیبال',
                'موسیقی', 'آهنگ', 'خواننده', 'گروه موسیقی',
                'فیلم', 'سینما', 'بازیگر', 'کارگردان',
                'غذا', 'رستوران', 'پیتزا', 'برگر', 'ساندویچ',
                'خرید', 'فروشگاه', 'مغازه', 'بازار', 'قیمت گوشی', 'قیمت ماشین'
            ]
            
            # Check if it contains excluded patterns
            for pattern in excluded_patterns:
                if pattern in question_lower:
                    return False
            
            # For Farsi, if it's not explicitly excluded, it's in scope
            return True
        
        # English scope detection (keep existing logic)
        scope_keywords = [
            # Python & Programming
            'python', 'programming', 'code', 'function', 'class', 'variable',
            'ai', 'artificial intelligence', 'machine learning', 'deep learning',
            'neural network', 'data science', 'pandas', 'numpy', 'tensorflow',
            'pytorch', 'scikit-learn', 'opencv', 'nlp', 'computer vision',
            
            # Course & Training
            'course', 'class', 'training', 'lesson', 'tutorial', 'matin',
            'instructor', 'teacher', 'enrollment', 'registration', 'pricing',
            'price', 'cost', 'fee', 'tuition', 'payment', 'money', 'dollar',
            'schedule', 'meeting', 'google meet', 'whatsapp', 'semester',
            'private', 'general', 'public', 'online', 'duration', 'month',
            'hour', 'session', 'beginner', 'advanced', 'scratch', 'prerequisite',
            
            # Contact Information
            'contact', 'telegram', 'phone', 'number', 'email', 'linkedin',
            'instagram', 'youtube', 'social', 'reach', 'get in touch',
            'telegram number', 'phone number', 'contact number', 'whatsapp',
            'how to contact', 'where to contact', 'contact info', 'contact details',
            
            # Instructor Information
            'who are you', 'about you', 'your background', 'your experience',
            'tell me about yourself', 'matin kafashian', 'instructor info',
            'teacher info', 'your profile', 'your details',
            
            # Projects and Work
            'projects', 'project', 'portfolio', 'freelance', 'freelancing', 'work', 'job',
            'earning', 'money', 'income', 'client', 'clients', 'yolo', 'computer vision',
            'nlp', 'rag', 'saas', 'automation', 'earning', 'earn', 'paid', 'payment',
            
            # Common question words
            'how much', 'what is', 'tell me', 'explain', 'help', 'learn',
            'teach', 'study', 'start', 'begin', 'join', 'register', 'do you have',
            'can you', 'are you', 'will you', 'can i', 'how can i'
        ]
        
        question_lower = question.lower().strip('؟?')
        
        # Check for direct keyword matches
        if any(keyword in question_lower for keyword in scope_keywords):
            return True
            
        # Additional checks for course-related questions
        course_indicators = [
            'cours', 'price', 'cost', 'fee', 'tuition', 'dollar', 'money',
            'how much', 'what cost', 'pricing', 'payment', 'semester',
            'private', 'general', 'class', 'training', 'learn', 'teach',
            'contact', 'telegram', 'phone', 'number', 'email', 'social'
        ]
        
        # Check course indicators
        if any(indicator in question_lower for indicator in course_indicators):
            return True
        
        return False

    def _recognize_intent(self, message: str) -> Tuple[str, float]:
        """Recognize user intent with confidence score"""
        message_lower = message.lower()
        intent_scores = {}
        
        for intent, patterns in self.intent_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, message_lower))
                score += matches
            intent_scores[intent] = score
        
        if not intent_scores or max(intent_scores.values()) == 0:
            return 'general', 0.0
        
        best_intent = max(intent_scores, key=intent_scores.get)
        confidence = min(intent_scores[best_intent] / 3.0, 1.0)  # Normalize to 0-1
        
        return best_intent, confidence

    def _get_contextual_response_enhancement(self, intent: str, confidence: float) -> str:
        """Get contextual enhancements based on intent"""
        enhancements = {
            'course_info': " I'd be happy to provide detailed course information and help you with enrollment!",
            'contact': " I can provide all contact details and help you get in touch with Matin Kafashian!",
            'instructor': " Let me tell you about Matin Kafashian's impressive background and expertise!",
            'technical': " I can help explain Python and AI concepts with examples and practical guidance!",
            'projects': " I can share information about our real-world projects and career opportunities!",
            'support': " I'm here to help! Let me provide you with comprehensive support and guidance!",
            'general': " I'm here to assist you with Python, AI, and our academy information!"
        }
        
        return enhancements.get(intent, enhancements['general'])

    def generate_response(self, user_message: str, session_id: str = None, language: str = 'en') -> Dict:
        """Generate AI response with advanced intent recognition and context awareness"""
        start_time = time.time()
        
        # Recognize user intent
        intent, intent_confidence = self._recognize_intent(user_message)
        contextual_enhancement = self._get_contextual_response_enhancement(intent, intent_confidence)
        
        try:
            if self.rag_service:
                # Use advanced RAG service
                enhanced_system_prompt = self.rag_service.get_enhanced_system_prompt(user_message)
                rag_result = self.rag_service.retrieve_relevant_information(user_message)
                
                # Check if question is in scope using advanced analysis
                if not rag_result['is_relevant']:
                    response = "I'm sorry, but I can only help with questions related to Python programming, Artificial Intelligence, and our course information. Please ask me about Python, AI concepts, or our training program instead."
                    return {
                        'response': response,
                        'sources': [],
                        'response_time': time.time() - start_time,
                        'in_scope': False
                    }
                
                # Prepare messages for OpenAI with enhanced context
                messages = [
                    {"role": "system", "content": enhanced_system_prompt},
                    {"role": "user", "content": user_message}
                ]
                
                # Extract sources from RAG results
                sources = [entry['title'] for entry in rag_result['relevant_entries']]
                confidence = rag_result['confidence']
                intents = rag_result['intent_analysis']['intents']
            else:
                # Fallback to basic implementation
                # Determine language from parameter or session for scope and prompts
                session_language = (language or 'en').lower()
                try:
                    if session_id:
                        sess = ChatSession.objects.get(session_id=session_id)
                        session_language = (sess.language or language or 'en').lower()
                except Exception:
                    session_language = (language or 'en').lower()

                if not self._is_question_in_scope(user_message, session_language):
                    # Determine language from session for out-of-scope reply
                    response = (
                        "متأسفم، فقط به پرسش‌های مرتبط با پایتون، هوش مصنوعی و اطلاعات دوره پاسخ می‌دهم. لطفاً سؤال خود را در این حوزه‌ها مطرح کنید." if session_language == 'fa' else
                        "I'm sorry, but I can only help with questions related to Python programming, Artificial Intelligence, and our course information. Please ask me about Python, AI concepts, or our training program instead."
                    )
                    return {
                        'response': response,
                        'sources': [],
                        'response_time': time.time() - start_time,
                        'in_scope': False
                    }
                
                # Get relevant knowledge using basic method
                relevant_knowledge = self._get_relevant_knowledge(user_message)
                
                # Build context from knowledge base
                context = ""
                sources = []
                if relevant_knowledge:
                    context = "\n\nRelevant information:\n"
                    for entry in relevant_knowledge:
                        context += f"- {entry['title']}: {entry['content'][:200]}...\n"
                        sources.append(entry['title'])
                
                # session_language already determined above

                # Prepare messages for OpenAI with enhanced context
                system_prompt = (
                    self._get_system_prompt_fa() if session_language == 'fa' else self.system_prompt
                )
                enhanced_prompt = system_prompt + context + f"\n\nUser Intent: {intent} (confidence: {intent_confidence:.2f})"
                messages = [
                    {"role": "system", "content": enhanced_prompt},
                    {"role": "user", "content": user_message}
                ]
                confidence = 0.8
                intents = [intent]
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=400,
                temperature=0.3
            )
            
            ai_response = response.choices[0].message.content
            response_time = time.time() - start_time
            
            return {
                'response': ai_response,
                'sources': sources,
                'response_time': response_time,
                'in_scope': True,
                'confidence': confidence,
                'intents': intents,
                'recognized_intent': intent,
                'intent_confidence': intent_confidence
            }
            
        except Exception as e:
            error_msg = str(e)
            if "invalid_api_key" in error_msg or "Incorrect API key" in error_msg:
                response = "I'm currently experiencing an API configuration issue. Please contact the administrator to resolve this."
            elif "rate_limit" in error_msg.lower():
                response = "I'm currently experiencing high demand. Please try again in a few moments."
            else:
                response = f"I apologize, but I'm experiencing technical difficulties. Please try again later."
            
            return {
                'response': response,
                'sources': [],
                'response_time': time.time() - start_time,
                'in_scope': True
            }
