# Tool definitions for CrewAI agents

import json
from typing import Dict, List, Any, Optional
from utils.logger import setup_logger
from utils.supabase_client import get_supabase_manager
from utils.fallback_llm import get_llm_client
from utils.fallback_tts import get_tts_client
from utils.fallback_stt import get_stt_client

logger = setup_logger(__name__)


# ==================== DATABASE TOOLS ====================
def save_to_supabase(table_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Save data to Supabase (generic)."""
    try:
        db = get_supabase_manager()
        
        if table_name == "study_plans":
            success = db.save_study_plan(data.get("user_id"), data.get("plan"))
        elif table_name == "quiz_results":
            success = db.save_quiz_result(
                user_id=data.get("user_id"),
                topic=data.get("topic"),
                score=data.get("score"),
                answers=data.get("answers"),
                time_spent_seconds=data.get("time_spent_seconds", 0),
            )
        elif table_name == "progress":
            success = db.update_progress(
                user_id=data.get("user_id"),
                topic=data.get("topic"),
                mastery_level=data.get("mastery_level"),
                attempts=data.get("attempts"),
            )
        else:
            logger.error(f"Unknown table: {table_name}")
            return {"success": False, "error": "Unknown table"}
        
        return {"success": success, "table": table_name}
    except Exception as e:
        logger.error(f"Supabase save error: {e}")
        return {"success": False, "error": str(e)}


def get_user_profile(user_id: str) -> Dict[str, Any]:
    """Retrieve user profile from database."""
    try:
        db = get_supabase_manager()
        profile = db.get_user_profile(user_id)
        return profile or {"error": "Profile not found"}
    except Exception as e:
        logger.error(f"Profile retrieval error: {e}")
        return {"error": str(e)}


def get_user_progress(user_id: str) -> Dict[str, float]:
    """Get user's mastery levels across all topics."""
    try:
        db = get_supabase_manager()
        progress = db.get_progress(user_id)
        return progress or {}
    except Exception as e:
        logger.error(f"Progress retrieval error: {e}")
        return {"error": str(e)}


def get_quiz_history(user_id: str, topic: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
    """Get user's quiz history."""
    try:
        db = get_supabase_manager()
        history = db.get_quiz_history(user_id, topic, limit)
        return history or []
    except Exception as e:
        logger.error(f"Quiz history retrieval error: {e}")
        return []


# ==================== LLM TOOLS ====================
def generate_response(
    prompt: str,
    system_prompt: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 2048,
) -> Dict[str, Any]:
    """Generate LLM response with automatic fallback."""
    try:
        client = get_llm_client()
        result = client.generate(prompt, system_prompt, temperature, max_tokens)
        return result
    except Exception as e:
        logger.error(f"LLM generation error: {e}")
        return {
            "response": "Error generating response",
            "provider": "error",
            "error": str(e),
        }


# ==================== VOICE TOOLS ====================
def synthesize_speech(
    text: str,
    language: str = "en",
    voice_name: Optional[str] = None,
) -> Dict[str, Any]:
    """Convert text to speech with automatic fallback."""
    try:
        client = get_tts_client()
        audio_bytes, provider = client.synthesize(text, language, voice_name)
        
        return {
            "success": audio_bytes is not None,
            "provider": provider,
            "audio_size": len(audio_bytes) if audio_bytes else 0,
        }
    except Exception as e:
        logger.error(f"TTS error: {e}")
        return {"success": False, "provider": "error", "error": str(e)}


def transcribe_audio(audio_bytes: bytes, language: str = "en") -> Dict[str, Any]:
    """Convert speech to text with automatic fallback."""
    try:
        client = get_stt_client()
        text, provider = client.transcribe(audio_bytes, language)
        
        return {
            "success": text is not None,
            "text": text or "",
            "provider": provider,
        }
    except Exception as e:
        logger.error(f"STT error: {e}")
        return {"success": False, "provider": "error", "error": str(e)}


# ==================== PARSING & VALIDATION ====================
def parse_json_response(text: str) -> Dict[str, Any]:
    """Safely parse JSON from LLM response."""
    try:
        # Try to find JSON in the response
        import re
        json_match = re.search(r"\{[\s\S]*\}", text)
        if json_match:
            return json.loads(json_match.group())
        return {"error": "No JSON found in response"}
    except Exception as e:
        logger.error(f"JSON parsing error: {e}")
        return {"error": str(e)}


def calculate_mastery_level(
    quiz_scores: List[float],
    time_spent_total: int,
    max_time_expected: int = 3600,
) -> float:
    """Calculate mastery level based on scores and time efficiency."""
    if not quiz_scores:
        return 0.0
    
    avg_score = sum(quiz_scores) / len(quiz_scores)
    time_factor = min(1.0, time_spent_total / max_time_expected) if max_time_expected else 1.0
    
    # Weighted average: 80% score, 20% time efficiency
    mastery = (avg_score * 0.8) + (time_factor * 0.2)
    return round(mastery, 2)


# ==================== VALIDATION ====================
def validate_quiz_answer(
    question: str,
    student_answer: str,
    correct_answer: str,
) -> Dict[str, Any]:
    """Validate a student's answer (especially for short-answer)."""
    try:
        # For multiple choice, simple equality
        if student_answer.strip().lower() == correct_answer.strip().lower():
            return {"correct": True, "score": 1.0, "feedback": "Excellent!"}
        
        # For short answers, use LLM to check semantic similarity
        client = get_llm_client()
        check_prompt = f"""
        Student answer: "{student_answer}"
        Correct answer: "{correct_answer}"
        Question: "{question}"
        
        Is the student's answer semantically correct? (Yes/No/Partial)
        Provide score 0-1 and brief feedback.
        
        Response format: {{"correct": bool, "score": float, "feedback": "..."}}
        """
        
        result = client.generate(check_prompt, temperature=0.2, max_tokens=100)
        parsed = parse_json_response(result.get("response", ""))
        return parsed
    except Exception as e:
        logger.error(f"Answer validation error: {e}")
        return {"correct": False, "score": 0.0, "feedback": "Error validating answer"}


# ==================== TOOL DEFINITIONS FOR CREW ====================
AGENT_TOOLS = {
    "database": [
        ("save_to_supabase", save_to_supabase),
        ("get_user_profile", get_user_profile),
        ("get_user_progress", get_user_progress),
        ("get_quiz_history", get_quiz_history),
    ],
    "llm": [
        ("generate_response", generate_response),
    ],
    "voice": [
        ("synthesize_speech", synthesize_speech),
        ("transcribe_audio", transcribe_audio),
    ],
    "utilities": [
        ("parse_json", parse_json_response),
        ("calculate_mastery", calculate_mastery_level),
        ("validate_answer", validate_quiz_answer),
    ],
}
