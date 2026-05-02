import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# --- LOAD SECURE KEYS ---
load_dotenv()

# --- PAGE SETUP ---
st.set_page_config(page_title="EduMentor v3.0", page_icon="🎓", layout="wide")
st.title("🎓 EduMentor: Adaptive AI Tutor")
st.markdown("Your personal AI tutor. Ask questions, get analogies, and test your knowledge.")

# --- API CONFIGURATION ---
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("🚨 API Key not found! Please check your .env file.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

# --- SIDEBAR & ONBOARDING ---
st.sidebar.header("Student Profile")
grade = st.sidebar.selectbox("Select Grade", ["Grade 5", "Grade 8", "Grade 10"])
subject = st.sidebar.selectbox("Select Subject", ["Mathematics", "Physics", "Chemistry", "Biology"])

system_instructions = f"""
You are EduMentor, an encouraging and brilliant AI teacher. 
The student is in {grade} studying {subject}. 
Always explain concepts simply, use relatable real-world analogies, and occasionally ask quick questions to check their understanding.
Keep your responses relatively brief.
"""

st.sidebar.markdown("---")
st.sidebar.success("Status: Chat Engine Online 🟢")

# NEW v3.0 FEATURE: The Quiz Generator
st.sidebar.markdown("### Test Your Knowledge")
generate_quiz = st.sidebar.button("📝 Generate Pop Quiz")

# --- INITIALIZE CHAT MEMORY ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "gemini_chat" not in st.session_state:
    st.session_state.gemini_chat = model.start_chat(
        history=[
            {"role": "user", "parts": [system_instructions]},
            {"role": "model", "parts": ["Understood. I am ready to teach!"]}
        ]
    )

# --- DISPLAY CHAT HISTORY ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- QUIZ LOGIC (v3.0) ---
if generate_quiz:
    if len(st.session_state.messages) == 0:
        st.sidebar.warning("We haven't learned anything yet! Ask a question first.")
    else:
        quiz_prompt = "Based ONLY on the concepts we have discussed in this conversation, generate a fun 3-question multiple-choice pop quiz. Put the correct answers at the very bottom."
        
        # Display user action in UI
        st.chat_message("user").markdown("📝 *Student requested a pop quiz...*")
        st.session_state.messages.append({"role": "user", "content": "📝 *Student requested a pop quiz...*"})
        
        with st.chat_message("assistant"):
            with st.spinner("Crafting your quiz..."):
                try:
                    response = st.session_state.gemini_chat.send_message(quiz_prompt)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"An error occurred: {e}")

# --- CHAT INPUT ---
if prompt := st.chat_input("What concept are you struggling with today?"):
    
    # Add user message to UI
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get response from Gemini
    with st.chat_message("assistant"):
        with st.spinner("EduMentor is thinking..."):
            try:
                response = st.session_state.gemini_chat.send_message(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"An error occurred: {e}")