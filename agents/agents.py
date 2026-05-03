# All 4 EduMentor agents with specialized roles and capabilities

from crewai import Agent
from langchain.tools import Tool
from typing import List, Callable, Any, Dict
from config.settings import AGENT_CONFIGS
from agents.tools import AGENT_TOOLS
from utils.fallback_llm import get_llm_client
from utils.logger import setup_logger

logger = setup_logger(__name__)


def _create_tools_list() -> List[Tool]:
    """Convert tool tuples to CrewAI Tool objects."""
    tools = []
    
    for category, tool_list in AGENT_TOOLS.items():
        for tool_name, tool_func in tool_list:
            tool = Tool(
                name=tool_name,
                func=tool_func,
                description=f"{tool_name}: {tool_func.__doc__ or 'Tool for agent use'}"
            )
            tools.append(tool)
    
    return tools


def create_planner_agent() -> Agent:
    """
    PLANNER AGENT
    ✅ Creates personalized daily/weekly study plans
    ✅ Considers student level, progress, and goals
    ✅ Recommends topics, time allocations, and milestones
    ✅ Adapts based on performance history
    """
    config = AGENT_CONFIGS["planner"]
    
    planner_prompt = """
    You are an expert curriculum designer specializing in personalized learning.
    Your role is to create adaptive study plans that:
    1. Break complex topics into manageable daily lessons
    2. Allocate time based on student level and commitment
    3. Include buffer days for review and practice
    4. Add local (Pakistani) context and examples
    5. Suggest realistic milestones and checkpoints
    
    Always output your plan as a structured JSON with daily/weekly breakdowns.
    Include time estimates for each module.
    """
    
    llm_client = get_llm_client()
    
    agent = Agent(
        role=config["role"],
        goal=config["goal"],
        backstory=config["backstory"],
        verbose=config["verbose"],
        allow_delegation=False,
        tools=_create_tools_list(),
        llm=llm_client,  # Use fallback LLM
    )
    
    agent.role_prompt = planner_prompt
    
    return agent


def create_teacher_agent() -> Agent:
    """
    TEACHER AGENT
    ✅ Explains concepts with Pakistani examples
    ✅ Creates age-appropriate analogies
    ✅ Uses simple, conversational language
    ✅ Connects to student's interests
    ✅ Supports voice output
    """
    config = AGENT_CONFIGS["teacher"]
    
    teacher_prompt = """
    You are an elite, patient, and engaging teacher for Pakistani students.
    Your teaching philosophy:
    1. Use SIMPLE language appropriate for the student's age
    2. Use real Pakistani examples (cities, traditions, local culture)
    3. Create analogies relevant to their daily life
    4. Break concepts into small, digestible pieces
    5. Encourage curiosity and deeper thinking
    6. NO complex jargon - be conversational
    7. Format for voice (no markdown, clear pronunciation)
    
    If asked off-topic questions, gently redirect to the current lesson.
    Always connect new concepts to what they already know.
    """
    
    llm_client = get_llm_client()
    
    agent = Agent(
        role=config["role"],
        goal=config["goal"],
        backstory=config["backstory"],
        verbose=config["verbose"],
        allow_delegation=False,
        tools=_create_tools_list(),
        llm=llm_client,
    )
    
    agent.role_prompt = teacher_prompt
    
    return agent


def create_quiz_agent() -> Agent:
    """
    QUIZ AGENT
    ✅ Generates adaptive quizzes (multiple choice + short answer)
    ✅ Evaluates student responses
    ✅ Provides detailed feedback
    ✅ Adjusts difficulty based on performance
    ✅ Tracks progress and struggle patterns
    """
    config = AGENT_CONFIGS["quiz"]
    
    quiz_prompt = """
    You are an expert assessment designer and evaluator.
    Your role:
    1. Generate quizzes that match the student's level
    2. Mix multiple choice (fact-checking) and short answer (deeper thinking)
    3. Create clear, unambiguous questions
    4. Provide detailed explanations for answers
    5. Use Pakistani context where possible
    6. Evaluate student responses fairly
    7. Give constructive feedback
    8. Identify knowledge gaps
    
    Always output quizzes as JSON with clear structure:
    {
        "questions": [
            {
                "id": 1,
                "question": "...",
                "type": "multiple_choice|short_answer",
                "options": ["...", "..."],
                "correct_answer": "...",
                "explanation": "..."
            }
        ]
    }
    """
    
    llm_client = get_llm_client()
    
    agent = Agent(
        role=config["role"],
        goal=config["goal"],
        backstory=config["backstory"],
        verbose=config["verbose"],
        allow_delegation=False,
        tools=_create_tools_list(),
        llm=llm_client,
    )
    
    agent.role_prompt = quiz_prompt
    
    return agent


def create_evaluator_agent() -> Agent:
    """
    EVALUATOR / PROGRESS AGENT
    ✅ Tracks mastery levels across topics
    ✅ Detects when students are struggling
    ✅ Recommends adaptive interventions
    ✅ Decides when to advance, repeat, or simplify
    ✅ Updates progress in database
    ✅ Identifies at-risk students
    """
    config = AGENT_CONFIGS["evaluator"]
    
    evaluator_prompt = """
    You are a learning analytics expert using data to optimize student outcomes.
    Your role:
    1. Analyze quiz performance trends (improving? plateauing? declining?)
    2. Calculate mastery level (0-1 scale)
    3. Identify knowledge gaps and struggle patterns
    4. Recommend interventions (repeat, simplify, practice more, etc.)
    5. Flag at-risk students for extra support
    6. Decide when students are ready to advance
    7. Provide actionable feedback to teachers and students
    
    Consider:
    - Recent quiz scores vs. historical performance
    - Time spent vs. performance ratio (efficiency)
    - Number of attempts needed
    - Common mistake patterns
    - Improvement rate (are they getting better?)
    
    Output JSON:
    {
        "mastery_level": 0.0-1.0,
        "status": "not_started|struggling|on_track|mastered",
        "risk_level": "low|medium|high",
        "recommendation": "repeat|practice|advance|simplify",
        "insights": ["...", "..."],
        "next_steps": ["..."]
    }
    """
    
    llm_client = get_llm_client()
    
    agent = Agent(
        role=config["role"],
        goal=config["goal"],
        backstory=config["backstory"],
        verbose=config["verbose"],
        allow_delegation=False,
        tools=_create_tools_list(),
        llm=llm_client,
    )
    
    agent.role_prompt = evaluator_prompt
    
    return agent


# ==================== AGENT POOL ====================
class AgentPool:
    """Manage all agents."""
    
    def __init__(self):
        """Initialize all agents."""
        logger.info("Initializing EduMentor Multi-Agent System...")
        
        self.planner = create_planner_agent()
        self.teacher = create_teacher_agent()
        self.quiz = create_quiz_agent()
        self.evaluator = create_evaluator_agent()
        
        logger.info("✅ All 4 agents initialized successfully!")
    
    def get_agent(self, role: str) -> Agent:
        """Get an agent by role name."""
        agents = {
            "planner": self.planner,
            "teacher": self.teacher,
            "quiz": self.quiz,
            "evaluator": self.evaluator,
        }
        return agents.get(role.lower())


# Global pool
_agent_pool = None


def get_agent_pool() -> AgentPool:
    """Get or create the agent pool."""
    global _agent_pool
    if _agent_pool is None:
        _agent_pool = AgentPool()
    return _agent_pool
