from django.core.management.base import BaseCommand
from chatbot.models import KnowledgeBaseEntry


class Command(BaseCommand):
    help = 'Populate the knowledge base with comprehensive Matin Kafashian AI Academy data'

    def handle(self, *args, **options):
        # Clear existing entries
        KnowledgeBaseEntry.objects.all().delete()
        
        # Comprehensive Knowledge Base Entries
        knowledge_entries = [
            {
                'title': 'Matin Kafashian AI Academy - Complete Brand Information',
                'content': 'Matin Kafashian AI Academy - "From Zero to AI Mastery — Learn. Build. Earn." Founded by Matin Kafashian, a Python and AI instructor with 6+ years of professional experience in AI, Computer Vision, and NLP. The academy specializes in international AI projects including real-time object detection dashboards and full end-to-end RAG and SaaS systems. Mission: Teach students practical, global-level AI skills through real projects while helping them turn knowledge into income.',
                'category': 'brand_info',
                'keywords': 'matin kafashian ai academy, brand, founder, mission, zero to ai mastery, learn build earn, python ai instructor, 6 years experience, computer vision, nlp, international projects, real projects, income generation',
                'priority': 10
            },
            {
                'title': 'Matin Kafashian - Complete Professional Profile',
                'content': 'Matin Kafashian, 35 years old, Master Degree in Computer Science from University of Tehran. 6+ years professional experience in Python programming, Machine Learning, Deep Learning, Computer Vision, NLP and RAG pipelines, AI SaaS product development. Fluent in English and Persian. Teaching style: Project-based, challenge-driven, mentorship-focused. Approach: Classes are fully practical — every concept taught through real projects, global competitions, and real freelance challenges. Students learn both the science and business side of AI.',
                'category': 'profile',
                'keywords': 'matin kafashian, 35 years old, master degree, university tehran, python programming, machine learning, deep learning, computer vision, nlp, rag, ai saas, teaching style, project-based, challenge-driven, mentorship',
                'priority': 10
            },
            {
                'title': 'Python AI Master Program - Complete Course Details',
                'content': 'Python & Artificial Intelligence Master Program: 6 months from zero to expert. Online format via Google Meet. Beginner to Advanced level. Maximum 8 students per class. Structure: 3 semesters, 10 sessions per semester, 1 hour per session. Fixed weekly sessions agreed in advance. Pricing: Private classes $250 per semester, Group classes $40 per semester. No prerequisites — starts completely from scratch. Based on international standards and W3Schools curriculum. Payment via online or direct (Telegram/WhatsApp).',
                'category': 'course_info',
                'keywords': 'python ai master program, 6 months, zero to expert, online, google meet, 3 semesters, 10 sessions, 1 hour, private 250, group 40, no prerequisites, w3schools, international standards',
                'priority': 9
            },
            {
                'title': 'Course Features and Real Projects',
                'content': 'Key features: Live coding, interactive problem-solving, real project replication (Computer Vision, NLP, Automation), freelance project simulation and earning guidance, AI career mentorship and portfolio building. Projects include: Real-time Object Detection and Analytics Dashboard (YOLO/Transformers), Text Summarization and Q&A Bot (RAG pipeline), Automated Web Data Extraction and Excel Reporting, Freelance AI SaaS project — full client workflow.',
                'category': 'projects',
                'keywords': 'live coding, interactive problem-solving, real projects, computer vision, nlp, automation, freelance simulation, career mentorship, portfolio building, object detection, yolo, transformers, text summarization, qa bot, rag pipeline, web data extraction, ai saas',
                'priority': 9
            },
            {
                'title': 'Course Outcomes and Career Support',
                'content': 'Outcomes: Master Python fundamentals, ML algorithms, deep learning frameworks. Gain confidence to work on real-world AI projects independently. Build portfolio-ready projects for freelancing and job applications. Learn how to find and deliver paid projects globally. Career support: Personal guidance on building GitHub portfolios, creating LinkedIn profiles, and finding international freelance clients. Students receive mentorship on earning their first $500–$1000 freelancing.',
                'category': 'career',
                'keywords': 'master python, ml algorithms, deep learning, real-world projects, portfolio, freelancing, jobs, paid projects, global, github, linkedin, international clients, earn 500-1000, freelancing income',
                'priority': 8
            },
            {
                'title': 'Complete Contact Information',
                'content': 'Contact Matin Kafashian: Telegram: +49 15731518417, Email: kafashianmatin@gmail.com, LinkedIn: https://www.linkedin.com/in/matinkafashian/, Instagram: python.teachr_ / hack.learning_, YouTube: https://www.youtube.com/@matinkafashian_. Timezone: Europe/Berlin. Usually replies within 24 hours. Available in English and Persian.',
                'category': 'contact_info',
                'keywords': 'contact, telegram +49 15731518417, email kafashianmatin@gmail.com, linkedin, instagram python.teachr_, hack.learning_, youtube, timezone europe berlin, reply 24 hours, english persian',
                'priority': 10
            },
            {
                'title': 'Frequently Asked Questions',
                'content': 'FAQ: Can join without programming knowledge? Yes, starts from zero. Classes online? Yes, Google Meet with live screen sharing. Available in Persian? Yes, both Persian and English. Certificate? Yes, professional certificate after completing all projects. Earn money? Yes! Last semester students work on real freelance projects. Refund policy: 7 days refund if unsatisfied. Classes recorded for absentees (30 days access).',
                'category': 'faq',
                'keywords': 'faq, no programming knowledge, starts zero, online classes, google meet, persian english, certificate, earn money, freelance projects, refund policy, 7 days',
                'priority': 8
            },
            {
                'title': 'Python Programming Fundamentals',
                'content': 'Python is a versatile programming language used for web development, data science, artificial intelligence, automation, and more. Key concepts include variables, data types, functions, classes, modules, and libraries. Python is known for its simple syntax and readability, making it ideal for beginners.',
                'category': 'python',
                'keywords': 'python, programming, fundamentals, variables, functions, classes, syntax, beginner, web development, data science',
                'priority': 7
            },
            {
                'title': 'Artificial Intelligence and Machine Learning',
                'content': 'Artificial Intelligence (AI) is the simulation of human intelligence in machines. Key areas include machine learning, deep learning, natural language processing, computer vision, and neural networks. Machine Learning enables computers to learn from experience without explicit programming. Applications range from recommendation systems to autonomous vehicles and medical diagnosis.',
                'category': 'ai',
                'keywords': 'artificial intelligence, AI, machine learning, deep learning, NLP, computer vision, neural networks, applications, supervised learning, unsupervised learning, reinforcement learning',
                'priority': 7
            },
            {
                'title': 'Career Achievements and Timeline',
                'content': '2022: Conducted AI classes with 120+ students, developed real-time traffic counting system using YOLOv8. 2023: Launched NLP RAG and computer vision SaaS products; 200+ students graduated with 4.8/5 satisfaction. 2024: Introduced "Earn with AI" mentorship, guiding students to make first $500–$1000 freelancing. 2025: Founded "Matin Kafashian AI Academy" for global online training and research collaboration.',
                'category': 'achievements',
                'keywords': 'achievements, timeline, 2022, 2023, 2024, 2025, students, yolo, saas, satisfaction, freelancing, academy, global',
                'priority': 6
            },
            {
                'title': 'Academic Resources and Tools',
                'content': 'Official GitHub Repositories: https://github.com/matinkafashian, Python Documentation: https://www.w3schools.com/python/, Machine Learning Playground: https://colab.research.google.com/, NLP & RAG Toolkit: https://huggingface.co/, Freelance Project Platforms: https://www.freelancer.com. Students get access to all resources for hands-on learning.',
                'category': 'resources',
                'keywords': 'resources, github, w3schools, colab, huggingface, freelancer, tools, documentation, playground, toolkit, platforms',
                'priority': 6
            },
            {
                'title': 'Academy Policies and Support',
                'content': 'Refund Policy: Students can request refund within first 7 days if unsatisfied. Attendance: Classes recorded, absentees can access recordings for 30 days. Behavior: Respectful communication mandatory, sharing recordings publicly prohibited. Privacy: All student information private, used only for educational purposes. Support available in English and Persian.',
                'category': 'policies',
                'keywords': 'policies, refund, attendance, behavior, privacy, support, english, persian, recordings, communication, educational',
                'priority': 5
            }
        ]
        
        # Create knowledge base entries
        for entry_data in knowledge_entries:
            KnowledgeBaseEntry.objects.create(**entry_data)
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {len(knowledge_entries)} comprehensive knowledge base entries')
        )
