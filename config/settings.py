# Configuration and constants for EduMentor Multi-Agent System

import os
from typing import List

# ==================== BASIC CONFIG ====================
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# ==================== RATE LIMITING & THROTTLING ====================
RATE_LIMITS = {
    "gemini": {"calls_per_minute": 60, "tokens_per_day": 1_000_000},
    "groq": {"calls_per_minute": 30, "tokens_per_day": 10_000_000},
    "openrouter": {"calls_per_minute": 50, "tokens_per_day": 1_000_000},
    "huggingface": {"calls_per_minute": 100, "tokens_per_day": 1_000_000},
}

TTS_RATE_LIMITS = {
    "elevenlabs": {"calls_per_minute": 10, "characters_per_month": 100_000},
    "azure": {"calls_per_minute": 120, "characters_per_month": 500_000},
}

STT_RATE_LIMITS = {
    "deepgram": {"calls_per_minute": 50, "hours_per_month": 100},
    "assemblyai": {"calls_per_minute": 100, "hours_per_month": 200},
    "azure": {"calls_per_minute": 120, "hours_per_month": 500},
}

# ==================== LLM FALLBACK ORDER ====================
LLM_FALLBACK_ORDER: List[str] = ["gemini", "groq", "openrouter", "huggingface"]

# ==================== TTS FALLBACK ORDER ====================
TTS_FALLBACK_ORDER: List[str] = ["elevenlabs", "azure", "browser"]

# ==================== STT FALLBACK ORDER ====================
STT_FALLBACK_ORDER: List[str] = ["deepgram", "assemblyai", "azure"]

# ==================== MODEL CONFIGS ====================
MODEL_CONFIGS = {
    "gemini": {
        "model": "gemini-2.5-flash",
        "temperature": 0.7,
        "max_tokens": 2048,
    },
    "groq": {
        "model": "mixtral-8x7b-32768",  # Fast, good for reasoning
        "temperature": 0.7,
        "max_tokens": 2048,
    },
    "openrouter": {
        "model": "meta-llama/llama-2-70b-chat",  # Reliable fallback
        "temperature": 0.7,
        "max_tokens": 2048,
    },
    "huggingface": {
        "model": "meta-llama/Llama-2-70b-chat-hf",
        "temperature": 0.7,
        "max_tokens": 1024,
    },
}

# ==================== AGENT CONFIGURATIONS ====================
AGENT_CONFIGS = {
    "planner": {
        "role": "Study Plan Creator",
        "goal": "Create personalized, adaptive daily and weekly study plans",
        "backstory": "Expert curriculum designer with deep knowledge of Pakistan's education system",
        "verbose": True,
    },
    "teacher": {
        "role": "Adaptive Teacher",
        "goal": "Explain concepts with Pakistani examples, analogies, and age-appropriate language",
        "backstory": "Experienced educator who knows how to connect with students from Pakistan",
        "verbose": True,
    },
    "quiz": {
        "role": "Quiz Master",
        "goal": "Generate adaptive quizzes and evaluate student responses with detailed feedback",
        "backstory": "Assessment expert who designs quizzes that match student level and learning goals",
        "verbose": True,
    },
    "evaluator": {
        "role": "Progress Evaluator",
        "goal": "Track mastery, detect struggles, and recommend adaptive interventions",
        "backstory": "Learning analytics expert who uses data to optimize student outcomes",
        "verbose": True,
    },
}

# ==================== SUPABASE CONFIG ====================
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# ==================== CACHE CONFIG ====================
CACHE_ENABLED = True
CACHE_TTL_SECONDS = 3600  # 1 hour

# ==================== VOICE CONFIG ====================
VOICE_ENABLED = True
VOICE_LANGUAGE = "en"  # English for teacher, but can switch to Urdu
ELEVENLABS_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Rachel (professional, clear)

# ==================== QUIZ CONFIG ====================
QUIZ_DIFFICULTY_LEVELS = ["easy", "medium", "hard", "expert"]
QUIZ_MIN_QUESTIONS = 3
QUIZ_MAX_QUESTIONS = 10
MASTERY_THRESHOLD = 0.75  # 75% to pass

# ==================== TIMEOUT CONFIG ====================
LLM_TIMEOUT_SECONDS = 30
TTS_TIMEOUT_SECONDS = 15
STT_TIMEOUT_SECONDS = 60

# ==================== LOGGING ====================
LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = os.path.join(LOG_DIR, "edumentor_agents.log")
