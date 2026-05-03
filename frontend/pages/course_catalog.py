# Course Catalog - Discovery & Search

import streamlit as st
from frontend.components.ui_components import (
    render_navbar,
    render_course_card,
    render_breadcrumb,
    render_empty_state,
)
from typing import Dict, Any


def render_course_catalog(user_profile: Dict[str, Any]):
    """Render the course catalog with search and filters."""
    
    # Header
    render_navbar(user_profile.get("full_name", "Student"))
    render_breadcrumb(["Home", "Course Catalog"])
    
    # Page Title
    st.markdown("""
    <div style='margin: 2rem 0;'>
        <h1 style='font-size: 2.25rem; font-weight: 700;'>
            Discover Courses & Expand Your Knowledge
        </h1>
        <p style='font-size: 1.125rem; color: #6c757d;'>
            Explore our collection of expertly designed courses across multiple domains.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ==================== SEARCH & FILTERS ====================
    st.markdown("<h3 style='margin: 1.5rem 0;'>Find the Right Course</h3>", unsafe_allow_html=True)
    
    # Search input
    search = st.text_input(
        "🔍 Search by course name, topic, or instructor",
        placeholder="e.g., Machine Learning, Python, Web Development"
    )
    
    # Filters Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        level_filter = st.multiselect(
            "Level",
            ["Beginner", "Intermediate", "Advanced", "Expert"],
            default=["Beginner", "Intermediate"]
        )
    
    with col2:
        duration_filter = st.multiselect(
            "Duration",
            ["< 2 weeks", "2-4 weeks", "4-8 weeks", "> 8 weeks"],
            default=["2-4 weeks", "4-8 weeks"]
        )
    
    with col3:
        category_filter = st.multiselect(
            "Category",
            ["AI & ML", "Programming", "Data Science", "Web Dev", "Cloud"],
            default=["AI & ML", "Programming"]
        )
    
    with col4:
        sort_by = st.selectbox(
            "Sort By",
            ["Most Popular", "Newest", "Highest Rated", "Most Students"]
        )
    
    # Applied Filters Info
    st.info(f"Showing courses for: {user_profile.get('preferred_language', 'English')} • Level: {', '.join(level_filter)}")
    
    # ==================== COURSE GRID ====================
    st.markdown("---")
    
    # Sample courses data
    courses_data = [
        {
            "title": "AI Fundamentals: Adaptive Course",
            "instructor": "AI Tutor",
            "emoji": "🤖",
            "rating": 4.8,
            "duration": "4 weeks",
            "level": "Beginner",
            "students": 2543,
            "enrolled": True,
        },
        {
            "title": "Machine Learning Basics",
            "instructor": "AI Tutor",
            "emoji": "🧠",
            "rating": 4.7,
            "duration": "6 weeks",
            "level": "Intermediate",
            "students": 1834,
            "enrolled": True,
        },
        {
            "title": "Advanced Algorithms",
            "instructor": "AI Tutor",
            "emoji": "📊",
            "rating": 4.6,
            "duration": "8 weeks",
            "level": "Advanced",
            "students": 892,
            "enrolled": True,
        },
        {
            "title": "Python for Data Science",
            "instructor": "AI Tutor",
            "emoji": "🐍",
            "rating": 4.9,
            "duration": "5 weeks",
            "level": "Intermediate",
            "students": 3201,
            "enrolled": False,
        },
        {
            "title": "Web Development Fundamentals",
            "instructor": "AI Tutor",
            "emoji": "🌐",
            "rating": 4.7,
            "duration": "4 weeks",
            "level": "Beginner",
            "students": 4102,
            "enrolled": False,
        },
        {
            "title": "Cloud Computing Essentials",
            "instructor": "AI Tutor",
            "emoji": "☁️",
            "rating": 4.8,
            "duration": "6 weeks",
            "level": "Intermediate",
            "students": 1567,
            "enrolled": False,
        },
        {
            "title": "Advanced Python Programming",
            "instructor": "AI Tutor",
            "emoji": "🐍",
            "rating": 4.6,
            "duration": "7 weeks",
            "level": "Advanced",
            "students": 1203,
            "enrolled": False,
        },
        {
            "title": "Deep Learning & Neural Networks",
            "instructor": "AI Tutor",
            "emoji": "🧠",
            "rating": 4.9,
            "duration": "8 weeks",
            "level": "Advanced",
            "students": 2104,
            "enrolled": False,
        },
        {
            "title": "Competitive Programming Bootcamp",
            "instructor": "AI Tutor",
            "emoji": "🏆",
            "rating": 4.5,
            "duration": "10 weeks",
            "level": "Expert",
            "students": 456,
            "enrolled": False,
        },
    ]
    
    # Display courses in grid
    cols = st.columns(3)
    
    for idx, course in enumerate(courses_data):
        with cols[idx % 3]:
            render_course_card(
                course_title=course["title"],
                instructor=course["instructor"],
                thumbnail_emoji=course["emoji"],
                rating=course["rating"],
                duration=course["duration"],
                level=course["level"],
                enrolled=course["enrolled"],
            )
            
            if course["enrolled"]:
                st.button(f"▶️ Continue", key=f"continue_{idx}", use_container_width=True)
            else:
                st.button(f"📖 View Course", key=f"view_{idx}", use_container_width=True)
    
    # ==================== PAGINATION ====================
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: #6c757d;'>Showing 1-9 of 248 courses</p>", unsafe_allow_html=True)
    
    pag_col1, pag_col2, pag_col3 = st.columns([1, 1, 1])
    with pag_col2:
        col_p1, col_p2, col_p3, col_p4, col_p5 = st.columns(5)
        with col_p1:
            st.button("⬅️", use_container_width=True)
        with col_p2:
            st.button("1", use_container_width=True)
        with col_p3:
            st.button("2", use_container_width=True)
        with col_p4:
            st.button("3", use_container_width=True)
        with col_p5:
            st.button("➡️", use_container_width=True)
