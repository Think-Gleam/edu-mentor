import streamlit as st
import google.generativeai as genai
import os

# --- PAGE SETUP ---
st.set_page_config(page_title="EduMentor MVP", page_icon="🎓", layout="wide")
st.title("🎓 EduMentor: Adaptive AI Tutor")
st.markdown("Your personal AI tutor for Science and Mathematics.")

# --- API CONFIGURATION ---
# We fetch the API key from your computer's hidden environment variables
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("🚨 API Key not found! Please set the GEMINI_API_KEY environment variable.")
    st.stop()

# Configure the Gemini Model
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

# --- SIDEBAR: ONBOARDING ---
st.sidebar.header("Student Profile")
grade = st.sidebar.selectbox("Select Grade", ["Grade 5", "Grade 8", "Grade 10"])
subject = st.sidebar.selectbox("Select Subject", ["Mathematics", "Physics", "Chemistry", "Biology"])
st.sidebar.markdown("---")
st.sidebar.success("Status: AI Tutor Online 🟢")

# --- MAIN APP: VIRTUAL TEACHER ---
st.subheader(f"Current Subject: {subject} ({grade})")

# User Input
user_query = st.text_input("What concept are you struggling with today?", placeholder="e.g., Explain Newton's Third Law")

if st.button("Explain Concept"):
    if user_query:
        with st.spinner("EduMentor is analyzing and creating an analogy..."):
            # Prompt Engineering based on your Hackathon document
            prompt = f"""
            You are EduMentor, a highly encouraging and adaptive AI teacher.
            The student is in {grade} and is studying {subject}. 
            Explain the following concept: '{user_query}'.
            Rules:
            1. Keep it simple and age-appropriate.
            2. Use a relatable real-world analogy.
            3. End by asking a quick, simple question to check their understanding.
            """
            
            try:
                response = model.generate_content(prompt)
                st.info("🤖 **EduMentor:**")
                st.write(response.text)
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please type a concept first!")