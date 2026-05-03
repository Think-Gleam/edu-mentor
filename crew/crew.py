# Main Crew Orchestrator - Coordinates all 4 agents for complete learning workflows

import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from crewai import Crew
from agents.agents import get_agent_pool
from agents.tasks import (
    create_planner_task,
    create_teacher_task,
    create_quiz_task,
    create_evaluator_task,
)
from utils.supabase_client import get_supabase_manager
from utils.logger import setup_logger

logger = setup_logger(__name__)


class EduMentorCrew:
    """
    Main orchestrator for the EduMentor multi-agent system.
    
    Workflows:
    1. Plan → Teach → Quiz → Evaluate (Full learning cycle)
    2. Teach → Quiz (Quick lesson + test)
    3. Quiz Only (Practice quizzes)
    4. Evaluate (Progress check)
    """
    
    def __init__(self):
        """Initialize the crew with all agents."""
        self.agent_pool = get_agent_pool()
        self.db = get_supabase_manager()
        logger.info("🎓 EduMentorCrew initialized")
    
    def run_full_learning_cycle(
        self,
        user_id: str,
        topic: str,
        duration: str = "weekly",
        difficulty: str = "medium",
    ) -> Dict[str, Any]:
        """
        Complete learning cycle:
        1. Planner creates a study plan
        2. Teacher explains the concept
        3. Quiz Agent tests understanding
        4. Evaluator assesses and recommends next steps
        """
        logger.info(f"🚀 Starting full learning cycle for user {user_id} on topic {topic}")
        
        # Get user profile
        user_profile = self.db.get_user_profile(user_id)
        if not user_profile:
            logger.error(f"User profile not found: {user_id}")
            return {"error": "User profile not found"}
        
        results = {
            "user_id": user_id,
            "topic": topic,
            "timestamp": datetime.utcnow().isoformat(),
            "phases": {},
        }
        
        # ==================== PHASE 1: PLANNING ====================
        logger.info("📋 Phase 1: Planning")
        try:
            planner_crew = Crew(
                agents=[self.agent_pool.planner],
                tasks=[
                    create_planner_task(
                        self.agent_pool.planner,
                        student_name=user_profile.get("full_name", "Student"),
                        topic=topic,
                        duration=duration,
                        level=difficulty,
                        daily_time=30,
                        learning_goals=", ".join(user_profile.get("learning_goals", ["General Knowledge"])),
                    )
                ],
                verbose=True,
            )
            
            plan_result = planner_crew.kickoff()
            results["phases"]["planning"] = {
                "status": "success",
                "plan": json.loads(plan_result) if isinstance(plan_result, str) else plan_result,
            }
            
            # Save to DB
            self.db.save_study_plan(
                user_id,
                results["phases"]["planning"]["plan"]
            )
            logger.info("✅ Planning phase complete")
        except Exception as e:
            logger.error(f"Planning phase error: {e}")
            results["phases"]["planning"] = {"status": "failed", "error": str(e)}
        
        # ==================== PHASE 2: TEACHING ====================
        logger.info("📚 Phase 2: Teaching")
        try:
            teacher_crew = Crew(
                agents=[self.agent_pool.teacher],
                tasks=[
                    create_teacher_task(
                        self.agent_pool.teacher,
                        student_name=user_profile.get("full_name", "Student"),
                        topic=topic,
                        age=user_profile.get("age", 15),
                        learning_goal=user_profile.get("learning_goals", ["General Knowledge"])[0],
                    )
                ],
                verbose=True,
            )
            
            teaching_result = teacher_crew.kickoff()
            results["phases"]["teaching"] = {
                "status": "success",
                "explanation": teaching_result,
            }
            logger.info("✅ Teaching phase complete")
        except Exception as e:
            logger.error(f"Teaching phase error: {e}")
            results["phases"]["teaching"] = {"status": "failed", "error": str(e)}
        
        # ==================== PHASE 3: QUIZ ====================
        logger.info("🧠 Phase 3: Quiz")
        try:
            quiz_crew = Crew(
                agents=[self.agent_pool.quiz],
                tasks=[
                    create_quiz_task(
                        self.agent_pool.quiz,
                        student_name=user_profile.get("full_name", "Student"),
                        topic=topic,
                        difficulty=difficulty,
                        num_questions=5,
                        student_level=difficulty,
                    )
                ],
                verbose=True,
            )
            
            quiz_result = quiz_crew.kickoff()
            quiz_data = json.loads(quiz_result) if isinstance(quiz_result, str) else quiz_result
            
            results["phases"]["quiz"] = {
                "status": "success",
                "questions": quiz_data.get("questions", []),
            }
            logger.info("✅ Quiz generation complete")
        except Exception as e:
            logger.error(f"Quiz phase error: {e}")
            results["phases"]["quiz"] = {"status": "failed", "error": str(e)}
        
        # ==================== PHASE 4: EVALUATION ====================
        logger.info("📊 Phase 4: Evaluation")
        try:
            # Get quiz history for context
            quiz_history = self.db.get_quiz_history(user_id, topic, limit=5)
            previous_scores = [q.get("score", 0) for q in quiz_history]
            
            evaluator_crew = Crew(
                agents=[self.agent_pool.evaluator],
                tasks=[
                    create_evaluator_task(
                        self.agent_pool.evaluator,
                        student_name=user_profile.get("full_name", "Student"),
                        topic=topic,
                        score=0,  # Would be actual score after quiz submission
                        attempts=len(quiz_history) + 1,
                        time_spent_minutes=0,  # Would be actual time
                        previous_scores=previous_scores,
                    )
                ],
                verbose=True,
            )
            
            evaluation_result = evaluator_crew.kickoff()
            evaluation_data = json.loads(evaluation_result) if isinstance(evaluation_result, str) else evaluation_result
            
            results["phases"]["evaluation"] = {
                "status": "success",
                "assessment": evaluation_data,
            }
            logger.info("✅ Evaluation phase complete")
        except Exception as e:
            logger.error(f"Evaluation phase error: {e}")
            results["phases"]["evaluation"] = {"status": "failed", "error": str(e)}
        
        logger.info("🎉 Full learning cycle complete!")
        return results
    
    def run_quick_lesson(
        self,
        user_id: str,
        topic: str,
    ) -> Dict[str, Any]:
        """Quick lesson: Teach → Quiz (no planning)."""
        logger.info(f"📚 Quick lesson for user {user_id} on topic {topic}")
        
        user_profile = self.db.get_user_profile(user_id)
        if not user_profile:
            return {"error": "User profile not found"}
        
        results = {"user_id": user_id, "topic": topic, "phases": {}}
        
        # Teaching
        try:
            teacher_crew = Crew(
                agents=[self.agent_pool.teacher],
                tasks=[
                    create_teacher_task(
                        self.agent_pool.teacher,
                        student_name=user_profile.get("full_name"),
                        topic=topic,
                        age=user_profile.get("age", 15),
                        learning_goal=user_profile.get("learning_goals", ["General"])[0],
                    )
                ],
            )
            teaching_result = teacher_crew.kickoff()
            results["phases"]["teaching"] = {"status": "success", "content": teaching_result}
        except Exception as e:
            results["phases"]["teaching"] = {"status": "failed", "error": str(e)}
        
        # Quiz
        try:
            quiz_crew = Crew(
                agents=[self.agent_pool.quiz],
                tasks=[
                    create_quiz_task(
                        self.agent_pool.quiz,
                        student_name=user_profile.get("full_name"),
                        topic=topic,
                        difficulty="medium",
                        num_questions=3,
                    )
                ],
            )
            quiz_result = quiz_crew.kickoff()
            results["phases"]["quiz"] = {"status": "success", "quiz": json.loads(quiz_result) if isinstance(quiz_result, str) else quiz_result}
        except Exception as e:
            results["phases"]["quiz"] = {"status": "failed", "error": str(e)}
        
        return results
    
    def run_quiz_only(
        self,
        user_id: str,
        topic: str,
        difficulty: str = "medium",
    ) -> Dict[str, Any]:
        """Generate a practice quiz on demand."""
        logger.info(f"📝 Quiz generation for user {user_id} on topic {topic}")
        
        user_profile = self.db.get_user_profile(user_id)
        if not user_profile:
            return {"error": "User profile not found"}
        
        try:
            quiz_crew = Crew(
                agents=[self.agent_pool.quiz],
                tasks=[
                    create_quiz_task(
                        self.agent_pool.quiz,
                        student_name=user_profile.get("full_name"),
                        topic=topic,
                        difficulty=difficulty,
                        num_questions=5,
                    )
                ],
            )
            
            quiz_result = quiz_crew.kickoff()
            quiz_data = json.loads(quiz_result) if isinstance(quiz_result, str) else quiz_result
            
            return {
                "user_id": user_id,
                "topic": topic,
                "difficulty": difficulty,
                "quiz": quiz_data,
            }
        except Exception as e:
            logger.error(f"Quiz generation error: {e}")
            return {"error": str(e)}
    
    def evaluate_progress(
        self,
        user_id: str,
        topic: str,
        quiz_score: float,
        time_spent_minutes: int,
    ) -> Dict[str, Any]:
        """Evaluate student progress and provide recommendations."""
        logger.info(f"📊 Evaluating progress for user {user_id} on topic {topic}")
        
        user_profile = self.db.get_user_profile(user_id)
        if not user_profile:
            return {"error": "User profile not found"}
        
        # Get history
        quiz_history = self.db.get_quiz_history(user_id, topic, limit=10)
        previous_scores = [q.get("score", 0) for q in quiz_history]
        
        try:
            evaluator_crew = Crew(
                agents=[self.agent_pool.evaluator],
                tasks=[
                    create_evaluator_task(
                        self.agent_pool.evaluator,
                        student_name=user_profile.get("full_name"),
                        topic=topic,
                        score=quiz_score,
                        attempts=len(quiz_history) + 1,
                        time_spent_minutes=time_spent_minutes,
                        previous_scores=previous_scores,
                    )
                ],
            )
            
            evaluation_result = evaluator_crew.kickoff()
            evaluation_data = json.loads(evaluation_result) if isinstance(evaluation_result, str) else evaluation_result
            
            # Save to database
            mastery = evaluation_data.get("mastery_level", 0)
            self.db.update_progress(user_id, topic, mastery, len(quiz_history) + 1)
            
            return {
                "user_id": user_id,
                "topic": topic,
                "score": quiz_score,
                "evaluation": evaluation_data,
            }
        except Exception as e:
            logger.error(f"Evaluation error: {e}")
            return {"error": str(e)}


# Global crew instance
_crew_instance = None


def get_edumentor_crew() -> EduMentorCrew:
    """Get or create the EduMentorCrew singleton."""
    global _crew_instance
    if _crew_instance is None:
        _crew_instance = EduMentorCrew()
    return _crew_instance
