"""
Example: Complete EduMentor Learning Session

This demonstrates the full workflow:
1. User logs in
2. System creates a personalized study plan
3. Teacher explains the concept
4. Quiz agent generates adaptive questions
5. Evaluator assesses mastery and recommends next steps

Run this to see the multi-agent system in action!
"""

import json
import sys
from typing import Dict, Any
from crew.crew import get_edumentor_crew
from utils.logger import setup_logger

logger = setup_logger(__name__)


def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


def print_json(data: Dict[str, Any], indent: int = 2):
    """Pretty print JSON data."""
    print(json.dumps(data, indent=indent))


def example_user_profile() -> Dict[str, Any]:
    """
    Example user profile (in a real app, fetch from Supabase).
    This shows what data the agents need.
    """
    return {
        "id": "user_123",
        "full_name": "Ahmed Ali",
        "age": 15,
        "grade_level": "Secondary / Matric (Grade 9–10)",
        "preferred_language": "English",
        "province": "Punjab",
        "learning_goals": ["Computer Science", "Mathematics"],
        "academic_board": "Federal Board",
        "learning_challenges": "Struggles with abstract concepts, prefers practical examples",
        "onboarding_complete": True,
    }


def run_complete_session():
    """Run a complete learning cycle."""
    print_section("🎓 EduMentor Multi-Agent Learning Session")
    
    # Initialize crew
    logger.info("Initializing EduMentor Crew...")
    crew = get_edumentor_crew()
    
    # Example user and topic
    user_id = "user_123"
    topic = "Introduction to Artificial Intelligence"
    
    print(f"👤 Student: Ahmed Ali (Age 15, Grade 9-10)")
    print(f"📚 Topic: {topic}")
    print(f"🎯 Goals: Computer Science, Mathematics")
    
    # ==================== RUN FULL CYCLE ====================
    print_section("🚀 Starting Full Learning Cycle")
    print("Phases: Planning → Teaching → Quiz → Evaluation\n")
    
    try:
        result = crew.run_full_learning_cycle(
            user_id=user_id,
            topic=topic,
            duration="weekly",
            difficulty="medium",
        )
        
        # Display results
        for phase, phase_data in result.get("phases", {}).items():
            print_section(f"✅ Phase: {phase.upper()}")
            
            if phase_data.get("status") == "success":
                if phase == "planning":
                    print("📋 Study Plan Generated:")
                    if isinstance(phase_data.get("plan"), dict):
                        print_json(phase_data["plan"])
                    else:
                        print(phase_data["plan"])
                
                elif phase == "teaching":
                    print("📚 Lesson Explanation:")
                    print(phase_data.get("explanation", ""))
                
                elif phase == "quiz":
                    print("🧠 Quiz Generated:")
                    questions = phase_data.get("questions", [])
                    for q in questions[:2]:  # Show first 2
                        print(f"\nQ: {q.get('question', '')}")
                        if q.get("type") == "multiple_choice":
                            for i, opt in enumerate(q.get("options", []), 1):
                                print(f"   {i}. {opt}")
                        print(f"✓ Answer: {q.get('correct_answer', '')}")
                
                elif phase == "evaluation":
                    print("📊 Assessment & Recommendations:")
                    assessment = phase_data.get("assessment", {})
                    print(f"Mastery Level: {assessment.get('mastery_level', 0):.0%}")
                    print(f"Status: {assessment.get('status', 'unknown')}")
                    print(f"Recommendation: {assessment.get('recommendation', 'continue')}")
                    print(f"Insights: {', '.join(assessment.get('insights', []))}")
            
            else:
                print(f"❌ Error: {phase_data.get('error', 'Unknown error')}")
        
        return result
    
    except Exception as e:
        logger.error(f"Session error: {e}", exc_info=True)
        print(f"❌ Error: {e}")
        return None


def run_quick_lesson():
    """Run a quick lesson (Teach + Quiz only)."""
    print_section("⚡ Quick Lesson (Teach + Quiz)")
    
    crew = get_edumentor_crew()
    user_id = "user_123"
    topic = "Machine Learning Basics"
    
    print(f"📚 Topic: {topic}\n")
    
    try:
        result = crew.run_quick_lesson(user_id, topic)
        
        if result.get("phases", {}).get("teaching", {}).get("status") == "success":
            print("📚 Lesson:")
            print(result["phases"]["teaching"]["content"][:500] + "...")
        
        if result.get("phases", {}).get("quiz", {}).get("status") == "success":
            print("\n🧠 Quick Quiz Generated (3 questions)")
        
        return result
    
    except Exception as e:
        logger.error(f"Quick lesson error: {e}")
        print(f"❌ Error: {e}")
        return None


def run_quiz_practice():
    """Run a practice quiz."""
    print_section("📝 Practice Quiz")
    
    crew = get_edumentor_crew()
    user_id = "user_123"
    topic = "Algorithms"
    
    print(f"📚 Topic: {topic}")
    print(f"📊 Difficulty: Medium\n")
    
    try:
        result = crew.run_quiz_only(user_id, topic, difficulty="medium")
        
        quiz_data = result.get("quiz", {})
        questions = quiz_data.get("questions", [])
        
        print(f"Generated {len(questions)} questions:\n")
        for i, q in enumerate(questions, 1):
            print(f"{i}. {q.get('question', '')}")
        
        return result
    
    except Exception as e:
        logger.error(f"Quiz error: {e}")
        print(f"❌ Error: {e}")
        return None


def run_progress_evaluation():
    """Run a progress evaluation."""
    print_section("📊 Progress Evaluation")
    
    crew = get_edumentor_crew()
    user_id = "user_123"
    topic = "Linear Algebra"
    
    print(f"📚 Topic: {topic}")
    print(f"🎯 Quiz Score: 82%")
    print(f"⏱️ Time Spent: 25 minutes\n")
    
    try:
        result = crew.evaluate_progress(
            user_id=user_id,
            topic=topic,
            quiz_score=0.82,
            time_spent_minutes=25,
        )
        
        evaluation = result.get("evaluation", {})
        
        print(f"Mastery Level: {evaluation.get('mastery_level', 0):.0%}")
        print(f"Status: {evaluation.get('status', 'unknown')}")
        print(f"Risk Level: {evaluation.get('risk_level', 'unknown')}")
        print(f"\n📝 Recommendation: {evaluation.get('recommendation', 'continue')}")
        print(f"\n💡 Next Steps:")
        for step in evaluation.get("next_steps", []):
            print(f"   - {step}")
        
        return result
    
    except Exception as e:
        logger.error(f"Evaluation error: {e}")
        print(f"❌ Error: {e}")
        return None


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="EduMentor Multi-Agent System Demo")
    parser.add_argument(
        "--mode",
        choices=["full", "quick", "quiz", "eval"],
        default="full",
        help="Which workflow to run",
    )
    
    args = parser.parse_args()
    
    print("\n")
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║           🎓 EduMentor Multi-Agent AI Tutor System 🎓             ║")
    print("║                                                                    ║")
    print("║   Powered by: CrewAI + Gemini/Groq + Supabase + Voice I/O        ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    
    if args.mode == "full":
        run_complete_session()
    elif args.mode == "quick":
        run_quick_lesson()
    elif args.mode == "quiz":
        run_quiz_practice()
    elif args.mode == "eval":
        run_progress_evaluation()
    
    print_section("✅ Session Complete!")
    print("Check logs/edumentor_agents.log for detailed execution logs.\n")


if __name__ == "__main__":
    main()
