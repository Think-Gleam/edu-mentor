# Main App Router - Coursera-Inspired Premium Learning Platform
# Integration of all pages with sidebar navigation and professional design

import streamlit as st
from frontend.components.ui_components import apply_page_config, inject_custom_css
from frontend.pages.home import render_home_page
from frontend.pages.course_catalog import render_course_catalog
from frontend.pages.course_detail import render_course_detail
from frontend.pages.learning_experience import render_learning_experience, render_quiz_page
from typing import Dict, Any


# ==================== PAGE CONFIGURATION ====================
apply_page_config()


# ==================== SESSION STATE INITIALIZATION ====================
def initialize_session_state():
    """Initialize all required session state variables."""
    if "current_page" not in st.session_state:
        st.session_state.current_page = "home"
    
    if "current_user" not in st.session_state:
        st.session_state.current_user = None
    
    if "auth_token" not in st.session_state:
        st.session_state.auth_token = None
    
    if "user_profile" not in st.session_state:
        # Default mock profile
        st.session_state.user_profile = {
            "id": "user_123",
            "full_name": "Ahmed Ali",
            "email": "ahmed@example.com",
            "grade_level": "10th Grade",
            "age": 16,
            "learning_goals": "Master AI and Machine Learning",
            "learning_challenges": "Complex mathematics",
            "preferred_language": "English",
            "time_commitment": "5 hours/week",
        }


# ==================== SIDEBAR NAVIGATION ====================
def render_sidebar_navigation():
    """Render custom sidebar with modern navigation."""
    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; padding: 1.5rem 0; border-bottom: 1px solid #e9ecef;'>
            <h1 style='margin: 0; font-size: 1.5rem;'>🎓 EduMentor</h1>
            <p style='margin: 0.5rem 0 0 0; color: #6c757d; font-size: 0.875rem;'>Premium Learning Platform</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # User Profile Section
        user = st.session_state.user_profile
        st.markdown(f"""
        <div style='background: #f8f9fa; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1.5rem; text-align: center;'>
            <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>{user['full_name'][0].upper()}</div>
            <p style='margin: 0.5rem 0; font-weight: 600;'>{user['full_name']}</p>
            <p style='margin: 0; font-size: 0.75rem; color: #6c757d;'>{user['grade_level']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation Menu
        st.markdown("<h4>Navigation</h4>", unsafe_allow_html=True)
        
        nav_items = [
            ("🏠 Home", "home"),
            ("📚 Browse Courses", "catalog"),
            ("🎯 Continue Learning", "learning"),
            ("📊 My Progress", "progress"),
            ("⭐ Wishlist", "wishlist"),
        ]
        
        for label, page in nav_items:
            is_active = st.session_state.current_page == page
            button_style = (
                "background-color: #0056b3; color: white; border-radius: 0.5rem; "
                if is_active else ""
            )
            
            if st.button(label, use_container_width=True, key=f"nav_{page}"):
                st.session_state.current_page = page
                st.rerun()
        
        st.markdown("---")
        
        # Settings Section
        st.markdown("<h4>Account</h4>", unsafe_allow_html=True)
        
        if st.button("⚙️ Settings", use_container_width=True, key="nav_settings"):
            st.session_state.current_page = "settings"
            st.rerun()
        
        if st.button("🚪 Log Out", use_container_width=True, key="nav_logout"):
            st.session_state.current_page = "login"
            st.rerun()
        
        st.markdown("---")
        
        # Stats Footer
        st.markdown(f"""
        <div style='font-size: 0.75rem; color: #6c757d; margin-top: 2rem;'>
            <p style='margin: 0.25rem 0;'>📊 <strong>3</strong> courses in progress</p>
            <p style='margin: 0.25rem 0;'>✅ <strong>2</strong> courses completed</p>
            <p style='margin: 0.25rem 0;'>🔥 <strong>12</strong> day streak</p>
            <p style='margin: 0.25rem 0;'>⭐ <strong>450</strong> achievement points</p>
        </div>
        """, unsafe_allow_html=True)


# ==================== PAGE ROUTING ====================
def route_to_page():
    """Route to the appropriate page based on session state."""
    page = st.session_state.current_page
    user = st.session_state.user_profile
    
    if page == "home":
        render_home_page(user)
    
    elif page == "catalog":
        render_course_catalog(user)
    
    elif page == "course_detail":
        render_course_detail(user)
    
    elif page == "learning":
        render_learning_experience(user)
    
    elif page == "quiz":
        render_quiz_page(user)
    
    elif page == "progress":
        render_progress_page(user)
    
    elif page == "settings":
        render_settings_page(user)
    
    else:
        st.error(f"Page '{page}' not found")


# ==================== ADDITIONAL PAGES ====================
def render_progress_page(user_profile: Dict[str, Any]):
    """Render the progress tracking page."""
    from frontend.components.ui_components import render_navbar, render_breadcrumb
    
    render_navbar(user_profile.get("full_name", "Student"))
    render_breadcrumb(["Home", "My Progress"])
    
    st.markdown("""
    <h1 style='font-size: 2.25rem; font-weight: 700; margin: 2rem 0;'>
        Your Learning Progress 📊
    </h1>
    """, unsafe_allow_html=True)
    
    # Progress Overview
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Hours", "24.5 hrs", "+2.3 hrs this week")
    with col2:
        st.metric("Courses In Progress", "3", "+1 this week")
    with col3:
        st.metric("Completion Rate", "68%", "+5% improvement")
    with col4:
        st.metric("Achievement Points", "450", "+50 this week")
    
    st.markdown("---")
    
    # Course Progress Cards
    st.markdown("<h2 style='margin: 2rem 0;'>Course Progress Details</h2>", unsafe_allow_html=True)
    
    courses_progress = [
        {"title": "AI Fundamentals", "progress": 45, "hours": 6.5, "next": "Week 2 Quiz"},
        {"title": "Machine Learning Basics", "progress": 30, "hours": 8.2, "next": "Clustering Algorithms"},
        {"title": "Advanced Algorithms", "progress": 15, "hours": 9.8, "next": "Dynamic Programming"},
    ]
    
    for course in courses_progress:
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f"""
            <div class='card' style='padding: 1.5rem;'>
                <h4 style='margin: 0 0 0.5rem 0;'>{course['title']}</h4>
                <div class='progress-container' style='margin: 1rem 0;'>
                    <div class='progress-bar'>
                        <div class='progress-fill' style='width: {course['progress']}%;'></div>
                    </div>
                    <p style='font-size: 0.875rem; color: #6c757d; margin-top: 0.5rem;'>{course['progress']}% Complete</p>
                </div>
                <p style='margin: 0; font-size: 0.875rem; color: #6c757d;'>Next: {course['next']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class='card' style='padding: 1.5rem; text-align: center;'>
                <h4 style='margin: 0;'>{course['hours']} hrs</h4>
                <p style='margin: 0.5rem 0 0 0; font-size: 0.75rem; color: #6c757d;'>Time Spent</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.button("Continue →", key=f"continue_course_{course['title']}", use_container_width=True)


def render_settings_page(user_profile: Dict[str, Any]):
    """Render the settings page."""
    from frontend.components.ui_components import render_navbar, render_breadcrumb
    
    render_navbar(user_profile.get("full_name", "Student"))
    render_breadcrumb(["Home", "Settings"])
    
    st.markdown("""
    <h1 style='font-size: 2.25rem; font-weight: 700; margin: 2rem 0;'>
        Settings ⚙️
    </h1>
    """, unsafe_allow_html=True)
    
    with st.expander("👤 Profile Settings", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            full_name = st.text_input("Full Name", value=user_profile.get("full_name"))
        with col2:
            email = st.text_input("Email", value=user_profile.get("email"))
        
        grade = st.selectbox("Grade Level", ["10th", "11th", "12th", "University"], 
                             index=0)
        age = st.number_input("Age", min_value=10, max_value=100, 
                             value=user_profile.get("age", 16))
        
        if st.button("Save Profile Changes"):
            st.success("Profile updated successfully!")
    
    with st.expander("🎓 Learning Preferences"):
        language = st.selectbox("Preferred Language", 
                               ["English", "Urdu", "Pashto"],
                               index=0)
        difficulty = st.selectbox("Starting Difficulty", 
                                 ["Easy", "Medium", "Challenging"],
                                 index=1)
        hours_per_week = st.slider("Target Learning Hours/Week", 
                                   min_value=1, max_value=20, value=5)
        
        if st.button("Save Learning Preferences"):
            st.success("Learning preferences updated!")
    
    with st.expander("🔔 Notification Settings"):
        email_notifications = st.checkbox("Email Notifications", value=True)
        reminder_emails = st.checkbox("Weekly Reminder Emails", value=True)
        progress_emails = st.checkbox("Progress Reports", value=True)
        
        if st.button("Save Notification Settings"):
            st.success("Notification settings updated!")
    
    with st.expander("🔐 Security"):
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        if st.button("Change Password"):
            if new_password and new_password == confirm_password:
                st.success("Password changed successfully!")
            else:
                st.error("Passwords do not match")


# ==================== MAIN APP ====================
def main():
    """Main application entry point."""
    initialize_session_state()
    
    # Render sidebar navigation
    render_sidebar_navigation()
    
    # Route to appropriate page
    route_to_page()


if __name__ == "__main__":
    main()
