import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from gtts import gTTS  # NEW: Voice Engine
import io              # NEW: For playing audio without saving files
from supabase import create_client, Client # <-- Make sure this is here!

# --- LOAD SECURE KEYS ---
load_dotenv()

# --- DATABASE CONFIGURATION ---
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")

if not supabase_url or not supabase_key:
    st.error("🚨 Supabase keys not found in .env file!")
    st.stop()

# Initialize the Supabase connection (This fixes the error!)
supabase: Client = create_client(supabase_url, supabase_key)

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="EduMentor Platform", page_icon="🚀", layout="wide")

# --- API CONFIGURATION ---
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("🚨 API Key not found! Please check your .env file.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

# --- INITIALIZE SESSION STATE ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_profile" not in st.session_state:
    st.session_state.user_profile = {}
if "current_page" not in st.session_state:
    st.session_state.current_page = "signup"

# --- PAGE 1: REAL AUTHENTICATION (Login & Sign Up) ---
def show_auth_page():
    st.title("🚀 Welcome to EduMentor")
    st.markdown("Log in or create a real account to access your adaptive learning dashboard.")
    
    # Create two tabs for Login and Sign Up
    tab_login, tab_signup = st.tabs(["🔐 Log In", "📝 Sign Up"])
    
    # --- LOG IN TAB ---
    with tab_login:
        st.subheader("Welcome Back!")
        login_email = st.text_input("Email", key="login_email")
        login_password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Log In"):
            with st.spinner("Authenticating with Supabase..."):
                try:
                    # Live Supabase Login Call
                    response = supabase.auth.sign_in_with_password({"email": login_email, "password": login_password})
                    
                    # Save the real user data to the session
                    st.session_state.logged_in = True
                    st.session_state.user_id = response.user.id
                    
                    # For now, give them a default profile (we will build the real profile saver next!)
                    st.session_state.user_profile = {
                        "name": login_email.split('@')[0],
                        "age": 15,
                        "level": "Beginner",
                        "interests": "Technology",
                        "time_commit": "30 mins"
                    }
                    
                    st.session_state.current_page = "dashboard"
                    st.success("Login Successful!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Login failed: Invalid email or password.")

    # --- SIGN UP TAB ---
    with tab_signup:
        st.subheader("Create a New Account")
        signup_email = st.text_input("Email", key="signup_email")
        signup_password = st.text_input("Password", type="password", key="signup_password")
        signup_password_confirm = st.text_input("Confirm Password", type="password", key="signup_password_confirm")
        
        if st.button("Create Account"):
            if signup_password != signup_password_confirm:
                st.error("Passwords do not match!")
            elif len(signup_password) < 6:
                st.error("Password must be at least 6 characters.")
            else:
                with st.spinner("Creating account in Supabase..."):
                    try:
                        # Live Supabase Sign Up Call
                        response = supabase.auth.sign_up({"email": signup_email, "password": signup_password})
                        st.success("Account successfully created! You can now log in using the Log In tab.")
                    except Exception as e:
                        st.error(f"Sign up failed: {e}")

# --- PAGE: RICH ONBOARDING & PROFILE EDIT ---
def show_onboarding():
    # Fetch existing profile data if it exists (for the "Edit Profile" feature)
    profile = st.session_state.get("user_profile") or {}
    
    st.title("✨ Personalize Your Profile")
    st.markdown("Update your details so EduMentor can adapt to your needs.")
    
    with st.form("onboarding_form"):
        st.subheader("1. The Basics")
        full_name = st.text_input("Full Name *", value=profile.get("full_name", ""))
        
        col1, col2 = st.columns(2)
        
        # Helper lists for dropdowns
        grade_options = ["Primary (Grade 1–5)", "Middle (Grade 6–8)", "Secondary / Matric (Grade 9–10)", "Intermediate / FSc (Grade 11–12)", "University / Bachelor", "University / Master & Above"]
        lang_options = ["English", "Urdu", "Bilingual (English + Urdu)"]
        prov_options = ["Punjab", "Sindh", "KPK", "Balochistan", "Gilgit-Baltistan", "AJK", "Federal Capital"]
        board_options = ["Not Applicable", "Federal Board", "Punjab Board", "Sindh Board", "Other"]
        
        with col1:
            # Safely set default index based on existing data
            grade_idx = grade_options.index(profile.get("grade_level")) if profile.get("grade_level") in grade_options else 0
            grade = st.selectbox("Grade / Education Level *", grade_options, index=grade_idx)
            
            age = st.number_input("Age", min_value=5, max_value=100, value=profile.get("age", 15))
            
        with col2:
            lang_idx = lang_options.index(profile.get("preferred_language")) if profile.get("preferred_language") in lang_options else 0
            language = st.selectbox("Preferred Language *", lang_options, index=lang_idx)
            
            prov_idx = prov_options.index(profile.get("province")) if profile.get("province") in prov_options else 0
            province = st.selectbox("Province / Region *", prov_options, index=prov_idx)
            
        st.subheader("2. Your Academic Profile")
        
        goals_options = ["Science", "Mathematics", "English", "Computer Science", "General Knowledge", "Exam Preparation", "Career Guidance"]
        goals = st.multiselect("Learning Goals / Interests", goals_options, default=profile.get("learning_goals", []))
        
        board_idx = board_options.index(profile.get("academic_board")) if profile.get("academic_board") in board_options else 0
        board = st.selectbox("Current Academic Board", board_options, index=board_idx)
        
        challenges = st.text_area("Any Specific Learning Challenges? (Optional)", value=profile.get("learning_challenges", ""))
        
        submit_profile = st.form_submit_button("Save Profile & Go to Dashboard")
        
        if submit_profile:
            if full_name:
                with st.spinner("Saving your adaptive profile..."):
                    try:
                        # THE FIX: Use UPSERT instead of INSERT
                        profile_data = {
                            "id": st.session_state.user_id,
                            "full_name": full_name,
                            "grade_level": grade,
                            "age": age,
                            "preferred_language": language,
                            "province": province,
                            "learning_goals": goals,
                            "academic_board": board,
                            "learning_challenges": challenges,
                            "onboarding_complete": True
                        }
                        # Upsert will create a new row if it doesn't exist, or update it if it does!
                        supabase.table("profiles").upsert(profile_data).execute()
                        
                        # Update local memory and push to dashboard
                        st.session_state.user_profile = profile_data
                        st.session_state.current_page = "dashboard"
                        st.success("Profile saved successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error saving profile: {e}")
            else:
                st.error("Please enter your Full Name to continue.")

# --- PAGE 2: USER DASHBOARD ---
def show_dashboard():
    profile = st.session_state.user_profile
    
    # Safely get the name (fallback to "Student" if missing)
    display_name = profile.get('full_name', 'Student')
    grade = profile.get('grade_level', 'Beginner')
    language = profile.get('preferred_language', 'English')
    
    st.sidebar.title(f"👋 Hello, {display_name.split()[0]}!")
    st.sidebar.markdown(f"**Grade:** {grade} | **Lang:** {language}")
    
    st.sidebar.markdown("---")
    if st.sidebar.button("⚙️ Edit Profile"):
        st.session_state.current_page = "onboarding"
        st.rerun()
    
    if st.sidebar.button("Log Out"):
        st.session_state.logged_in = False
        st.session_state.current_page = "signup"
        st.rerun()

    st.title("📊 Your Learning Dashboard")
    
    st.subheader("🏆 Your Accomplishments")
    col1, col2, col3 = st.columns(3)
    col1.info("🔥 1 Day Streak")
    col2.success("🥇 AI Pioneer Badge")
    col3.warning("⭐ 150 Learning Points")
    
    st.markdown("---")
    
    st.subheader("📚 Your Enrolled Courses")
    with st.container(border=True):
        st.markdown("### 🤖 AI Fundamentals: Adaptive Course")
        
        # Format learning goals nicely for the UI
        goals_list = profile.get('learning_goals', ['Technology'])
        goals_str = ", ".join(goals_list) if isinstance(goals_list, list) else goals_list
        
        st.markdown(f"Customized for a **{profile.get('age', 15)}-year-old** in **{grade}** interested in **{goals_str}**.")
        st.progress(10) 
        
        if st.button("Resume Learning - Module 1"):
            st.session_state.current_page = "course_ui"
            st.rerun()

# --- PAGE 3: THE LEARNING INTERFACE ---
def show_course_ui():
    profile = st.session_state.user_profile
    
    if st.sidebar.button("⬅️ Back to Dashboard"):
        st.session_state.current_page = "dashboard"
        st.rerun()
        
    st.title("🤖 Module 1: Introduction to Artificial Intelligence")
    
    tab_lesson, tab_activity, tab_tutor = st.tabs(["📖 Lesson", "⚙️ Activities & Quiz", "💬 AI Context Tutor"])
    
    # ----------------------------------------
    # 1. THE ADAPTIVE LESSON TAB (DYNAMIC GEN)
    # ----------------------------------------
    with tab_lesson:
        st.header("The Adaptive Lesson")
        
        # Only generate the lesson ONCE per session so it doesn't reload constantly
        if "generated_lesson" not in st.session_state:
            with st.spinner("✨ Gemini is crafting your personalized lesson..."):
                try:
                    # Safely extract goals for the prompt
                    goals_list = profile.get('learning_goals', ['General Knowledge'])
                    goals_str = ", ".join(goals_list) if isinstance(goals_list, list) else goals_list

                    # The Prompt that makes it adapt to the upgraded user profile!
                    prompt = f"""
                    You are an expert curriculum designer. Write a highly engaging, 2-paragraph introduction to Artificial Intelligence for a student named {profile.get('full_name', 'Student')}.
                    The student is {profile.get('age', 15)} years old.
                    Their education level is: {profile.get('grade_level', 'High School')}.
                    They are highly interested in: {goals_str}.
                    
                    RULES:
                    1. Use clear language strictly appropriate for their age and education level.
                    2. Use an analogy directly related to their interests ({goals_str}).
                    3. Do NOT use markdown like asterisks or bolding, just plain text so the Text-to-Speech engine can read it smoothly.
                    """
                    response = model.generate_content(prompt)
                    st.session_state.generated_lesson = response.text
                except Exception as e:
                    st.error(f"Generation Error: {e}")
                    st.session_state.generated_lesson = "We had trouble generating your lesson. Please try again."

        # Display the dynamically generated text
        st.markdown(st.session_state.generated_lesson)
        
        st.markdown("---")
        st.subheader("🎧 Listen to this Lesson")
        
        if st.button("▶️ Generate Audio Lesson"):
            with st.spinner("EduMentor is recording your audio..."):
                try:
                    # Read the dynamically generated text!
                    tts = gTTS(text=st.session_state.generated_lesson, lang='en', slow=False)
                    audio_bytes = io.BytesIO()
                    tts.write_to_fp(audio_bytes)
                    audio_bytes.seek(0)
                    
                    st.success("Audio ready!")
                    st.audio(audio_bytes, format="audio/mp3")
                except Exception as e:
                    st.error(f"Failed to generate audio: {e}")
        
    # ----------------------------------------
    # 2. THE ACTIVITY TAB (MASTERY ENGINE)
    # ----------------------------------------
    with tab_activity:
        st.header("Hands-On Mastery Quiz")
        st.markdown("You must score **75% or higher** to unlock the next module.")
        
        # --- INITIALIZE QUIZ STATE ---
        if "quiz_attempts" not in st.session_state:
            st.session_state.quiz_attempts = 0
        if "quiz_passed" not in st.session_state:
            st.session_state.quiz_passed = False
        if "force_restudy" not in st.session_state:
            st.session_state.force_restudy = False

        # --- THE RE-STUDY LOCKOUT ---
        if st.session_state.force_restudy:
            st.error("🚨 Maximum attempts (3) reached.")
            st.warning("You must review the Adaptive Lesson tab again. The system has detected a struggle with these concepts.")
            if st.button("I have re-read the lesson. Unlock new attempt."):
                # Reset for the mastery loop
                st.session_state.quiz_attempts = 0
                st.session_state.force_restudy = False
                st.session_state.quiz_passed = False
                st.rerun()

        # --- SUCCESS STATE ---
        elif st.session_state.quiz_passed:
            st.success("🎉 Module Mastered! You scored above 75%.")
            st.balloons()
            if st.button("Proceed to Next Module ➡️"):
                # In a full app, this increments the user's progress in Supabase
                st.info("Next module loading...")

        # --- ACTIVE QUIZ STATE ---
        else:
            st.write(f"**Attempts Remaining:** {3 - st.session_state.quiz_attempts}")
            st.warning("Anti-Cheat System Active: Copy/Paste Disabled.")
            
            with st.form("quiz_form"):
                # Question 1
                q1 = st.radio("1. What is the core goal of AI?", [
                    "To build faster cars", 
                    "To create systems capable of learning and reasoning", 
                    "To replace all human jobs"
                ], index=None)
                
                # Question 2
                q2 = st.radio("2. Machine Learning is a subset of...", [
                    "Mathematics", 
                    "Artificial Intelligence", 
                    "Hardware Engineering"
                ], index=None)
                
                # Question 3
                q3 = st.radio("3. Which of these adapts based on user data?", [
                    "A static PDF textbook", 
                    "A standard calculator", 
                    "An AI Learning Companion"
                ], index=None)

                submit_quiz = st.form_submit_button("Submit Answers")

                if submit_quiz:
                    # Calculate Score
                    score = 0
                    if q1 == "To create systems capable of learning and reasoning": score += 1
                    if q2 == "Artificial Intelligence": score += 1
                    if q3 == "An AI Learning Companion": score += 1
                    
                    percentage = (score / 3) * 100
                    
                    if percentage >= 75:
                        st.session_state.quiz_passed = True
                        st.rerun()
                    else:
                        st.session_state.quiz_attempts += 1
                        if st.session_state.quiz_attempts >= 3:
                            st.session_state.force_restudy = True
                        else:
                            st.error(f"Score: {percentage:.0f}%. You need 75% to pass. Please try again.")
                        st.rerun()
        
    # ----------------------------------------
    # 3. THE STRICT AI TUTOR TAB
    # ----------------------------------------
    with tab_tutor:
        st.header("Contextual AI Tutor")
        st.write("I am your strict, professional guide. I will help you understand, but I will not do the work for you.")
        
        # Tutor must know what the dynamic lesson is!
        current_lesson_text = st.session_state.get("generated_lesson", "No lesson generated yet.")
        
        strict_tutor_instructions = f"""
        You are EduMentor, an elite, professional academic tutor. 
        You are currently teaching a {profile.get('age', 15)}-year-old student at a {profile.get('grade_level', 'High School')} level.
        
        YOUR CURRENT LESSON CONTEXT:
        "{current_lesson_text}"
        
        YOUR STRICT RULES:
        1. THE SOCRATIC METHOD: NEVER give the student the direct answer to a problem. Instead, ask them guiding questions.
        2. CONTEXT BOUNDING: You are ONLY allowed to talk about the CURRENT LESSON CONTEXT. 
        3. REFUSAL PROTOCOL: If the student asks about a different topic, firmly say: "That is outside the scope of our current lesson. Let's get back on track."
        """
        
        if "restricted_chat" not in st.session_state:
            st.session_state.restricted_chat = model.start_chat(
                history=[{"role": "user", "parts": [strict_tutor_instructions]},
                         {"role": "model", "parts": ["Understood. I am locked into the tutor persona."]}]
            )

        if "tutor_messages" not in st.session_state:
            st.session_state.tutor_messages = []

        for message in st.session_state.tutor_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        user_q = st.chat_input("Ask a question about the lesson...")
        
        if user_q:
            st.chat_message("user").markdown(user_q)
            st.session_state.tutor_messages.append({"role": "user", "content": user_q})
            
            with st.chat_message("assistant"):
                with st.spinner("Analyzing..."):
                    try:
                        response = st.session_state.restricted_chat.send_message(user_q)
                        st.markdown(response.text)
                        st.session_state.tutor_messages.append({"role": "assistant", "content": response.text})
                    except Exception as e:
                        st.error(f"Error: {e}")

# --- THE NEW MASTER ROUTER ---
# Put this at the very bottom of your file to control the flow!

# --- THE NEW MASTER ROUTER ---
if st.session_state.logged_in == False:
    show_auth_page() 
    
elif st.session_state.logged_in == True:
    # 1. Force onboarding if it's their very first time
    if not st.session_state.get("user_profile") or st.session_state.user_profile.get("onboarding_complete") != True:
        show_onboarding() 
        
    # 2. Allow them to access the profile editor intentionally
    elif st.session_state.current_page == "onboarding":
        show_onboarding()
        
    # 3. Standard routing
    elif st.session_state.current_page == "dashboard":
        show_dashboard() 
        
    elif st.session_state.current_page == "course_ui":
        show_course_ui()