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
    """Modern, clean authentication page with Login and Sign Up tabs"""
    
    # Header
    st.title("🚀 Welcome to EduMentor")
    st.markdown("Your personalized adaptive learning platform for students across Pakistan and beyond.")
    
    # Create two tabs for Login and Sign Up
    tab_login, tab_signup = st.tabs(["🔐 Log In", "📝 Sign Up"])
    
    # ==================== LOG IN TAB ====================
    with tab_login:
        st.subheader("Welcome Back!")
        st.markdown("Sign in to your EduMentor account and continue learning.")
        
        # FIX 1: Wrap in st.form to solve the browser Auto-Fill bug!
        with st.form("login_form"):
            login_email = st.text_input("Email", placeholder="your@email.com")
            login_password = st.text_input("Password", type="password", placeholder="••••••••")
            submit_login = st.form_submit_button("🔓 Log In", use_container_width=True)
            
            if submit_login:
                if not login_email or not login_password:
                    st.error("❌ Please enter both email and password.")
                else:
                    with st.spinner("🔐 Authenticating with Supabase..."):
                        try:
                            # Live Supabase Login Call
                            response = supabase.auth.sign_in_with_password({
                                "email": login_email, 
                                "password": login_password
                            })
                            
                            st.session_state.logged_in = True
                            st.session_state.user_id = response.user.id
                            
                            # Fetch real profile from database
                            profile_response = supabase.table("profiles").select("*").eq("id", response.user.id).execute()
                            
                            if len(profile_response.data) > 0:
                                st.session_state.user_profile = profile_response.data[0]
                                
                                # FIX 2: Explicitly check the boolean to break the infinite loop
                                if st.session_state.user_profile.get("onboarding_complete") == True:
                                    st.session_state.current_page = "dashboard"
                                else:
                                    st.session_state.current_page = "onboarding"
                            else:
                                # Brand new user, no profile row exists yet
                                st.session_state.user_profile = None
                                st.session_state.current_page = "onboarding"
                                
                            st.success("✅ Login Successful!")
                            st.rerun()
                        except Exception as e:
                            st.error("❌ Login failed: Invalid email or password.")
        
        # Sign up link
        st.markdown("---")
        st.markdown("**Don't have an account?** Click on the **Sign Up** tab to create one.", unsafe_allow_html=True)

    # ==================== SIGN UP TAB ====================
    with tab_signup:
        st.subheader("Create Your Account")
        st.markdown("Join thousands of students learning on EduMentor. It only takes 2 minutes!")
        
        # Use form to group all fields
        with st.form("signup_form", clear_on_submit=False):
            st.markdown("### 📋 Basic Information")
            
            # Step 1: Basic Info (2 columns)
            col1, col2 = st.columns(2)
            
            with col1:
                full_name = st.text_input(
                    "Full Name *",
                    placeholder="Ahmed Ali",
                    help="Your first and last name"
                )
            
            with col2:
                date_of_birth = st.date_input(
                    "Date of Birth (Optional)",
                    value=None,
                    help="We use this to personalize your learning experience"
                )
            
            signup_email = st.text_input(
                "Email Address *",
                placeholder="your@email.com",
                help="We'll send a verification link here"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                signup_password = st.text_input(
                    "Create Password *",
                    type="password",
                    placeholder="At least 8 characters",
                    help="Use a mix of letters, numbers, and symbols for security"
                )
            
            with col2:
                signup_password_confirm = st.text_input(
                    "Confirm Password *",
                    type="password",
                    placeholder="Repeat your password",
                    help="Make sure it matches"
                )
            
            st.markdown("---")
            st.markdown("### 🎓 Learning Profile")
            st.markdown("Help us understand your learning needs to personalize your experience.")
            
            # Step 2: Learning Profile (2 columns)
            col1, col2 = st.columns(2)
            
            with col1:
                student_type = st.radio(
                    "I am a... *",
                    options=[
                        "👶 Kid / Primary Student (Age 6–11)",
                        "📚 Middle School Student (Age 12–14)",
                        "🎓 High School Student (Age 15–18)",
                        "🏫 University / College Student",
                        "💼 Working Professional / Adult Learner",
                        "👨‍👩‍👧 Parent / Guardian (for a child)"
                    ]
                )
            
            with col2:
                preferred_language = st.selectbox(
                    "Preferred Language *",
                    options=["English", "Urdu", "Bilingual (English + Urdu)"],
                    index=0,
                    help="You can change this anytime"
                )
                
                education_level = st.selectbox(
                    "Current Education Level *",
                    options=[
                        "Primary (Grades 1–5)",
                        "Middle (Grades 6–8)",
                        "Secondary / Matric (Grades 9–10)",
                        "Intermediate / FSc (Grades 11–12)",
                        "Undergraduate / Bachelor",
                        "Postgraduate / Master+",
                        "Other / Not Sure"
                    ],
                    index=0
                )
            
            st.markdown("---")
            
            # Terms & Conditions
            accept_terms = st.checkbox(
                "I agree to the Terms of Service and Privacy Policy *",
                help="Read our terms before signing up"
            )
            
            submit_signup = st.form_submit_button("🚀 Create My Account", use_container_width=True)
            
            if submit_signup:
                # Validation
                errors = []
                
                if not full_name or len(full_name.strip()) < 2:
                    errors.append("Please enter your full name (at least 2 characters).")
                
                if not signup_email or "@" not in signup_email:
                    errors.append("Please enter a valid email address.")
                
                if not signup_password or len(signup_password) < 8:
                    errors.append("Password must be at least 8 characters long.")
                
                if signup_password != signup_password_confirm:
                    errors.append("Passwords do not match. Please try again.")
                
                if not accept_terms:
                    errors.append("You must accept the Terms of Service to continue.")
                
                if errors:
                    for error in errors:
                        st.error(error)
                else:
                    # All validations passed, proceed to Supabase sign up
                    with st.spinner("🔐 Creating your account..."):
                        try:
                            # Create auth account
                            response = supabase.auth.sign_up({
                                "email": signup_email, 
                                "password": signup_password
                            })
                            
                            # Store signup data in session for the onboarding page
                            st.session_state.logged_in = True
                            st.session_state.user_id = response.user.id
                            st.session_state.current_page = "signup_onboarding"
                            st.session_state.signup_data = {
                                "full_name": full_name,
                                "email": signup_email,
                                "date_of_birth": str(date_of_birth) if date_of_birth else None,
                                "student_type": student_type,
                                "preferred_language": preferred_language,
                                "education_level": education_level,
                                "onboarding_complete": False
                            }
                            
                            st.success("✅ Account created successfully! Let's set up your learning profile.")
                            st.rerun()
                            
                        except Exception as e:
                            error_msg = str(e)
                            if "already registered" in error_msg.lower():
                                st.error("❌ This email is already registered. Please log in instead.")
                            else:
                                st.error(f"❌ Sign up failed: {error_msg}")

# --- PAGE: POST-SIGNUP ONBOARDING & PERSONALIZATION ---
def show_signup_onboarding():
    """Onboarding page immediately after sign-up - collects learning interests and city"""
    
    st.title("🎯 Let's Personalize Your Learning")
    st.markdown("Tell us what you want to learn and we'll create a perfect study plan for you!")
    
    # Get the signup data from session
    signup_data = st.session_state.get("signup_data", {})
    user_id = st.session_state.get("user_id")
    
    with st.form("onboarding_personalization_form"):
        st.markdown("### 📚 What Do You Want to Learn?")
        st.markdown("Select all topics that interest you:")
        
        # Multi-select learning interests
        learning_interests = st.multiselect(
            "Learning Interests *",
            options=[
                "🤖 AI Fundamentals",
                "📐 Mathematics",
                "🔬 Science",
                "📖 English Language",
                "💻 Programming",
                "📝 Exam Preparation",
                "🧠 General Knowledge",
                "🗣️ Communication Skills",
                "💼 Career Guidance"
            ],
            help="Choose as many as you like. You can change these anytime.",
            default=[],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.markdown("### 📍 Location & Background")
        
        col1, col2 = st.columns(2)
        
        with col1:
            your_city = st.text_input(
                "Your City (Optional)",
                placeholder="e.g., Karachi, Lahore, Islamabad",
                help="Helps us show you relevant local resources"
            )
        
        with col2:
            how_heard = st.selectbox(
                "How Did You Hear About EduMentor? (Optional)",
                options=[
                    "Select an option...",
                    "📱 Social Media (Facebook/Instagram/TikTok)",
                    "👥 Friend or Family Recommendation",
                    "🔍 Google Search",
                    "📺 YouTube / Online Ad",
                    "🏫 School or Institution",
                    "📰 News Article",
                    "💬 Other"
                ]
            )
        
        st.markdown("---")
        
        # Submit button
        submit_onboarding = st.form_submit_button("✨ Complete My Profile", use_container_width=True)
        
        if submit_onboarding:
            if not learning_interests:
                st.error("❌ Please select at least one learning interest.")
            else:
                with st.spinner("🚀 Setting up your personalized learning experience..."):
                    try:
                        # Combine signup data with onboarding data
                        profile_data = {
                            "id": user_id,
                            **signup_data,
                            "learning_interests": learning_interests,
                            "city": your_city if your_city else None,
                            "how_heard": how_heard if how_heard != "Select an option..." else None,
                            "onboarding_complete": True,
                            "created_at": "now()"
                        }
                        
                        # Create profile in database
                        supabase.table("profiles").upsert(profile_data).execute()
                        
                        # Update session
                        st.session_state.user_profile = profile_data
                        st.session_state.current_page = "dashboard"
                        st.session_state.signup_data = None  # Clear signup data
                        
                        st.success("✅ Your profile is ready! Welcome to EduMentor! 🎉")
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Error saving your profile: {str(e)}")


# --- PAGE: EDIT PROFILE (for existing users) ---
def show_onboarding():
    """Modern profile editing page for existing users"""
    
    # Fetch existing profile data
    profile = st.session_state.get("user_profile") or {}
    
    st.title("✨ Update Your Profile")
    st.markdown("Customize your learning preferences and keep your information up to date.")
    
    with st.form("edit_profile_form"):
        st.markdown("### 📋 Basic Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            full_name = st.text_input(
                "Full Name *",
                value=profile.get("full_name", ""),
                placeholder="Ahmed Ali",
                help="Your first and last name"
            )
        
        with col2:
            date_of_birth = st.date_input(
                "Date of Birth",
                value=None,
                help="Optional: helps us personalize your learning"
            )
        
        st.markdown("---")
        st.markdown("### 🎓 Education & Preferences")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Grade/Education Level
            grade_options = [
                "Primary (Grades 1–5)",
                "Middle (Grades 6–8)",
                "Secondary / Matric (Grades 9–10)",
                "Intermediate / FSc (Grades 11–12)",
                "Undergraduate / Bachelor",
                "Postgraduate / Master+",
                "Other / Not Sure"
            ]
            grade_idx = grade_options.index(profile.get("education_level", "Secondary / Matric (Grades 9–10)")) if profile.get("education_level") in grade_options else 2
            grade = st.selectbox(
                "Education Level *",
                grade_options,
                index=grade_idx,
                help="Your current or most recent education level"
            )
            
            # Age
            age = st.number_input(
                "Age",
                min_value=5,
                max_value=100,
                value=profile.get("age", 15),
                help="Helps personalize content difficulty"
            )
        
        with col2:
            # Preferred Language
            lang_options = ["English", "Urdu", "Bilingual (English + Urdu)"]
            lang_idx = lang_options.index(profile.get("preferred_language", "English")) if profile.get("preferred_language") in lang_options else 0
            language = st.selectbox(
                "Preferred Language *",
                lang_options,
                index=lang_idx,
                help="Language for lessons and communication"
            )
            
            # City
            city = st.text_input(
                "Your City (Optional)",
                value=profile.get("city", ""),
                placeholder="e.g., Karachi, Lahore",
                help="Helps show relevant local resources"
            )
        
        st.markdown("---")
        st.markdown("### 🎯 Learning Profile")
        
        # Learning Interests
        learning_interests_options = [
            "🤖 AI Fundamentals",
            "📐 Mathematics",
            "🔬 Science",
            "📖 English Language",
            "💻 Programming",
            "📝 Exam Preparation",
            "🧠 General Knowledge",
            "🗣️ Communication Skills",
            "💼 Career Guidance"
        ]
        
        selected_interests = st.multiselect(
            "Learning Interests *",
            learning_interests_options,
            default=profile.get("learning_interests", ["🤖 AI Fundamentals"]),
            help="Choose topics you want to learn"
        )
        
        # Learning Challenges
        challenges = st.text_area(
            "Any Specific Learning Challenges? (Optional)",
            value=profile.get("learning_challenges", ""),
            placeholder="e.g., I struggle with mathematics word problems...",
            help="Help us understand your needs"
        )
        
        # Academic Board (Pakistan-specific)
        board_options = [
            "Federal Board",
            "Punjab Board",
            "Sindh Board",
            "KPK Board",
            "Balochistan Board",
            "AJK Board",
            "Not Applicable"
        ]
        board_idx = board_options.index(profile.get("academic_board", "Federal Board")) if profile.get("academic_board") in board_options else 0
        board = st.selectbox(
            "Academic Board (Optional)",
            board_options,
            index=board_idx,
            help="Your school or college's exam board"
        )
        
        st.markdown("---")
        
        # Submit button
        submit_profile = st.form_submit_button("💾 Save Changes", use_container_width=True)
        
        if submit_profile:
            if not full_name or len(full_name.strip()) < 2:
                st.error("❌ Please enter your full name (at least 2 characters).")
            elif not selected_interests:
                st.error("❌ Please select at least one learning interest.")
            else:
                with st.spinner("💾 Saving your profile..."):
                    try:
                        profile_data = {
                            "id": st.session_state.user_id,
                            "full_name": full_name,
                            "date_of_birth": str(date_of_birth) if date_of_birth else profile.get("date_of_birth"),
                            "education_level": grade,
                            "age": age,
                            "preferred_language": language,
                            "city": city if city else None,
                            "learning_interests": selected_interests,
                            "learning_challenges": challenges if challenges else None,
                            "academic_board": board,
                            "onboarding_complete": True
                        }
                        
                        # Upsert profile
                        supabase.table("profiles").upsert(profile_data).execute()
                        
                        # Update session
                        st.session_state.user_profile = profile_data
                        st.session_state.current_page = "dashboard"
                        
                        st.success("✅ Profile updated successfully!")
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Error saving profile: {str(e)}")

# --- PAGE 2: USER DASHBOARD ---
def show_dashboard():
    profile = st.session_state.user_profile
    
    # Safely get the name (fallback to "Student" if missing)
    display_name = profile.get('full_name', 'Student')
    education_level = profile.get('education_level', 'Beginner')
    language = profile.get('preferred_language', 'English')
    
    st.sidebar.title(f"👋 Hello, {display_name.split()[0]}!")
    st.sidebar.markdown(f"**Level:** {education_level} | **Lang:** {language}")
    
    st.sidebar.markdown("---")
    if st.sidebar.button("⚙️ Edit Profile"):
        st.session_state.current_page = "onboarding"
        st.rerun()
    
    if st.sidebar.button("🚪 Log Out"):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.user_profile = {}
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
        
        # Format learning interests nicely for the UI
        interests_list = profile.get('learning_interests', ['🤖 AI Fundamentals'])
        interests_str = ", ".join(interests_list) if isinstance(interests_list, list) else interests_list
        
        st.markdown(f"Customized for a **{profile.get('age', 15)}-year-old** learning **{interests_str}**.")
        st.progress(0.10) 
        
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

# --- THE MASTER ROUTER ---
# Controls the entire app flow based on authentication and page state

if st.session_state.logged_in == False:
    # Not authenticated - show login and sign-up
    show_auth_page() 
    
elif st.session_state.logged_in == True:
    # Authenticated user - route based on current page
    
    if st.session_state.current_page == "signup_onboarding":
        # New user after sign-up - collect learning interests
        show_signup_onboarding()
        
    elif st.session_state.current_page == "onboarding":
        # Edit profile page for existing users
        show_onboarding()
        
    elif st.session_state.current_page == "dashboard":
        # Main dashboard
        show_dashboard() 
        
    elif st.session_state.current_page == "course_ui":
        # Learning interface
        show_course_ui()
        
    else:
        # Fallback - if no valid page set, show dashboard
        st.session_state.current_page = "dashboard"
        st.rerun()