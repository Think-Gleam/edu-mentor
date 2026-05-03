<div align="center">

# 🎓 EduMentor

### *Your Intelligent AI Learning Companion — Personalized, Voice-Enabled, and Built for Every Student*

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.57-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![CrewAI](https://img.shields.io/badge/CrewAI-Multi--Agent-6C63FF)](https://crewai.com)
[![Google Gemini](https://img.shields.io/badge/Google-Gemini%202.5%20Flash-4285F4?logo=google&logoColor=white)](https://deepmind.google/technologies/gemini/)
[![Supabase](https://img.shields.io/badge/Supabase-Database-3ECF8E?logo=supabase&logoColor=white)](https://supabase.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![HEC Gen-AI Hackathon](https://img.shields.io/badge/HEC-Gen--AI%20Hackathon%202025-green)](https://hec.gov.pk)
[![SDG 4](https://img.shields.io/badge/UN%20SDG-Quality%20Education%20%234-red)](https://sdgs.un.org/goals/goal4)

**Making quality education accessible to every student in Pakistan — from primary school to university.**

[🚀 Live Demo](#live-demo) · [📸 Screenshots](#screenshots) · [⚡ Quick Start](#how-to-run-locally) · [🤝 Team](#contributors)

</div>

---

## 🌟 Live Demo

> 🔗 **[https://edu-mentor.streamlit.app](https://edu-mentor.streamlit.app)** *(link placeholder — replace with your deployed URL)*

---

## 📸 Screenshots

<div align="center">

| Dashboard | AI Tutor Chat | Adaptive Quiz |
|:---------:|:-------------:|:-------------:|
| ![Dashboard](docs/screenshots/dashboard.png) | ![AI Tutor](docs/screenshots/tutor_chat.png) | ![Quiz](docs/screenshots/quiz.png) |
| *Personalized student dashboard* | *Conversational AI teacher* | *Adaptive difficulty quizzes* |

| Study Plan | Progress Tracker | Voice Lesson |
|:----------:|:----------------:|:------------:|
| ![Study Plan](docs/screenshots/study_plan.png) | ![Progress](docs/screenshots/progress.png) | ![Voice](docs/screenshots/voice_lesson.png) |
| *AI-generated weekly study plan* | *Mastery & performance analytics* | *ElevenLabs voice-enabled lessons* |

> 📌 *Replace the image paths above with actual screenshots once available.*

</div>

---

## ✨ Key Features

### 🤖 Agentic AI System
- **4 Specialized AI Agents** (Planner, Teacher, Quiz Master, Evaluator) working in concert via CrewAI
- Agents collaborate to deliver a complete, end-to-end learning experience
- Intelligent task delegation and autonomous decision-making

### 📚 Adaptive Learning
- **Level-aware personalization** — content automatically adjusts for Grade 5 through university
- Dynamic difficulty scaling based on real-time performance
- Smart progress tracking with mastery thresholds (75% to advance)

### 🗣️ Voice-Enabled Lessons
- **ElevenLabs TTS** for natural, high-quality text-to-speech
- **Azure Neural Voices** as a fallback (English & Urdu voices)
- Browser Web Speech API as a final fallback — works everywhere
- Urdu-language voice support (`ur-PK-UzmaNeural`)

### 🌍 Bilingual Support (Urdu + English)
- Full platform available in English, Urdu, and bilingual mode
- Real Pakistani examples, cities, and cultural references in all lessons
- Curriculum aligned with Federal, Punjab, Sindh, and other local boards

### 📝 Adaptive Quizzes
- Multiple-choice and short-answer question generation
- Per-question explanations and detailed feedback
- Performance-based difficulty adjustment
- Identification of knowledge gaps and struggle patterns

### 📊 Progress & Analytics
- Mastery level tracking (0–1 scale per topic)
- Risk detection — flags students who are struggling
- Personalized intervention recommendations (repeat, simplify, advance)
- Full history stored in Supabase

### 🔐 Secure User Authentication
- Supabase-powered sign-up and login
- Two-phase onboarding: basic info + learning profile
- 15+ profile fields (age, board, language, interests, city)
- UPSERT-safe — no duplicate accounts

### 🏫 Pakistan-First Design
- Curriculum knowledge of Pakistani education boards
- Local examples: cities, traditions, daily life
- Student types: kids, school students, university, professionals, parents

---

## 🧠 Adaptive Learning Approach

EduMentor uses a **multi-layered adaptation engine** to personalize the learning experience:

```
Student Profile
      │
      ▼
┌─────────────────────────────────────┐
│         PLANNER AGENT               │
│  • Reads age, level, subject goals  │
│  • Generates daily/weekly plan      │
│  • Allocates time per topic         │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│         TEACHER AGENT               │
│  • Adjusts vocabulary to grade      │
│  • Uses local Pakistani analogies   │
│  • Formats content for voice/text   │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│         QUIZ AGENT                  │
│  • Easy → Medium → Hard → Expert    │
│  • Evaluates responses in real-time │
│  • Provides step-by-step feedback   │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│        EVALUATOR AGENT              │
│  • Mastery score updated per quiz   │
│  • Detects plateaus and regressions │
│  • Recommends: advance / repeat /   │
│    simplify / extra practice        │
└─────────────────────────────────────┘
```

| Student Level | Vocabulary | Examples | Quiz Difficulty | Content Depth |
|:-------------:|:----------:|:--------:|:---------------:|:-------------:|
| Primary (Grade 1–5) | Simple | Cartoon/daily life | Easy | Conceptual |
| Middle (Grade 6–8) | Moderate | Local stories | Easy–Medium | Applied |
| Matric (Grade 9–10) | Standard | Pakistan-context | Medium–Hard | Analytical |
| Inter (Grade 11–12) | Academic | Real-world data | Hard | Evaluative |
| University | Professional | Research-level | Hard–Expert | Synthesis |

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|:-----:|:----------:|:-------:|
| **Frontend** | [Streamlit 1.57](https://streamlit.io) | Interactive web UI |
| **AI Orchestration** | [CrewAI](https://crewai.com) | Multi-agent framework |
| **Primary LLM** | [Google Gemini 2.5 Flash](https://deepmind.google/technologies/gemini/) | Teaching, planning, evaluation |
| **Fallback LLM** | [Groq (Mixtral-8x7B)](https://groq.com) | Fast inference fallback |
| **Voice (TTS)** | [ElevenLabs](https://elevenlabs.io) + Azure Neural + Browser API | Text-to-speech with fallback chain |
| **Database** | [Supabase](https://supabase.com) | Auth, user profiles, progress data |
| **Containerization** | [Docker](https://docker.com) | Deployment packaging |
| **Language** | Python 3.10+ | Core application |

### LLM Fallback Chain
```
Gemini 2.5 Flash  →  Groq (Mixtral)  →  OpenRouter (LLaMA-2 70B)  →  HuggingFace
```

### TTS Fallback Chain
```
ElevenLabs  →  Azure Neural Voices  →  Browser Web Speech API
```

---

## 🚀 How to Run Locally

### Prerequisites
- Python 3.10 or higher
- A Supabase project ([free tier](https://supabase.com))
- Google Gemini API key ([Google AI Studio](https://aistudio.google.com))

### 1. Clone the Repository

```bash
git clone https://github.com/Think-Gleam/edu-mentor.git
cd edu-mentor
```

### 2. Create a Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
# ── Required ─────────────────────────────────────────
GEMINI_API_KEY=your_gemini_api_key_here
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your_supabase_anon_key_here

# ── LLM Fallbacks (Optional) ─────────────────────────
GROQ_API_KEY=your_groq_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here

# ── Voice / TTS (Optional) ───────────────────────────
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here

# ── Azure Speech (Optional fallback) ─────────────────
AZURE_SPEECH_KEY_1=your_azure_speech_key_here
AZURE_SPEECH_REGION=eastus

# ── Debug ─────────────────────────────────────────────
DEBUG=False
LOG_LEVEL=INFO
```

### 5. Run the Application

**Full LMS Platform** (with authentication, profiles, and all features):
```bash
streamlit run lms_app.py
```

**Standalone AI Tutor** (quick demo, no login required):
```bash
streamlit run app.py
```

**Using Docker:**
```bash
docker build -t edu-mentor .
docker run -p 8501:8501 --env-file .env edu-mentor
```

Open your browser at **http://localhost:8501** 🎉

---

## 📁 Project Structure

```
edu-mentor/
│
├── app.py                    # Standalone AI tutor (v1 — no login)
├── app_v2.py                 # Enhanced tutor UI (v2)
├── lms_app.py                # Full LMS platform (auth + all features)
├── requirements.txt          # Python dependencies
├── Dockerfile                # Container configuration
│
├── agents/                   # CrewAI multi-agent system
│   ├── agents.py             # 4 agent definitions (Planner, Teacher, Quiz, Evaluator)
│   ├── tasks.py              # Agent task definitions
│   └── tools.py              # Tools available to agents
│
├── crew/
│   └── crew.py               # CrewAI orchestration & workflow
│
├── config/
│   ├── settings.py           # App configuration, model configs, fallback chains
│   └── prompts.py            # System prompt templates
│
├── utils/
│   ├── fallback_llm.py       # LLM fallback logic (Gemini → Groq → OpenRouter)
│   ├── fallback_tts.py       # TTS fallback logic (ElevenLabs → Azure → Browser)
│   ├── fallback_stt.py       # STT fallback logic
│   ├── supabase_client.py    # Supabase database client
│   └── logger.py             # Structured logging
│
├── frontend/
│   ├── components/           # Reusable UI components
│   ├── pages/                # Individual page modules
│   └── styles/               # CSS styling
│
├── examples/                 # Example scripts and demos
└── docs/
    └── screenshots/          # Application screenshots (add yours here)
```

---

## 🏆 Hackathon Context

<div align="center">

**🎯 HEC Gen-AI Hackathon 2025**
*Higher Education Commission of Pakistan*

**Team: AI SQUAD XERO**

</div>

EduMentor was built for the **HEC Gen-AI Hackathon 2025**, organized by the Higher Education Commission of Pakistan, with the goal of leveraging Generative AI to solve real-world challenges in education.

### Problem We're Solving
Pakistan faces a significant **education quality gap**: millions of students lack access to qualified teachers, personalized attention, and quality study materials — especially outside major urban centers. EduMentor bridges this gap by putting an AI-powered personal tutor in every student's pocket.

### Our Innovation
- **Agentic AI Architecture** — Four autonomous AI agents working collaboratively, not just a single chatbot
- **True Adaptivity** — Content, difficulty, and language dynamically change based on the learner's profile and real-time performance
- **Cultural Relevance** — Built specifically for Pakistani students with local examples, Urdu support, and curriculum alignment
- **Voice-First for Inclusivity** — Text-to-speech support removes literacy barriers and aids visual learners

### UN SDG Alignment
> 📌 **SDG 4 — Quality Education**: *"Ensure inclusive and equitable quality education and promote lifelong learning opportunities for all."*

---

## 🗺️ Future Roadmap

### Phase 2 — Near-Term
- [ ] 📱 **Mobile App** — React Native app for iOS and Android
- [ ] 🌐 **Expanded Language Support** — Sindhi, Punjabi, Pashto
- [ ] 👨‍🏫 **Teacher Dashboard** — Monitor student progress and intervene
- [ ] 📧 **Email Verification & Password Recovery**
- [ ] 🔑 **Social Login** — Google and Microsoft OAuth

### Phase 3 — Mid-Term
- [ ] 🎥 **Video Lessons** — AI-generated explainer videos
- [ ] 🤝 **Peer Learning** — Study groups and collaborative quizzes
- [ ] 🏅 **Gamification** — Badges, streaks, leaderboards
- [ ] 📊 **Parent Portal** — Progress reports for parents
- [ ] 🏫 **School Integration** — API for institutional use

### Phase 4 — Long-Term
- [ ] 🌍 **Regional Expansion** — Bangladesh, Afghanistan, and other South Asian markets
- [ ] 🧪 **AR/VR Labs** — Immersive science and math simulations
- [ ] 🤖 **Fine-Tuned Models** — Custom LLMs trained on Pakistani curriculum
- [ ] 📡 **Offline Mode** — Learn without internet via edge AI

---

## 👥 Contributors

<div align="center">

**Team AI SQUAD XERO** — HEC Gen-AI Hackathon 2025

</div>

| Name | Role | GitHub |
|:----:|:----:|:------:|
| *(Team Member 1)* | Project Lead & AI Architecture | [@username](https://github.com) |
| *(Team Member 2)* | Frontend & UX Design | [@username](https://github.com) |
| *(Team Member 3)* | Backend & Database | [@username](https://github.com) |
| *(Team Member 4)* | AI Agents & Prompt Engineering | [@username](https://github.com) |

> 📌 *Replace with actual team member names, roles, and GitHub links.*

---

## 📄 License & Acknowledgments

### License
This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

### Acknowledgments

We are grateful to the following organizations and open-source projects that made EduMentor possible:

- 🏛️ **Higher Education Commission (HEC) of Pakistan** — for organizing the Gen-AI Hackathon and fostering AI innovation in education
- 🤖 **[CrewAI](https://crewai.com)** — for the powerful multi-agent orchestration framework
- ✨ **[Google Gemini](https://deepmind.google/technologies/gemini/)** — for state-of-the-art language model capabilities
- 🗄️ **[Supabase](https://supabase.com)** — for the open-source backend infrastructure
- 🎙️ **[ElevenLabs](https://elevenlabs.io)** — for natural, human-quality text-to-speech
- 🚀 **[Streamlit](https://streamlit.io)** — for making beautiful data apps fast
- ⚡ **[Groq](https://groq.com)** — for blazing-fast LLM inference

---

<div align="center">

**Made with ❤️ for the students of Pakistan**

*"Education is the most powerful weapon which you can use to change the world." — Nelson Mandela*

[![GitHub stars](https://img.shields.io/github/stars/Think-Gleam/edu-mentor?style=social)](https://github.com/Think-Gleam/edu-mentor)
[![GitHub forks](https://img.shields.io/github/forks/Think-Gleam/edu-mentor?style=social)](https://github.com/Think-Gleam/edu-mentor/fork)

</div>
