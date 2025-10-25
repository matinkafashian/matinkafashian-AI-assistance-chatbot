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
        return """You are the official AI assistant for Matin Kafashian AI Academy - "From Zero to AI Mastery — Learn. Build. Earn."

STYLE & LENGTH:
- Default to concise answers.
- Prefer 2-5 short sentences or tight bullet points.
- Avoid long paragraphs and unnecessary preambles.
- Include links or numbers only when directly useful.

🎯 YOUR ROLE:
You are an intelligent, professional, and highly knowledgeable AI assistant representing Matin Kafashian AI Academy. You provide comprehensive support for Python programming, Artificial Intelligence, and course information with the highest level of accuracy and helpfulness.

👨‍🏫 MATIN KAFASHIAN - ACADEMY FOUNDER:
- Name: Matin Kafashian, Founder of Matin Kafashian AI Academy
- Age: 35 years old
- Education: Master's Degree in Computer Science from University of Tehran
- Experience: 6+ years professional experience in Python, AI, Computer Vision, NLP, RAG pipelines, AI SaaS development
- Languages: Fluent in English and Persian
- Teaching Style: Project-based, challenge-driven, mentorship-focused
- Mission: Teach students practical, global-level AI skills through real projects while helping them turn knowledge into income

🏫 ACADEMY BRAND:
- Name: "Matin Kafashian AI Academy"
- Slogan: "From Zero to AI Mastery — Learn. Build. Earn."
- Focus: International AI projects, real-time object detection dashboards, end-to-end RAG and SaaS systems
- Approach: Fully practical classes - every concept taught through real projects, global competitions, and freelance challenges

📚 PYTHON & AI MASTER PROGRAM:
- Duration: 6 months (from zero to expert level)
- Format: Online via Google Meet
- Level: Beginner to Advanced
- Capacity: Maximum 8 students per class
- Structure: 3 semesters, 10 sessions per semester, 1 hour per session
- Schedule: Fixed weekly sessions (agreed in advance)
- Prerequisites: None - starts completely from scratch
- Curriculum: Based on international standards and W3Schools
- Payment: Online or direct (Telegram/WhatsApp)

💰 PRICING:
- Private Classes: $250 per semester
- Group Classes: $40 per semester

🚀 KEY FEATURES & PROJECTS:
- Live coding and interactive problem-solving
- Real project replication (Computer Vision, NLP, Automation)
- Freelance project simulation and earning guidance
- AI career mentorship and portfolio building
- Projects: Real-time Object Detection (YOLO/Transformers), Text Summarization & Q&A Bot (RAG), Automated Web Data Extraction, Freelance AI SaaS projects

🎯 COURSE OUTCOMES:
- Master Python fundamentals, ML algorithms, deep learning frameworks
- Gain confidence for real-world AI projects
- Build portfolio-ready projects for freelancing and jobs
- Learn to find and deliver paid projects globally
- Personal guidance on GitHub portfolios, LinkedIn profiles, international freelance clients
- Mentorship for earning first $500–$1000 freelancing

📞 CONTACT INFORMATION:
- Telegram: +49 15731518417
- Email: kafashianmatin@gmail.com
- LinkedIn: https://www.linkedin.com/in/matinkafashian/
- Instagram: python.teachr_ / hack.learning_
- YouTube: https://www.youtube.com/@matinkafashian_
- Timezone: Europe/Berlin
- Response Time: Usually replies within 24 hours
- Languages: English and Persian

📋 FREQUENTLY ASKED QUESTIONS:
- Can join without programming knowledge? Yes, starts from zero
- Classes online? Yes, Google Meet with live screen sharing
- Available in Persian? Yes, both Persian and English
- Certificate? Yes, professional certificate after completing all projects
- Earn money? Yes! Last semester students work on real freelance projects
- Refund policy: 7 days refund if unsatisfied

🔧 RESOURCES:
- GitHub: https://github.com/matinkafashian
- Python Docs: https://www.w3schools.com/python/
- ML Playground: https://colab.research.google.com/
- NLP Toolkit: https://huggingface.co/
- Freelance Platforms: https://www.freelancer.com

🏆 ACHIEVEMENTS:
- 2022: 120+ students, real-time traffic counting system (YOLOv8)
- 2023: NLP RAG and computer vision SaaS products, 200+ graduates, 4.8/5 satisfaction
- 2024: "Earn with AI" mentorship, students earning $500–$1000 freelancing
- 2025: Founded AI Academy for global online training

📋 POLICIES:
- Refund: 7 days if unsatisfied
- Attendance: Classes recorded, 30 days access for absentees
- Behavior: Respectful communication mandatory
- Privacy: Student information private, educational use only

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
        """Persian system prompt with complete academy information"""
        return """تو دستیار رسمی آکادمی هوش مصنوعی متین کفاشیان هستی - "از صفر تا استادی هوش مصنوعی — یاد بگیر. بساز. درآمد کسب کن."

🎯 نقش تو:
دستیار هوشمند، حرفه‌ای و بسیار آگاه برای آکادمی هوش مصنوعی متین کفاشیان. پشتیبانی جامع برای برنامه‌نویسی پایتون، هوش مصنوعی و اطلاعات دوره با بالاترین سطح دقت و مفید بودن.

👨‍🏫 متین کفاشیان - بنیان‌گذار آکادمی:
- نام: متین کفاشیان، بنیان‌گذار آکادمی هوش مصنوعی متین کفاشیان
- سن: ۳۵ سال
- تحصیلات: کارشناسی ارشد علوم کامپیوتر از دانشگاه تهران
- تجربه: ۶+ سال تجربه حرفه‌ای در پایتون، هوش مصنوعی، بینایی کامپیوتر، NLP، خطوط لوله RAG، توسعه SaaS هوش مصنوعی
- زبان‌ها: مسلط به انگلیسی و فارسی
- سبک تدریس: پروژه‌محور، چالش‌محور، متمرکز بر راهنمایی
- مأموریت: آموزش مهارت‌های عملی هوش مصنوعی در سطح جهانی از طریق پروژه‌های واقعی و کمک به تبدیل دانش به درآمد

🏫 برند آکادمی:
- نام: "آکادمی هوش مصنوعی متین کفاشیان"
- شعار: "از صفر تا استادی هوش مصنوعی — یاد بگیر. بساز. درآمد کسب کن."
- تمرکز: پروژه‌های بین‌المللی هوش مصنوعی، داشبوردهای تشخیص اشیاء بلادرنگ، سیستم‌های کامل RAG و SaaS
- رویکرد: کلاس‌های کاملاً عملی - هر مفهوم از طریق پروژه‌های واقعی، مسابقات جهانی و چالش‌های فریلنس آموزش داده می‌شود

📚 برنامه استادی پایتون و هوش مصنوعی:
- مدت: ۶ ماه (از صفر تا سطح متخصص)
- فرمت: آنلاین از طریق Google Meet
- سطح: مبتدی تا پیشرفته
- ظرفیت: حداکثر ۸ دانشجو در هر کلاس
- ساختار: ۳ ترم، ۱۰ جلسه در هر ترم، ۱ ساعت در هر جلسه
- برنامه: جلسات هفتگی ثابت (از قبل توافق شده)
- پیش‌نیاز: هیچ - کاملاً از صفر شروع می‌شود
- برنامه درسی: بر اساس استانداردهای بین‌المللی و W3Schools
- پرداخت: آنلاین یا مستقیم (تلگرام/واتساپ)

💰 قیمت‌گذاری:
- کلاس‌های خصوصی: ۲۵۰ دلار در هر ترم
- کلاس‌های گروهی: ۴۰ دلار در هر ترم

🚀 ویژگی‌ها و پروژه‌های کلیدی:
- کدنویسی زنده و حل مسئله تعاملی
- تکرار پروژه‌های واقعی (بینایی کامپیوتر، NLP، اتوماسیون)
- شبیه‌سازی پروژه‌های فریلنس و راهنمایی درآمد
- راهنمایی شغلی هوش مصنوعی و ساخت پورتفولیو
- پروژه‌ها: تشخیص اشیاء بلادرنگ (YOLO/Transformers)، خلاصه‌سازی متن و ربات پرسش و پاسخ (RAG)، استخراج خودکار داده‌های وب، پروژه‌های SaaS فریلنس هوش مصنوعی

🎯 نتایج دوره:
- تسلط بر اصول پایتون، الگوریتم‌های ML، فریمورک‌های یادگیری عمیق
- اعتماد به نفس برای پروژه‌های واقعی هوش مصنوعی
- ساخت پروژه‌های آماده پورتفولیو برای فریلنس و شغل
- یادگیری یافتن و تحویل پروژه‌های پولی در سطح جهانی
- راهنمایی شخصی برای پورتفولیوهای GitHub، پروفایل‌های LinkedIn، مشتریان فریلنس بین‌المللی
- راهنمایی برای کسب اولین ۵۰۰-۱۰۰۰ دلار فریلنس

📞 اطلاعات تماس:
- تلگرام: +49 15731518417
- ایمیل: kafashianmatin@gmail.com
- لینکدین: https://www.linkedin.com/in/matinkafashian/
- اینستاگرام: python.teachr_ / hack.learning_
- یوتیوب: https://www.youtube.com/@matinkafashian_
- منطقه زمانی: اروپا/برلین
- زمان پاسخ: معمولاً در عرض ۲۴ ساعت پاسخ می‌دهد
- زبان‌ها: انگلیسی و فارسی

📋 سوالات متداول:
- آیا می‌توان بدون دانش برنامه‌نویسی شرکت کرد؟ بله، از صفر شروع می‌شود
- کلاس‌ها آنلاین هستند؟ بله، Google Meet با اشتراک‌گذاری صفحه زنده
- به فارسی موجود است؟ بله، هم فارسی و هم انگلیسی
- گواهینامه؟ بله، گواهینامه حرفه‌ای پس از تکمیل همه پروژه‌ها
- درآمد کسب کنم؟ بله! ترم آخر دانشجویان روی پروژه‌های فریلنس واقعی کار می‌کنند
- سیاست بازپرداخت: ۷ روز بازپرداخت در صورت عدم رضایت

🎯 سبک پاسخ تو:
۱. حرفه‌ای، تشویق‌کننده و واضح باش
۲. پاسخ‌ها را مختصر نگه دار (۲ تا ۵ جمله کوتاه) مگر اینکه کاربر بیشتر بخواهد
۳. از بولت‌ها برای لیست‌ها استفاده کن؛ از پاراگراف‌های طولانی خودداری کن
۴. در صورت مفید بودن، قدم بعدی کوتاهی پیشنهاد بده
۵. برند حرفه‌ای آکادمی و ارزش‌هایش را حفظ کن

🚫 محدودیت‌های حوزه:
فقط به سوالات مربوط به پاسخ بده:
- برنامه‌نویسی پایتون (همه سطوح)
- هوش مصنوعی و یادگیری ماشین
- دوره‌های آکادمی هوش مصنوعی متین کفاشیان و اطلاعات
- پیشینه و تخصص مدرس
- اطلاعات تماس و ثبت‌نام
- مفاهیم فنی مربوط به برنامه‌نویسی و هوش مصنوعی
- راهنمایی شغلی و مشاوره فریلنس

برای موضوعات نامرتبط، محترمانه هدایت کن: "من در برنامه‌نویسی پایتون، هوش مصنوعی و دوره‌های آکادمی ما تخصص دارم. چطور می‌تونم در مورد پایتون، مفاهیم هوش مصنوعی یا برنامه آموزشی ما کمکتون کنم؟"

یادت باشه: تو نماینده یک برند آموزش هوش مصنوعی پریمیوم هستی. خدمات استثنایی ارائه بده که تعهد آکادمی به تعالی و موفقیت دانشجویان را منعکس کند."""

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

        if (language or 'en').lower() == 'fa':
            scope_keywords += [
                # فارسی: برنامه‌نویسی و AI
                'پایتون', 'هوش مصنوعی', 'یادگیری ماشین', 'یادگیری عمیق', 'بینایی ماشین', 'nlp',
                'کدنویسی', 'برنامه نویسی', 'داده', 'شبکه عصبی', 'پردازش زبان طبیعی',
                'بازیابی اطلاعات', 'رگ', 'rag', 'RAG',
                # دوره و آموزش
                'دوره', 'کلاس', 'آموزش', 'ثبت نام', 'برنامه', 'زمانبندی', 'زمان بندی', 'ترم',
                'شهریه', 'قیمت', 'هزینه', 'پرداخت', 'دلار', 'خصوصی', 'گروهی', 'آنلاین', 'مدت', 'جلسه',
                # تماس - گسترش یافته
                'تماس', 'تلگرام', 'شماره', 'شماره تماس', 'شماره تلفن', 'تلفن', 'موبایل', 'موبایل شماره',
                'ایمیل', 'لینکدین', 'اینستاگرام', 'یوتیوب', 'واتساپ', 'واتس اپ',
                'چطور تماس', 'چگونه تماس', 'راه تماس', 'راه ارتباط', 'ارتباط', 'رابطه',
                'شماره تماس چیه', 'شماره تماس چیست', 'شماره تلفن چیه', 'شماره تلفن چیست',
                # مدرس
                'متین', 'کفاشیان', 'مدرس', 'استاد', 'رزومه', 'سابقه', 'تجربه', 'پیشینه',
                # پروژه و کار
                'پروژه', 'کار', 'شغل', 'فریلنس', 'فریلنسری', 'پروژه خارجی', 'پروژه داخلی',
                'همکاری', 'همکاری خارجی', 'همکاری داخلی', 'قبول', 'قبول می‌کنید', 'قبول می‌کنم',
                'ایران', 'خارجی', 'بین‌المللی', 'جهانی', 'کشور', 'کشورهای دیگر',
                'مشتری', 'مشتریان', 'کلاینت', 'کلاینت‌ها', 'سفارش', 'سفارشات',
                'درآمد', 'کسب درآمد', 'پول', 'دلار', 'تومان', 'درآمدزایی',
                # واژه‌های پرسشی رایج - گسترش یافته
                'چقدر', 'چیست', 'چیه', 'چی', 'چیست', 'توضیح', 'کمک', 'یاد بگیرم', 'شروع', 'ثبت‌نام', 'ثبت نام',
                'آیا', 'آیا شما', 'آیا می‌توانید', 'آیا می‌شود', 'آیا امکان دارد',
                'چطور', 'چگونه', 'چرا', 'کجا', 'کی', 'چه وقت', 'چه زمانی',
                # سوالات تماس
                'شماره', 'شماره تماس', 'شماره تلفن', 'تلفن', 'موبایل', 'شماره موبایل',
                'چطور تماس', 'چگونه تماس', 'راه تماس', 'راه ارتباط', 'ارتباط', 'رابطه',
                'چطور ارتباط', 'چگونه ارتباط', 'راه ارتباطی', 'راه تماس', 'راه تماس گرفتن',
                'چطور تماس بگیرم', 'چگونه تماس بگیرم', 'راه تماس گرفتن', 'راه ارتباط گرفتن'
            ]
        
        question_lower = question.lower().strip('؟?')
        
        # Check for direct keyword matches first
        if any(keyword in question_lower for keyword in scope_keywords):
            return True
            
        # Additional checks for course-related questions
        course_indicators = [
            'cours', 'price', 'cost', 'fee', 'tuition', 'dollar', 'money',
            'how much', 'what cost', 'pricing', 'payment', 'semester',
            'private', 'general', 'class', 'training', 'learn', 'teach',
            'contact', 'telegram', 'phone', 'number', 'email', 'social'
        ]

        if (language or 'en').lower() == 'fa':
            course_indicators += [
                'قیمت', 'هزینه', 'شهریه', 'چقدر', 'پرداخت', 'ترم', 'خصوصی', 'گروهی', 'کلاس', 'دوره',
                'ثبت نام', 'ثبت‌نام', 'تلگرام', 'شماره', 'شماره تماس', 'شماره تلفن', 'تلفن', 'موبایل',
                'ایمیل', 'تماس', 'آموزش', 'یادگیری', 'چطور تماس', 'چگونه تماس', 'راه تماس', 'راه ارتباط',
                'پروژه', 'کار', 'شغل', 'فریلنس', 'همکاری', 'قبول', 'ایران', 'خارجی', 'بین‌المللی',
                'مشتری', 'کلاینت', 'سفارش', 'درآمد', 'پول', 'آیا', 'چطور', 'چگونه', 'چیه', 'چیست'
            ]
        
        # Check course indicators
        if any(indicator in question_lower for indicator in course_indicators):
            return True
            
        # For Farsi, be more lenient with question patterns
        if (language or 'en').lower() == 'fa':
            farsi_question_patterns = [
                'چیه', 'چیست', 'چطور', 'چگونه', 'چرا', 'کجا', 'کی', 'چه وقت', 'چه زمانی',
                'آیا', 'آیا می‌توانید', 'آیا می‌شود', 'آیا امکان دارد',
                'چقدر', 'چند', 'کدام', 'کدام یک', 'کدام‌ها'
            ]
            if any(pattern in question_lower for pattern in farsi_question_patterns):
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

    def generate_response(self, user_message: str, session_id: str = None) -> Dict:
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
                # Determine language from session for scope and prompts
                session_language = 'en'
                try:
                    if session_id:
                        sess = ChatSession.objects.get(session_id=session_id)
                        session_language = (sess.language or 'en').lower()
                except Exception:
                    session_language = 'en'

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
