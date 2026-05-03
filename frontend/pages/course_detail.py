# Course Detail Page - Like Coursera

import streamlit as st
from frontend.components.ui_components import (
    render_navbar,
    render_breadcrumb,
    render_course_header,
    render_curriculum_section,
    render_learning_outcomes,
)
from typing import Dict, Any


def render_course_detail(user_profile: Dict[str, Any], course_id: str = "ai-fundamentals"):
    """Render detailed course page."""
    
    # Header
    render_navbar(user_profile.get("full_name", "Student"))
    render_breadcrumb(["Home", "Courses", "AI Fundamentals"])
    
    # ==================== COURSE HERO ====================
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #0056b3 0%, #17a2b8 100%); 
                color: white; padding: 3rem; border-radius: 0.5rem; 
                margin-bottom: 2rem; text-align: center;'>
        <div style='font-size: 5rem; margin-bottom: 1rem;'>🤖</div>
        <h1 style='color: white; margin: 0 0 1rem 0;'>AI Fundamentals: Adaptive Course</h1>
        <p style='font-size: 1.125rem; opacity: 0.9; margin: 0;'>
            Master the core concepts of Artificial Intelligence from scratch
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Course Header with Key Info
    render_course_header(
        course_title="AI Fundamentals: Adaptive Course",
        instructor="EduMentor AI Tutor",
        rating=4.8,
        students=2543,
        duration="4 weeks",
        level="Beginner"
    )
    
    # ==================== MAIN CONTENT ====================
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # About Section
        st.markdown("""
        <h2 style='margin: 2rem 0 1rem 0;'>About This Course</h2>
        """, unsafe_allow_html=True)
        
        st.write("""
        Artificial Intelligence is transforming every industry. In this adaptive course, 
        you'll learn the fundamental concepts that power AI systems used by millions worldwide.
        
        **What makes this course special:**
        - 🎯 Adaptive difficulty that adjusts to YOUR level
        - 📊 Real-world examples tailored to your interests
        - 🗣️ Interactive lessons with AI tutor guidance
        - 🧪 Practice quizzes with instant feedback
        - 📈 Track your progress with detailed analytics
        """)
        
        # Learning Outcomes
        st.markdown("<h3 style='margin: 2rem 0 1rem 0;'>What You'll Learn</h3>", unsafe_allow_html=True)
        outcomes = [
            "Understand the core concepts of AI, machine learning, and neural networks",
            "Apply AI techniques to solve real-world problems",
            "Build and train simple AI models",
            "Understand ethical implications of AI",
            "Prepare for advanced AI courses",
        ]
        render_learning_outcomes(outcomes)
        
        # Curriculum
        st.markdown("<h3 style='margin: 2rem 0 1rem 0;'>Course Curriculum</h3>", unsafe_allow_html=True)
        
        weeks_data = [
            {
                "title": "AI Fundamentals & History",
                "duration_minutes": 180,
                "lessons": [
                    {"title": "What is AI?", "duration_minutes": 15},
                    {"title": "History of AI", "duration_minutes": 20},
                    {"title": "AI in the Real World", "duration_minutes": 25},
                    {"title": "Quiz: AI Basics", "duration_minutes": 10},
                ]
            },
            {
                "title": "Machine Learning Introduction",
                "duration_minutes": 240,
                "lessons": [
                    {"title": "What is Machine Learning?", "duration_minutes": 20},
                    {"title": "Supervised vs Unsupervised Learning", "duration_minutes": 30},
                    {"title": "Classification & Regression", "duration_minutes": 30},
                    {"title": "Practice: Build Your First Model", "duration_minutes": 40},
                ]
            },
            {
                "title": "Deep Learning Basics",
                "duration_minutes": 300,
                "lessons": [
                    {"title": "Neural Networks Explained", "duration_minutes": 40},
                    {"title": "Forward & Backward Propagation", "duration_minutes": 50},
                    {"title": "Activation Functions", "duration_minutes": 30},
                    {"title": "Project: Image Classification", "duration_minutes": 60},
                ]
            },
            {
                "title": "AI Ethics & Final Project",
                "duration_minutes": 200,
                "lessons": [
                    {"title": "Ethical AI & Bias", "duration_minutes": 30},
                    {"title": "AI Safety & Transparency", "duration_minutes": 25},
                    {"title": "Capstone Project", "duration_minutes": 120},
                ]
            },
        ]
        
        render_curriculum_section(weeks_data)
        
        # Requirements
        st.markdown("<h3 style='margin: 2rem 0 1rem 0;'>Course Requirements</h3>", unsafe_allow_html=True)
        st.write("""
        - No prior AI/ML experience required
        - Basic math knowledge (algebra, statistics)
        - Computer with internet connection
        - 5-10 hours per week commitment
        """)
    
    with col2:
        # Enrollment Card
        st.markdown("""
        <div class='card' style='position: sticky; top: 80px; padding: 2rem;'>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <h3 style='margin: 0 0 1.5rem 0;'>Ready to Learn?</h3>
        """, unsafe_allow_html=True)
        
        # Price
        st.markdown("""
        <div style='background: #f8f9fa; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1.5rem;'>
            <p style='margin: 0; color: #6c757d; font-size: 0.875rem;'>COURSE PRICE</p>
            <h2 style='margin: 0.5rem 0 0 0;'>FREE</h2>
            <p style='margin: 0.5rem 0 0 0; font-size: 0.875rem; color: #28a745;'>✓ Lifetime access</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Enrollment Stats
        st.markdown(f"""
        <div style='margin-bottom: 1.5rem;'>
            <p style='margin: 0 0 0.5rem 0;'>
                <strong>⭐ 4.8</strong> <span style='color: #6c757d;'>(2,543 reviews)</span>
            </p>
            <p style='margin: 0;'>
                <strong>👥 24,587</strong> <span style='color: #6c757d;'>students enrolled</span>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Enroll Button
        if st.button("🚀 Enroll Now - Free", use_container_width=True):
            st.success("Welcome! You've successfully enrolled. Starting course...")
            st.session_state.current_page = "learning"
        
        # Or continue if already enrolled
        st.button("▶️ Continue Learning", use_container_width=True)
        
        # Wishlist
        if st.button("❤️ Add to Wishlist", use_container_width=True):
            st.info("Added to your wishlist!")
        
        st.markdown("---")
        
        # Instructor Info
        st.markdown("""
        <div style='margin-top: 1.5rem;'>
            <h4 style='margin-bottom: 1rem;'>About the Instructor</h4>
            <div style='display: flex; gap: 1rem; margin-bottom: 1rem;'>
                <div style='font-size: 2.5rem;'>🤖</div>
                <div>
                    <p style='margin: 0; font-weight: 600;'>EduMentor AI Tutor</p>
                    <p style='margin: 0.5rem 0 0 0; font-size: 0.875rem; color: #6c757d;'>
                        Advanced AI system trained on thousands of educational materials
                    </p>
                </div>
            </div>
            <p style='margin: 0; font-size: 0.875rem;'>
                ⭐ 4.8 average rating<br/>
                👥 47,203 students taught<br/>
                📚 12 courses published
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # ==================== REVIEWS SECTION ====================
    st.markdown("---")
    st.markdown("<h2 style='margin: 2rem 0 1.5rem 0;'>Student Reviews</h2>", unsafe_allow_html=True)
    
    reviews = [
        {
            "name": "Ahmed Ali",
            "rating": 5,
            "text": "Excellent course! The adaptive difficulty really helped me learn at my own pace. Highly recommended!",
            "verified": True,
        },
        {
            "name": "Fatima Khan",
            "rating": 5,
            "text": "The AI tutor is amazing. Very patient and explains concepts clearly. This changed my understanding of AI!",
            "verified": True,
        },
        {
            "name": "Hassan Malik",
            "rating": 4,
            "text": "Great content, but wish there were more hands-on projects. Overall very good course.",
            "verified": True,
        },
    ]
    
    for review in reviews:
        st.markdown(f"""
        <div class='card' style='padding: 1.5rem; margin-bottom: 1rem;'>
            <div style='display: flex; justify-content: space-between; margin-bottom: 0.5rem;'>
                <strong>{review['name']}</strong>
                <span style='color: #ffc107;'>{'⭐' * review['rating']}</span>
            </div>
            <p style='margin: 0.5rem 0 0 0; color: #6c757d;'>{review['text']}</p>
            <p style='margin: 0.5rem 0 0 0; font-size: 0.75rem; color: #17a2b8;'>
                {"✓ Verified Student" if review['verified'] else ""}
            </p>
        </div>
        """, unsafe_allow_html=True)
