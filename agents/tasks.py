# Task definitions for CrewAI agents

from crewai import Task
from config.prompts import (
    PLANNER_TASK, TEACHER_TASK, QUIZ_TASK, EVALUATOR_TASK
)
from utils.logger import setup_logger

logger = setup_logger(__name__)


def create_planner_task(agent, **kwargs) -> Task:
    """Create a study planning task."""
    description = PLANNER_TASK.format(
        duration=kwargs.get("duration", "weekly"),
        student_name=kwargs.get("student_name", "Student"),
        topic=kwargs.get("topic", "General"),
        level=kwargs.get("level", "beginner"),
        daily_time=kwargs.get("daily_time", 30),
        learning_goals=kwargs.get("learning_goals", "General Knowledge"),
    )
    
    return Task(
        description=description,
        expected_output="A detailed JSON study plan with daily lessons, milestones, and time allocations",
        agent=agent,
    )


def create_teacher_task(agent, **kwargs) -> Task:
    """Create a teaching/explanation task."""
    description = TEACHER_TASK.format(
        student_name=kwargs.get("student_name", "Student"),
        topic=kwargs.get("topic", "General"),
        age=kwargs.get("age", 15),
        learning_goal=kwargs.get("learning_goal", "General Knowledge"),
    )
    
    return Task(
        description=description,
        expected_output="A clear, engaging explanation with Pakistani examples and analogies",
        agent=agent,
    )


def create_quiz_task(agent, **kwargs) -> Task:
    """Create a quiz generation/evaluation task."""
    description = QUIZ_TASK.format(
        difficulty=kwargs.get("difficulty", "medium"),
        student_name=kwargs.get("student_name", "Student"),
        topic=kwargs.get("topic", "General"),
        num_questions=kwargs.get("num_questions", 5),
        student_level=kwargs.get("student_level", "beginner"),
    )
    
    return Task(
        description=description,
        expected_output="A JSON quiz with questions, multiple choice options, correct answers, and explanations",
        agent=agent,
    )


def create_evaluator_task(agent, **kwargs) -> Task:
    """Create a progress evaluation task."""
    description = EVALUATOR_TASK.format(
        student_name=kwargs.get("student_name", "Student"),
        topic=kwargs.get("topic", "General"),
        score=kwargs.get("score", 0),
        attempts=kwargs.get("attempts", 1),
        time_spent_minutes=kwargs.get("time_spent_minutes", 0),
        previous_scores=kwargs.get("previous_scores", []),
    )
    
    return Task(
        description=description,
        expected_output="JSON analysis with mastery level, risk flags, and recommendations",
        agent=agent,
    )
