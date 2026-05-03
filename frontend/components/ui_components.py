# Reusable UI Components for Coursera-Inspired Design
# These functions help build consistent, professional UI elements

import streamlit as st
from typing import List, Dict, Any, Optional, Callable
import json

# ==================== STYLING UTILITIES ====================

def inject_custom_css():
    """Inject custom CSS for Coursera-like design."""
    with open("frontend/styles/coursera_style.css", "r") as f:
        css = f.read()
    
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def apply_page_config():
    """Apply professional page configuration."""
    st.set_page_config(
        page_title="EduMentor - Premium Learning Platform",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    inject_custom_css()


# ==================== NAVIGATION COMPONENTS ====================

def render_navbar(user_name: str = "Student", show_search: bool = True):
    """Render professional top navigation bar."""
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        st.markdown(
            "<div class='navbar-logo'>🎓 EduMentor</div>",
            unsafe_allow_html=True
        )
    
    if show_search:
        with col2:
            st.markdown("<div class='navbar-search'>", unsafe_allow_html=True)
            search = st.text_input(
                "Search courses, topics...",
                placeholder="Search...",
                label_visibility="collapsed"
            )
            st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown(
            f"""<div class='navbar-profile'>
                <span>{user_name}</span>
                <div class='profile-avatar'>{user_name[0].upper()}</div>
            </div>""",
            unsafe_allow_html=True
        )
    
    st.divider()
    
    return search if show_search else None


def render_sidebar(
    user_profile: Dict[str, Any],
    current_page: str,
):
    """Render professional sidebar navigation."""
    st.markdown("""
        <div class='sidebar'>
    """, unsafe_allow_html=True)
    
    # User Profile Section
    st.markdown(f"""
        <div class='sidebar-section'>
            <div style='text-align: center; padding: 1rem;'>
                <div class='profile-avatar' style='width: 80px; height: 80px; margin: 0 auto; font-size: 2rem;'>
                    {user_profile.get('full_name', 'Student')[0].upper()}
                </div>
                <p style='margin-top: 0.5rem; font-weight: 600;'>{user_profile.get('full_name', 'Student')}</p>
                <p style='font-size: 0.75rem; color: #6c757d;'>{user_profile.get('grade_level', 'Student')}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navigation Links
    nav_items = [
        ("📊 Dashboard", "dashboard"),
        ("📚 My Courses", "courses"),
        ("🎯 Learning Path", "learning_path"),
        ("📝 Wishlist", "wishlist"),
        ("📊 Progress", "progress"),
        ("⚙️ Settings", "settings"),
        ("🚪 Log Out", "logout"),
    ]
    
    for label, page in nav_items:
        is_active = current_page == page
        st.markdown(f"""
            <div class='sidebar-link {"active" if is_active else ""}' style='border-left: 4px solid {"#0056b3" if is_active else "transparent"};'>
                {label}
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)


# ==================== CARD COMPONENTS ====================

def render_course_card(
    course_title: str,
    instructor: str,
    thumbnail_emoji: str = "📚",
    rating: float = 4.8,
    duration: str = "4 weeks",
    level: str = "Beginner",
    enrolled: bool = False,
    on_click: Optional[Callable] = None,
):
    """Render a professional course card."""
    html = f"""
    <div class='course-card' style='cursor: pointer;'>
        <div class='course-thumbnail'>
            {thumbnail_emoji}
        </div>
        <div class='course-info'>
            <div class='course-title'>{course_title}</div>
            <div class='course-instructor'>By {instructor}</div>
            
            <div class='course-meta'>
                <div class='course-rating'>
                    ⭐ {rating} <span style='font-size: 0.75rem;'>(120)</span>
                </div>
                <span>{duration}</span>
            </div>
            
            <div class='course-footer'>
                <span class='course-level'>{level}</span>
                <span style='font-size: 0.75rem; color: #6c757d;'>
                    {"Enrolled" if enrolled else "Free"}
                </span>
            </div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_hero_section(
    title: str,
    subtitle: str,
    cta_text: str = "Get Started",
    cta_secondary: str = "Learn More",
):
    """Render professional hero section."""
    st.markdown(f"""
    <div class='hero'>
        <h1 class='hero-title'>{title}</h1>
        <p class='hero-subtitle'>{subtitle}</p>
        <div class='hero-action'>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        st.button(f"✨ {cta_text}", use_container_width=True)
    with col2:
        st.button(f"→ {cta_secondary}", use_container_width=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)


def render_progress_card(
    title: str,
    current: int,
    total: int,
    icon: str = "🎯",
):
    """Render a progress summary card."""
    percentage = (current / total) * 100 if total > 0 else 0
    
    st.markdown(f"""
    <div class='card' style='padding: 1.5rem;'>
        <div style='font-size: 2rem; margin-bottom: 0.5rem;'>{icon}</div>
        <h3 style='margin: 0 0 0.5rem 0; font-size: 1.125rem;'>{title}</h3>
        <p style='color: #6c757d; margin: 0 0 1rem 0;'>{current} of {total}</p>
        <div class='progress-container' style='margin: 0;'>
            <div class='progress-bar'>
                <div class='progress-fill' style='width: {percentage}%;'></div>
            </div>
            <p style='font-size: 0.875rem; color: #6c757d; margin-top: 0.5rem;'>{percentage:.0f}% Complete</p>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ==================== COURSE DETAIL COMPONENTS ====================

def render_course_header(
    course_title: str,
    instructor: str,
    rating: float,
    students: int,
    duration: str,
    level: str,
):
    """Render course header with key info."""
    st.markdown(f"""
    <div class='card' style='margin-bottom: 2rem;'>
        <div class='card-body'>
            <h1 style='margin: 0 0 0.5rem 0;'>{course_title}</h1>
            <p style='font-size: 1.125rem; color: #6c757d; margin: 0 0 1rem 0;'>Taught by AI Tutor • {instructor}</p>
            
            <div style='display: flex; gap: 2rem; margin: 1.5rem 0;'>
                <div>
                    <strong>⭐ {rating}</strong>
                    <span style='color: #6c757d;'> Rating ({students} reviews)</span>
                </div>
                <div>
                    <strong>👥 {students:,}</strong>
                    <span style='color: #6c757d;'> Students Enrolled</span>
                </div>
                <div>
                    <strong>⏱️ {duration}</strong>
                    <span style='color: #6c757d;'> Course Duration</span>
                </div>
                <div>
                    <strong>📊 {level}</strong>
                    <span style='color: #6c757d;'> Difficulty</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_curriculum_section(
    weeks_data: List[Dict[str, Any]],
):
    """Render expandable curriculum section."""
    st.markdown("<h2 style='margin-bottom: 1.5rem;'>Course Curriculum</h2>", unsafe_allow_html=True)
    
    total_lessons = sum(len(week.get("lessons", [])) for week in weeks_data)
    total_duration = sum(week.get("duration_minutes", 0) for week in weeks_data)
    
    st.info(f"📚 {len(weeks_data)} weeks • {total_lessons} lessons • {total_duration} minutes")
    
    for i, week in enumerate(weeks_data, 1):
        with st.expander(f"Week {i}: {week.get('title', 'Module')} ({week.get('duration_minutes', 0)} min)"):
            lessons = week.get("lessons", [])
            for j, lesson in enumerate(lessons, 1):
                col1, col2 = st.columns([0.1, 0.9])
                with col1:
                    st.write(f"{j}.")
                with col2:
                    st.write(f"**{lesson.get('title', 'Lesson')}** ({lesson.get('duration_minutes', 0)} min)")


def render_learning_outcomes(outcomes: List[str]):
    """Render learning outcomes list."""
    st.markdown("<h3>What You'll Learn</h3>", unsafe_allow_html=True)
    
    for outcome in outcomes:
        st.markdown(f"✓ {outcome}")


# ==================== IN-COURSE EXPERIENCE ====================

def render_lesson_player(
    lesson_title: str,
    lesson_content: str,
    has_audio: bool = True,
):
    """Render lesson content player."""
    st.markdown(f"""
    <div class='card' style='padding: 2rem; margin-bottom: 2rem;'>
        <h2 style='margin-bottom: 1rem;'>{lesson_title}</h2>
        <div style='background: linear-gradient(135deg, #0056b3, #17a2b8); 
                    color: white; padding: 3rem; border-radius: 0.5rem; 
                    text-align: center; margin-bottom: 1.5rem; font-size: 3rem;'>
            📹
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(lesson_content)
    
    if has_audio:
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("🔊 Listen to Lesson"):
                st.info("Playing audio explanation...")


def render_module_sidebar(
    modules: List[Dict[str, Any]],
    current_module_id: str,
):
    """Render side-by-side module navigation."""
    st.markdown("<h4>Course Modules</h4>", unsafe_allow_html=True)
    
    for module in modules:
        is_current = module.get("id") == current_module_id
        is_completed = module.get("completed", False)
        
        status_icon = "✓" if is_completed else "▷"
        active_style = "background-color: #e7f1ff; border-left: 4px solid #0056b3;" if is_current else ""
        
        st.markdown(f"""
        <div class='module-item' style='{active_style}'>
            <div class='module-title'>{status_icon} {module.get('title', 'Module')}</div>
            <div class='module-duration'>{module.get('duration_minutes', 0)} min</div>
        </div>
        """, unsafe_allow_html=True)


def render_quiz_interface(
    questions: List[Dict[str, Any]],
):
    """Render interactive quiz interface."""
    st.markdown("<h3>Test Your Knowledge</h3>", unsafe_allow_html=True)
    
    user_answers = {}
    
    for i, q in enumerate(questions, 1):
        st.markdown(f"""
        <div class='card' style='padding: 1.5rem; margin-bottom: 1.5rem;'>
            <h4 style='margin: 0 0 1rem 0;'>Question {i}</h4>
            <p style='margin: 0 0 1rem 0;'>{q.get('question', '')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if q.get("type") == "multiple_choice":
            options = q.get("options", [])
            answer = st.radio(
                f"Answer {i}",
                options,
                label_visibility="collapsed",
                key=f"q_{i}"
            )
            user_answers[i] = answer
        else:
            answer = st.text_area(
                f"Answer {i}",
                label_visibility="collapsed",
                key=f"q_{i}"
            )
            user_answers[i] = answer
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("⬅️ Previous Lesson", use_container_width=True):
            st.info("Loading previous lesson...")
    with col2:
        if st.button("Submit Answers ✓", use_container_width=True):
            st.success("Quiz submitted! Evaluating your answers...")
    
    return user_answers


def render_progress_sidebar(
    course_progress: float,
    modules_completed: int,
    total_modules: int,
    streak_days: int = 0,
):
    """Render progress tracking sidebar."""
    st.markdown(f"""
    <div class='card' style='padding: 1.5rem; margin-bottom: 1.5rem;'>
        <h4 style='margin: 0 0 1rem 0;'>📊 Progress</h4>
        <div class='progress-container' style='margin: 0 0 1rem 0;'>
            <div class='progress-label' style='margin: 0 0 0.5rem 0;'>
                <span>Course Progress</span>
                <strong>{course_progress:.0f}%</strong>
            </div>
            <div class='progress-bar'>
                <div class='progress-fill' style='width: {course_progress}%;'></div>
            </div>
        </div>
        
        <div style='background: #f8f9fa; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem;'>
            <p style='margin: 0 0 0.5rem 0;'><strong>{modules_completed}/{total_modules}</strong></p>
            <p style='margin: 0; font-size: 0.875rem; color: #6c757d;'>Modules Completed</p>
        </div>
        
        <div style='background: #fff3cd; padding: 1rem; border-radius: 0.5rem;'>
            <p style='margin: 0;'>🔥 <strong>{streak_days} Day Streak</strong></p>
            <p style='margin: 0.5rem 0 0 0; font-size: 0.875rem;'>Keep it going!</p>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ==================== UTILITY COMPONENTS ====================

def render_badge(text: str, badge_type: str = "primary"):
    """Render a badge."""
    type_class = f"badge-{badge_type}"
    st.markdown(f"<span class='badge {type_class}'>{text}</span>", unsafe_allow_html=True)


def render_breadcrumb(items: List[str]):
    """Render breadcrumb navigation."""
    breadcrumb = " / ".join(items)
    st.markdown(f"<p style='font-size: 0.875rem; color: #6c757d;'>{breadcrumb}</p>", unsafe_allow_html=True)


def render_empty_state(
    title: str,
    description: str,
    icon: str = "📚",
    action_text: str = "Get Started",
):
    """Render empty state."""
    st.markdown(f"""
    <div style='text-align: center; padding: 3rem;'>
        <div style='font-size: 3rem; margin-bottom: 1rem;'>{icon}</div>
        <h3>{title}</h3>
        <p style='color: #6c757d; margin-bottom: 1.5rem;'>{description}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.button(action_text, use_container_width=True)
