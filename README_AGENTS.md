# 🎓 EduMentor Multi-Agent AI Tutor System

A production-ready multi-agent system for personalized adaptive learning using CrewAI, LangChain, and intelligent LLM fallbacks.

## 🚀 Overview

EduMentor coordinates **4 specialized AI agents** to deliver complete learning experiences:

### The 4 Agents

| Agent | Role | Capabilities |
|-------|------|--------------|
| **Planner** 📋 | Study Plan Creator | Creates personalized daily/weekly study plans, adapts based on progress |
| **Teacher** 📚 | Adaptive Educator | Explains concepts with Pakistani examples, voice output, simple language |
| **Quiz** 🧠 | Assessment Master | Generates adaptive quizzes, evaluates responses, provides feedback |
| **Evaluator** 📊 | Progress Tracker | Detects struggles, calculates mastery, recommends interventions |

## 🏗️ Project Structure

```
EduMentor/
├── agents/
│   ├── __init__.py
│   ├── agents.py          # All 4 agents with prompts
│   ├── tools.py           # Tool definitions
│   └── tasks.py           # Task templates
├── crew/
│   ├── __init__.py
│   └── crew.py            # Main orchestrator & workflows
├── utils/
│   ├── __init__.py
│   ├── fallback_llm.py    # LLM fallback: Gemini → Groq → OpenRouter → HF
│   ├── fallback_tts.py    # TTS fallback: ElevenLabs → Azure → Browser
│   ├── fallback_stt.py    # STT fallback: Deepgram → AssemblyAI → Azure
│   ├── supabase_client.py # Database operations
│   └── logger.py          # Logging setup
├── config/
│   ├── __init__.py
│   ├── settings.py        # Configuration constants
│   └── prompts.py         # Centralized prompt templates
├── examples/
│   ├── run_full_session.py    # Complete workflow demo
│   └── test_agents.py         # Individual agent tests
├── lms_app.py             # Streamlit app
├── requirements.txt       # Python dependencies
├── Dockerfile             # Container setup
└── README_AGENTS.md       # This file
```

## ⚙️ Intelligent Fallback System

### LLM Fallback Chain
```
1. Gemini (Primary - Fast, reliable)
   ↓ [if fails]
2. Groq (Fast inference)
   ↓ [if fails]
3. OpenRouter (Many models)
   ↓ [if fails]
4. HuggingFace (Open source)
```

### TTS Fallback Chain
```
1. ElevenLabs (Best quality)
   ↓ [if fails]
2. Azure Speech (Urdu support!)
   ↓ [if fails]
3. Browser Web Speech API (Client-side)
```

### STT Fallback Chain
```
1. Deepgram (Best accuracy)
   ↓ [if fails]
2. AssemblyAI (Urdu support!)
   ↓ [if fails]
3. Azure (Urdu support!)
```

## 🔧 Required Environment Variables

```env
# LLM APIs
GEMINI_API_KEY=your_key
GROQ_API_KEY=your_key
OPENROUTER_API_KEY=your_key
HUGGINGFACE_TOKEN=your_token

# Voice APIs
ELEVENLABS_API_KEY=your_key
DEEPGRAM_API_KEY=your_key
ASSEMBLYAI_API_KEY=your_key
AZURE_SPEECH_KEY_1=your_key
AZURE_SPEECH_KEY_2=your_key
AZURE_SPEECH_REGION=eastus

# Database
SUPABASE_URL=your_url
SUPABASE_KEY=your_key

# Optional
DEBUG=False
LOG_LEVEL=INFO
```

## 📦 Installation

```bash
# 1. Clone the repository
git clone <repo>
cd EduMentor

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
cp .env.example .env
# Edit .env with your API keys

# 5. Run the system
python examples/run_full_session.py
```

## 🎯 Workflows

### 1. Full Learning Cycle
**Plan → Teach → Quiz → Evaluate**

```python
from crew.crew import get_edumentor_crew

crew = get_edumentor_crew()
result = crew.run_full_learning_cycle(
    user_id="user_123",
    topic="AI Fundamentals",
    duration="weekly",
    difficulty="medium"
)
```

**Output:**
- Study plan (weekly breakdown)
- Personalized lesson explanation
- Adaptive quiz (3-5 questions)
- Mastery assessment & recommendations

### 2. Quick Lesson
**Teach + Quiz**

```python
result = crew.run_quick_lesson(
    user_id="user_123",
    topic="Machine Learning"
)
```

### 3. Practice Quiz
**Quiz Only**

```python
result = crew.run_quiz_only(
    user_id="user_123",
    topic="Algorithms",
    difficulty="hard"
)
```

### 4. Progress Evaluation
**Assess & Recommend**

```python
result = crew.evaluate_progress(
    user_id="user_123",
    topic="Linear Algebra",
    quiz_score=0.82,
    time_spent_minutes=25
)
```

## 💻 Running Examples

```bash
# Full cycle (Plan → Teach → Quiz → Evaluate)
python examples/run_full_session.py --mode full

# Quick lesson (Teach + Quiz)
python examples/run_full_session.py --mode quick

# Practice quiz
python examples/run_full_session.py --mode quiz

# Progress evaluation
python examples/run_full_session.py --mode eval
```

## 🗄️ Database Schema (Supabase)

### profiles table
```sql
id (UUID, primary key)
user_id (UUID)
full_name (text)
age (integer)
grade_level (text)
preferred_language (text)
province (text)
learning_goals (JSON array)
academic_board (text)
learning_challenges (text)
created_at (timestamp)
updated_at (timestamp)
```

### study_plans table
```sql
id (UUID, primary key)
user_id (UUID)
plan (JSON)
created_at (timestamp)
updated_at (timestamp)
```

### quiz_results table
```sql
id (UUID, primary key)
user_id (UUID)
topic (text)
score (float 0-1)
answers (JSON)
time_spent_seconds (integer)
created_at (timestamp)
```

### progress table
```sql
id (UUID, primary key)
user_id (UUID)
topic (text)
mastery_level (float 0-1)
attempts (integer)
created_at (timestamp)
updated_at (timestamp)
```

### agent_logs table
```sql
id (UUID, primary key)
user_id (UUID)
agent_name (text)
input (text)
output (text)
tokens_used (integer)
created_at (timestamp)
```

## 🎨 Agent Prompts & Customization

Edit prompts in `config/prompts.py` for different teaching styles:

```python
TEACHER_SYSTEM_PROMPT = """
You are an elite teacher for Pakistani students.
Your teaching style:
1. Use SIMPLE language appropriate for their age
2. Use real Pakistani examples (cricket, Bollywood, cities)
3. Create analogies from their daily life
...
"""
```

## 📊 Rate Limiting & Cost Control

Configure in `config/settings.py`:

```python
RATE_LIMITS = {
    "gemini": {"calls_per_minute": 60},
    "groq": {"calls_per_minute": 30},
    "elevenlabs": {"calls_per_minute": 10},
}
```

**Cost Optimization Tips:**
1. Use Groq for fast inference (free tier)
2. Cache lesson explanations (3600s TTL)
3. Batch quiz generation
4. Use Azure for Urdu TTS (cheaper than ElevenLabs)
5. Monitor token usage with `agent_logs` table

## 🐛 Error Handling & Recovery

The system automatically:
1. **Detects failures** in any LLM/TTS/STT service
2. **Retries with next provider** in fallback chain
3. **Logs all errors** for debugging
4. **Returns sensible defaults** if all providers fail

Example log output:
```
INFO: Attempting gemini...
WARNING: Gemini failed: Rate limit exceeded. Trying next provider...
INFO: Attempting groq...
✅ Groq succeeded
```

## 🚀 Deployment

### Docker

```bash
docker build -t edumentor:latest .
docker run -p 8080:8080 \
  -e GEMINI_API_KEY=$GEMINI_API_KEY \
  -e GROQ_API_KEY=$GROQ_API_KEY \
  -e SUPABASE_URL=$SUPABASE_URL \
  -e SUPABASE_KEY=$SUPABASE_KEY \
  edumentor:latest
```

### Cloud Run

```bash
gcloud run deploy edumentor \
  --source . \
  --region us-central1 \
  --set-env-vars GEMINI_API_KEY=$GEMINI_API_KEY
```

## 📈 Monitoring & Analytics

- **Logs**: Check `logs/edumentor_agents.log`
- **Agent calls**: Query `agent_logs` table
- **Student progress**: Query `progress` table
- **Quiz performance**: Query `quiz_results` table

## 🎓 Best Practices

1. **Session Management**: One crew per user session
2. **Caching**: Cache lesson explanations for repeat visits
3. **Fallbacks**: Always have 2+ API keys configured
4. **Timeouts**: Set appropriate timeouts for each service
5. **Monitoring**: Log all agent interactions for analysis
6. **Cost**: Use rate limiting to control API costs
7. **User Experience**: Provide progress feedback UI

## 🔐 Security

- All API keys in `.env` (never commit!)
- Database queries use parameterized statements
- User IDs validated before each operation
- Log sensitive data minimized
- Credentials rotated regularly

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with `python examples/run_full_session.py`
5. Submit a pull request

## 📝 License

MIT License - See LICENSE file

## 🙏 Acknowledgments

- **CrewAI** - Multi-agent orchestration
- **LangChain** - LLM integrations
- **Gemini, Groq, OpenRouter** - LLM providers
- **ElevenLabs, Azure, Deepgram** - Voice providers
- **Supabase** - Database & auth

---

**Built with ❤️ for Pakistani students everywhere.**
