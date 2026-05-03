# Supabase client and database utilities

import os
from typing import Dict, List, Any, Optional
from datetime import datetime
from supabase import create_client, Client
from config.settings import SUPABASE_URL, SUPABASE_KEY
from utils.logger import setup_logger

logger = setup_logger(__name__)


class SupabaseManager:
    """Manage all Supabase database operations."""
    
    def __init__(self):
        """Initialize Supabase client."""
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY not found in .env")
        
        self.client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        logger.info("Supabase client initialized")
    
    # ==================== STUDY PLANS ====================
    def save_study_plan(self, user_id: str, plan_data: Dict[str, Any]) -> bool:
        """Save a study plan to the database."""
        try:
            data = {
                "user_id": user_id,
                "plan": plan_data,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
            }
            self.client.table("study_plans").insert(data).execute()
            logger.info(f"Study plan saved for user {user_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to save study plan: {e}")
            return False
    
    def get_study_plan(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve the latest study plan for a user."""
        try:
            response = self.client.table("study_plans").select("*").eq("user_id", user_id).order("created_at", desc=True).limit(1).execute()
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"Failed to retrieve study plan: {e}")
            return None
    
    # ==================== QUIZ RESULTS ====================
    def save_quiz_result(self, user_id: str, topic: str, score: float, answers: Dict[str, Any], time_spent_seconds: int) -> bool:
        """Save quiz results."""
        try:
            data = {
                "user_id": user_id,
                "topic": topic,
                "score": score,
                "answers": answers,
                "time_spent_seconds": time_spent_seconds,
                "created_at": datetime.utcnow().isoformat(),
            }
            self.client.table("quiz_results").insert(data).execute()
            logger.info(f"Quiz result saved for user {user_id} on topic {topic}")
            return True
        except Exception as e:
            logger.error(f"Failed to save quiz result: {e}")
            return False
    
    def get_quiz_history(self, user_id: str, topic: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Get quiz history for a user (optionally filtered by topic)."""
        try:
            query = self.client.table("quiz_results").select("*").eq("user_id", user_id)
            if topic:
                query = query.eq("topic", topic)
            response = query.order("created_at", desc=True).limit(limit).execute()
            return response.data or []
        except Exception as e:
            logger.error(f"Failed to retrieve quiz history: {e}")
            return []
    
    # ==================== PROGRESS TRACKING ====================
    def update_progress(self, user_id: str, topic: str, mastery_level: float, attempts: int) -> bool:
        """Update or create a progress record."""
        try:
            # Check if record exists
            existing = self.client.table("progress").select("*").eq("user_id", user_id).eq("topic", topic).execute()
            
            data = {
                "user_id": user_id,
                "topic": topic,
                "mastery_level": mastery_level,
                "attempts": attempts,
                "updated_at": datetime.utcnow().isoformat(),
            }
            
            if existing.data:
                # Update
                self.client.table("progress").update(data).eq("user_id", user_id).eq("topic", topic).execute()
            else:
                # Insert
                data["created_at"] = datetime.utcnow().isoformat()
                self.client.table("progress").insert(data).execute()
            
            logger.info(f"Progress updated for user {user_id} on topic {topic}")
            return True
        except Exception as e:
            logger.error(f"Failed to update progress: {e}")
            return False
    
    def get_progress(self, user_id: str) -> Dict[str, float]:
        """Get mastery levels for all topics."""
        try:
            response = self.client.table("progress").select("topic, mastery_level").eq("user_id", user_id).execute()
            return {item["topic"]: item["mastery_level"] for item in response.data or []}
        except Exception as e:
            logger.error(f"Failed to retrieve progress: {e}")
            return {}
    
    # ==================== USER PROFILE ====================
    def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user profile from profiles table."""
        try:
            response = self.client.table("profiles").select("*").eq("id", user_id).execute()
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"Failed to retrieve user profile: {e}")
            return None
    
    # ==================== FEEDBACK & LOGS ====================
    def log_agent_interaction(self, user_id: str, agent_name: str, input_text: str, output_text: str, tokens_used: int) -> bool:
        """Log agent interactions for analysis and debugging."""
        try:
            data = {
                "user_id": user_id,
                "agent_name": agent_name,
                "input": input_text,
                "output": output_text,
                "tokens_used": tokens_used,
                "created_at": datetime.utcnow().isoformat(),
            }
            self.client.table("agent_logs").insert(data).execute()
            return True
        except Exception as e:
            logger.error(f"Failed to log agent interaction: {e}")
            return False


# Global instance
_supabase_manager = None


def get_supabase_manager() -> SupabaseManager:
    """Get or create the Supabase manager singleton."""
    global _supabase_manager
    if _supabase_manager is None:
        _supabase_manager = SupabaseManager()
    return _supabase_manager
