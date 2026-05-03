# In-Course Learning Experience - Premium Player

import streamlit as st
from frontend.components.ui_components import (
    render_navbar,
    render_breadcrumb,
    render_lesson_player,
    render_module_sidebar,
    render_progress_sidebar,
    render_quiz_interface,
)
from typing import Dict, Any, List


def render_learning_experience(
    user_profile: Dict[str, Any],
    course_title: str = "AI Fundamentals",
    current_module_id: str = "module_1",
):
    """Render the premium in-course learning experience."""
    
    # Hide sidebar for immersive experience
    hide_sidebar = """
    <style>
        [data-testid="stSidebar"] {display: none}
    </style>
    """
    st.markdown(hide_sidebar, unsafe_allow_html=True)
    
    # Compact navbar
    render_navbar(user_profile.get("full_name", "Student"))
    st.markdown("<style>main { padding: 0; }</style>", unsafe_allow_html=True)
    
    # Breadcrumb
    render_breadcrumb(["Home", "Courses", course_title, "Lesson 1"])
    
    # ==================== THREE-COLUMN LAYOUT ====================
    left_col, main_col, right_col = st.columns([0.2, 0.6, 0.2])
    
    # ==================== LEFT SIDEBAR: MODULE LIST ====================
    with left_col:
        st.markdown("<h4 style='margin: 1.5rem 0 1rem 0;'>Course Content</h4>", unsafe_allow_html=True)
        
        modules = [
            {
                "id": "module_0",
                "title": "What is AI?",
                "duration_minutes": 15,
                "completed": True,
            },
            {
                "id": "module_1",
                "title": "History of AI",
                "duration_minutes": 20,
                "completed": False,
            },
            {
                "id": "module_2",
                "title": "AI in Real World",
                "duration_minutes": 25,
                "completed": False,
            },
            {
                "id": "module_3",
                "title": "Quiz: AI Basics",
                "duration_minutes": 10,
                "completed": False,
            },
            {
                "id": "module_4",
                "title": "Machine Learning",
                "duration_minutes": 30,
                "completed": False,
            },
        ]
        
        render_module_sidebar(modules, current_module_id)
    
    # ==================== MAIN CONTENT: LESSON PLAYER ====================
    with main_col:
        st.markdown("### Lesson 1: History of Artificial Intelligence")
        
        # Lesson Player with Video Placeholder
        render_lesson_player(
            lesson_title="The Evolution of AI",
            lesson_content="""
            <div style='background: linear-gradient(135deg, #0056b3, #17a2b8); 
                        color: white; padding: 4rem; border-radius: 0.5rem; 
                        text-align: center; margin-bottom: 2rem;'>
                <div style='font-size: 5rem; margin-bottom: 1rem;'>▶️</div>
                <p style='margin: 0; font-size: 1.125rem;'>Video Lesson: 20 minutes</p>
                <p style='margin: 0.5rem 0 0 0; opacity: 0.9;'>Artificial Intelligence has evolved dramatically over the past 60 years...</p>
            </div>
            
            <h3 style='margin: 2rem 0 1rem 0;'>Lesson Transcript</h3>
            
            <p><strong>Overview:</strong></p>
            <p>In this lesson, you'll learn about the fascinating history of Artificial Intelligence, 
            from its theoretical foundations in the 1950s to modern deep learning systems. We'll explore 
            key milestones, important personalities, and the technological breakthroughs that shaped the field.</p>
            
            <p><strong>Key Topics Covered:</strong></p>
            <ul>
                <li>The Turing Test and early AI concepts (1950s)</li>
                <li>Expert Systems and the AI winter (1970s-1980s)</li>
                <li>Machine Learning revolution (1990s-2000s)</li>
                <li>Deep Learning and neural networks (2010s)</li>
                <li>Transformer models and large language models (2020s)</li>
            </ul>
            
            <p><strong>Why This Matters:</strong></p>
            <p>Understanding the history helps you appreciate the current state of AI and understand 
            why certain approaches became dominant. It also helps you avoid repeating past mistakes 
            and understand the cyclical nature of AI advancement.</p>
            """,
            has_audio=True,
        )
        
        st.markdown("---")
        
        # Lesson Navigation Buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("⬅️ Previous Lesson", use_container_width=True):
                st.info("Loading previous lesson...")
        with col2:
            st.write("")  # Spacer
        with col3:
            if st.button("Next Lesson ➡️", use_container_width=True):
                st.info("Loading next lesson...")
    
    # ==================== RIGHT SIDEBAR: PROGRESS & INFO ====================
    with right_col:
        st.markdown("", unsafe_allow_html=True)
        
        # Progress Card
        render_progress_sidebar(
            course_progress=45.0,
            modules_completed=3,
            total_modules=12,
            streak_days=12,
        )
        
        # Notes Section
        st.markdown("<h4 style='margin: 1.5rem 0 1rem 0;'>📝 My Notes</h4>", unsafe_allow_html=True)
        note = st.text_area(
            "Add notes for this lesson",
            placeholder="Type your notes here...",
            height=150,
            label_visibility="collapsed"
        )
        if st.button("Save Note", key="save_note", use_container_width=True):
            st.success("Note saved!")
        
        st.markdown("---")
        
        # AI Tutor Chat
        st.markdown("<h4 style='margin: 1.5rem 0 1rem 0;'>💬 Ask AI Tutor</h4>", unsafe_allow_html=True)
        
        question = st.text_input(
            "Ask a question about this lesson",
            placeholder="e.g., Explain the Turing Test",
            label_visibility="collapsed"
        )
        
        if st.button("Get Help", key="get_help", use_container_width=True):
            st.info("""
            **AI Tutor Response:**
            
            The Turing Test is a measure of machine intelligence proposed by Alan Turing in 1950. 
            It suggests that if a machine's responses in written conversation are indistinguishable 
            from those of a human, then the machine can be considered intelligent.
            """)


def render_quiz_page(
    user_profile: Dict[str, Any],
    course_title: str = "AI Fundamentals",
    module_number: int = 1,
):
    """Render the quiz/assessment page."""
    
    render_navbar(user_profile.get("full_name", "Student"))
    render_breadcrumb(["Home", "Courses", course_title, f"Module {module_number} Quiz"])
    
    # Quiz Header
    st.markdown(f"""
    <div class='card' style='padding: 2rem; margin-bottom: 2rem; background: #e7f1ff;'>
        <h2 style='margin: 0 0 0.5rem 0; color: #0056b3;'>Module {module_number} Assessment</h2>
        <p style='margin: 0; color: #6c757d;'>
            Test your understanding of the concepts covered in this module.
            You need to score <strong>75% or higher</strong> to unlock the next module.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quiz Questions
    questions = [
        {
            "question": "When was the Turing Test proposed?",
            "type": "multiple_choice",
            "options": ["1935", "1950", "1965", "1980"],
            "correct": "1950",
        },
        {
            "question": "What was the primary focus of Expert Systems?",
            "type": "multiple_choice",
            "options": [
                "Emulating human intelligence",
                "Replicating expert knowledge in specific domains",
                "Creating robots",
                "Building self-driving cars"
            ],
            "correct": "Replicating expert knowledge in specific domains",
        },
        {
            "question": "Explain the AI Winter and why it occurred.",
            "type": "short_answer",
            "correct": "Periods when AI research saw reduced funding and interest due to unmet expectations",
        },
        {
            "question": "How did deep learning change the AI landscape?",
            "type": "short_answer",
            "correct": "Deep learning enabled better feature extraction and improved performance on complex tasks",
        },
    ]
    
    user_answers = render_quiz_interface(questions)
    
    # Submit and Navigation
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("⬅️ Back to Lesson", use_container_width=True):
            st.session_state.current_page = "learning"
    with col3:
        if st.button("Submit Quiz ✓", use_container_width=True):
            # Simulate scoring
            st.success("""
            ### Quiz Complete! 🎉
            
            **Your Score: 85% (3.4/4 points)**
            
            Great work! You've successfully completed this module assessment.
            Your performance has been recorded and you're ready to move to the next module.
            """)
            
            col_next1, col_next2 = st.columns(2)
            with col_next1:
                if st.button("Review Answers"):
                    st.info("Showing detailed answer review...")
            with col_next2:
                if st.button("Next Module ➡️", use_container_width=True):
                    st.session_state.current_page = "learning"
