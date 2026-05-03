# Homepage / Dashboard - Premium Modern Design

import streamlit as st
from frontend.components.ui_components import (
    render_navbar,
    render_hero_section,
    render_course_card,
    render_progress_card,
    render_breadcrumb,
    render_empty_state,
)
from typing import Dict, Any


def render_home_page(user_profile: Dict[str, Any]):
    """Render the premium homepage/dashboard."""
    
    # Header
    render_navbar(user_profile.get("full_name", "Student"))
    render_breadcrumb(["Home"])
    
    # Welcome Section
    st.markdown(f"""
    <div style='margin: 2rem 0;'>
        <h1 style='font-size: 2.25rem; font-weight: 700;'>
            Welcome back, {user_profile.get('full_name', 'Student')}! 👋
        </h1>
        <p style='font-size: 1.125rem; color: #6c757d;'>
            Continue your learning journey and unlock new skills.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ==================== CONTINUE LEARNING SECTION ====================
    st.markdown("<h2 style='margin: 2rem 0 1.5rem 0; font-weight: 700;'>Continue Learning</h2>", unsafe_allow_html=True)
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_progress_card("In Progress", 2, 5, "📚")
    with col2:
        render_progress_card("Completed", 3, 8, "✅")
    with col3:
        render_progress_card("Learning Streak", 12, 30, "🔥")
    with col4:
        render_progress_card("Achievement Points", 450, 1000, "⭐")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Active Courses
    st.markdown("<h3 style='margin-top: 2rem; margin-bottom: 1.5rem;'>Your Active Courses</h3>", unsafe_allow_html=True)
    
    cols = st.columns(3)
    
    # Course 1: AI Fundamentals
    with cols[0]:
        render_course_card(
            course_title="AI Fundamentals: Adaptive Course",
            instructor="AI Tutor",
            thumbnail_emoji="🤖",
            rating=4.8,
            duration="4 weeks",
            level="Beginner",
            enrolled=True,
        )
        if st.button("▶️ Continue", key="continue_1", use_container_width=True):
            st.session_state.current_page = "learning"
    
    # Course 2: Machine Learning Basics
    with cols[1]:
        render_course_card(
            course_title="Machine Learning Basics",
            instructor="AI Tutor",
            thumbnail_emoji="🧠",
            rating=4.7,
            duration="6 weeks",
            level="Intermediate",
            enrolled=True,
        )
        if st.button("▶️ Continue", key="continue_2", use_container_width=True):
            st.session_state.current_page = "learning"
    
    # Course 3: Advanced Algorithms
    with cols[2]:
        render_course_card(
            course_title="Advanced Algorithms",
            instructor="AI Tutor",
            thumbnail_emoji="📊",
            rating=4.6,
            duration="8 weeks",
            level="Advanced",
            enrolled=True,
        )
        if st.button("▶️ Continue", key="continue_3", use_container_width=True):
            st.session_state.current_page = "learning"
    
    # ==================== RECOMMENDED COURSES ====================
    st.markdown("---")
    st.markdown("<h2 style='margin: 2rem 0 1.5rem 0; font-weight: 700;'>Recommended for You</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #6c757d; margin-bottom: 1.5rem;'>Based on your interests in Computer Science and Mathematics</p>", unsafe_allow_html=True)
    
    rec_cols = st.columns(3)
    
    # Recommended 1
    with rec_cols[0]:
        render_course_card(
            course_title="Python for Data Science",
            instructor="AI Tutor",
            thumbnail_emoji="🐍",
            rating=4.9,
            duration="5 weeks",
            level="Intermediate",
            enrolled=False,
        )
        if st.button("Explore", key="explore_1", use_container_width=True):
            st.session_state.current_page = "course_detail"
    
    # Recommended 2
    with rec_cols[1]:
        render_course_card(
            course_title="Web Development Fundamentals",
            instructor="AI Tutor",
            thumbnail_emoji="🌐",
            rating=4.7,
            duration="4 weeks",
            level="Beginner",
            enrolled=False,
        )
        if st.button("Explore", key="explore_2", use_container_width=True):
            st.session_state.current_page = "course_detail"
    
    # Recommended 3
    with rec_cols[2]:
        render_course_card(
            course_title="Cloud Computing Essentials",
            instructor="AI Tutor",
            thumbnail_emoji="☁️",
            rating=4.8,
            duration="6 weeks",
            level="Intermediate",
            enrolled=False,
        )
        if st.button("Explore", key="explore_3", use_container_width=True):
            st.session_state.current_page = "course_detail"
    
    # ==================== CATEGORIES ====================
    st.markdown("---")
    st.markdown("<h2 style='margin: 2rem 0 1.5rem 0; font-weight: 700;'>Explore by Category</h2>", unsafe_allow_html=True)
    
    cat_cols = st.columns(4)
    
    categories = [
        ("🤖", "Artificial Intelligence", "120 courses"),
        ("🐍", "Programming", "350 courses"),
        ("📊", "Data Science", "89 courses"),
        ("🌐", "Web Development", "156 courses"),
    ]
    
    for i, (emoji, name, count) in enumerate(categories):
        with cat_cols[i]:
            st.markdown(f"""
            <div class='card' style='padding: 1.5rem; text-align: center; cursor: pointer;'>
                <div style='font-size: 2rem; margin-bottom: 0.5rem;'>{emoji}</div>
                <h4 style='margin: 0.5rem 0;'>{name}</h4>
                <p style='color: #6c757d; margin: 0; font-size: 0.875rem;'>{count}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # ==================== FOOTER STATS ====================
    st.markdown("---")
    
    footer_cols = st.columns(4)
    
    with footer_cols[0]:
        st.metric("Total Learning Hours", "24.5 hrs", "+2.3 hrs this week")
    
    with footer_cols[1]:
        st.metric("Certificates Earned", 2, "+1 this month")
    
    with footer_cols[2]:
        st.metric("Current Streak", "12 days", "🔥 Keep it up!")
    
    with footer_cols[3]:
        st.metric("Completion Rate", "68%", "+5% improvement")
