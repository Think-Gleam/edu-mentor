# EduMentor Authentication & Registration Redesign
## Modern, International User Experience (Coursera / Duolingo Style)

---

## 📋 Overview

The authentication system has been completely redesigned with two distinct user journeys:

### **For New Users:**
1. **Sign-Up Form** → Collect basic info + learning profile
2. **Post-Signup Onboarding** → Learning interests + city + referral source
3. **Dashboard** → Start learning

### **For Existing Users:**
1. **Login** → Enter email/password
2. **Dashboard** → Resume learning
3. **Edit Profile** → Optional profile updates

---

## 🔐 Authentication Flow

```
┌─────────────────────────────────────────────────────────────┐
│                        START                                │
└──────────┬──────────────────────────────────────────────────┘
           │
           ├─ Not Logged In ─────────────┐
           │                             │
           ├─ Logged In ──────────────┐  │
           │                          │  │
           │                    Show Auth Page
           │                    ├─ Login Tab (existing users)
           │                    └─ Sign Up Tab (new users)
           │                          │
           │                    ┌─────┴─────┐
           │                    │           │
           │              Login Success   Sign Up Success
           │                    │           │
           │                   [A]        Store signup_data
           │                              in session
           │                              │
           │                            [B]
           │                        show_signup_onboarding()
           │                              │
           │                        Collect interests +
           │                        city + referral
           │                              │
           │                            [C]
           │                    Save full profile
           │                              │
           └──────────────────────────────┴──────────────────┘
                                   │
                            Check onboarding_complete
                                   │
                ┌──────────────────┴──────────────────┐
                │                                     │
             False                                  True
                │                                     │
        show_signup_onboarding()               show_dashboard()
         (if not already done)
```

---

## 🔧 Key Components

### 1. **Login Form** (`show_auth_page()` - Login Tab)

**Features:**
- ✅ Wrapped in `st.form()` to fix browser auto-fill issues
- ✅ Email & password fields with placeholders
- ✅ Form submission with validation
- ✅ Fetches user profile from Supabase
- ✅ Checks `onboarding_complete` flag
- ✅ Routes to dashboard or onboarding

**Error Handling:**
- Catches invalid credentials
- Shows clear error messages
- Guides users to sign-up if needed

### 2. **Sign-Up Form** (`show_auth_page()` - Sign Up Tab)

**Step 1: Basic Information** (2-column layout)
- Full Name * (Required)
- Date of Birth (Optional)
- Email Address * (Required)
- Create Password * (Required, 8+ chars)
- Confirm Password * (Required, must match)

**Step 2: Learning Profile** (2-column layout)
- I am a... * (Radio buttons)
  - 👶 Kid / Primary Student (Age 6–11)
  - 📚 Middle School Student (Age 12–14)
  - 🎓 High School Student (Age 15–18)
  - 🏫 University / College Student
  - 💼 Working Professional / Adult Learner
  - 👨‍👩‍👧 Parent / Guardian (for a child)
  
- Preferred Language * (Dropdown)
  - English
  - Urdu
  - Bilingual (English + Urdu)
  
- Current Education Level * (Dropdown)
  - Primary (Grades 1–5)
  - Middle (Grades 6–8)
  - Secondary / Matric (Grades 9–10)
  - Intermediate / FSc (Grades 11–12)
  - Undergraduate / Bachelor
  - Postgraduate / Master+
  - Other / Not Sure

**Validations:**
- Full name: 2+ characters required
- Email: Valid email format required
- Password: 8+ characters required
- Passwords must match
- Terms & conditions must be accepted

**On Success:**
- Creates Supabase auth account
- Stores signup data in `st.session_state.signup_data`
- Routes to `signup_onboarding` page

### 3. **Post-Signup Onboarding** (`show_signup_onboarding()`)

**Purpose:** Collect learning preferences immediately after sign-up to enable personalization

**Fields:**
- **Learning Interests** * (Multi-select) - Required
  - 🤖 AI Fundamentals
  - 📐 Mathematics
  - 🔬 Science
  - 📖 English Language
  - 💻 Programming
  - 📝 Exam Preparation
  - 🧠 General Knowledge
  - 🗣️ Communication Skills
  - 💼 Career Guidance

- **Your City** (Optional, 2-column layout)
  - Helps show relevant local resources

- **How Did You Hear About EduMentor?** (Optional, 2-column layout)
  - 📱 Social Media (Facebook/Instagram/TikTok)
  - 👥 Friend or Family Recommendation
  - 🔍 Google Search
  - 📺 YouTube / Online Ad
  - 🏫 School or Institution
  - 📰 News Article
  - 💬 Other

**On Success:**
- Combines signup_data + onboarding data into profile_data
- Sets `onboarding_complete = True`
- Saves to Supabase `profiles` table via UPSERT
- Routes to dashboard
- Clears signup_data from session

### 4. **Edit Profile** (`show_onboarding()`)

**Purpose:** Allow existing users to update their profile information

**Sections:**

**Basic Information**
- Full Name * (Required)
- Date of Birth (Optional)

**Education & Preferences** (2-column)
- Education Level * (Dropdown)
- Age (Number input)
- Preferred Language * (Dropdown)
- Your City (Text input, optional)

**Learning Profile**
- Learning Interests * (Multi-select) - Required
- Learning Challenges (Text area, optional)
- Academic Board (Dropdown, optional)
  - Federal Board
  - Punjab Board
  - Sindh Board
  - KPK Board
  - Balochistan Board
  - AJK Board
  - Not Applicable

**On Success:**
- Updates Supabase profile via UPSERT
- Routes to dashboard
- Shows success message

---

## 💾 Database Schema

### `profiles` Table Structure

```sql
CREATE TABLE profiles (
    id UUID PRIMARY KEY,  -- Matches Supabase auth.users.id
    
    -- Basic Information
    full_name TEXT,
    email TEXT,
    date_of_birth DATE,
    
    -- Learning Profile
    student_type TEXT,  -- From radio buttons
    preferred_language TEXT,  -- English, Urdu, Bilingual
    education_level TEXT,  -- Primary, Middle, Secondary, etc.
    age INT,
    
    -- Learning Interests
    learning_interests TEXT[],  -- Array of selected interests
    learning_challenges TEXT,
    academic_board TEXT,
    
    -- Metadata
    city TEXT,
    how_heard TEXT,
    onboarding_complete BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);
```

### UPSERT Operation
- Uses Supabase `.upsert()` to create or update profiles
- Prevents duplicate key errors
- Seamlessly handles both new and existing users

---

## 🎨 Design Principles

### **Clean & Professional**
- Clear headings and sections
- Consistent spacing (8pt baseline)
- Professional color scheme (Coursera blue #0056b3)
- Proper typography hierarchy

### **International & Inclusive**
- Support for multiple languages (English, Urdu, Bilingual)
- Pakistan-specific options (provinces, boards)
- Student type radio buttons (kids, students, professionals, parents)
- City field for localization

### **Mobile-First Responsive**
- 2-column layout on desktop
- Stacks to single column on mobile
- Touch-friendly button sizes
- Readable font sizes

### **User-Friendly**
- Clear required field indicators (*)
- Helpful placeholder text
- Descriptive help text on hover
- Progressive disclosure (basic info → learning profile)
- Terms & conditions agreement
- Success/error messages

---

## 🔄 Session State Management

### **Key Session Variables**

```python
st.session_state.logged_in
# Boolean: True if user is authenticated

st.session_state.user_id
# String (UUID): Unique user identifier from Supabase auth

st.session_state.user_profile
# Dict: User profile data from Supabase profiles table
# Contains: full_name, email, age, education_level, learning_interests, etc.

st.session_state.current_page
# String: Current page to render
# Values: "signup", "signup_onboarding", "onboarding", "dashboard", "course_ui"

st.session_state.signup_data
# Dict: Temporary storage for signup form data
# Used to populate onboarding page after successful sign-up
# Cleared after profile creation
```

---

## 🚀 User Journeys

### **Journey 1: New User Sign-Up**

```
1. User sees "Sign Up" tab
2. Fills basic info (name, email, password) + learning profile (type, language, level)
3. Clicks "Create My Account"
4. Validations pass → Supabase auth account created
5. Redirects to signup_onboarding page
6. Fills learning interests + city + referral source
7. Clicks "Complete My Profile"
8. Full profile saved to Supabase
9. Redirects to dashboard
10. Sees "Welcome to EduMentor" with personalized content
```

### **Journey 2: Existing User Login**

```
1. User sees "Log In" tab
2. Enters email and password
3. Clicks "Log In"
4. Supabase validates credentials
5. Fetches profile from database
6. Checks onboarding_complete flag
7. If True → Routes to dashboard
8. If False → Routes to onboarding (shouldn't happen for existing users)
9. Dashboard shows personalized content
```

### **Journey 3: Profile Edit**

```
1. User on dashboard clicks "⚙️ Edit Profile"
2. Routes to onboarding page with pre-filled data
3. Updates any fields
4. Clicks "Save Changes"
5. Profile updated in Supabase
6. Redirects to dashboard
7. Shows success message
```

---

## ✅ Validation Rules

| Field | Rule | Error Message |
|-------|------|---------------|
| Full Name | 2+ characters | "Please enter your full name (at least 2 characters)." |
| Email | Valid format | "Please enter a valid email address." |
| Password | 8+ characters | "Password must be at least 8 characters long." |
| Confirm Password | Matches password | "Passwords do not match. Please try again." |
| Learning Interests | At least 1 selected | "Please select at least one learning interest." |
| Terms & Conditions | Must be checked | "You must accept the Terms of Service to continue." |

---

## 🔒 Security Best Practices

✅ **Passwords:**
- Minimum 8 characters enforced
- Stored in Supabase auth (hashed)
- Confirm password field to prevent typos

✅ **Session Management:**
- User ID stored in `st.session_state`
- Profile data cached to reduce DB queries
- Logout clears all sensitive data

✅ **Database:**
- UPSERT prevents duplicate rows
- Profile id matches Supabase auth.users.id
- Timestamps track creation/updates

✅ **Email Verification:**
- Supabase auth handles verification links
- Can be enabled in Supabase settings

---

## 🧪 Testing Checklist

### **Sign-Up Flow**
- [ ] Can submit sign-up form
- [ ] Validations work (empty fields, short password, email format)
- [ ] Password confirmation validation works
- [ ] Terms & conditions checkbox required
- [ ] Supabase auth account created
- [ ] Redirects to signup_onboarding

### **Onboarding Flow**
- [ ] Learning interests multi-select works
- [ ] At least 1 interest required
- [ ] City field optional
- [ ] How heard field optional
- [ ] Profile saved to Supabase
- [ ] Redirects to dashboard

### **Login Flow**
- [ ] Can submit login form
- [ ] Invalid credentials show error
- [ ] Valid credentials fetch profile
- [ ] Routes to dashboard (if onboarding_complete = true)
- [ ] Routes to onboarding (if onboarding_complete = false)

### **Edit Profile**
- [ ] Form pre-fills with existing data
- [ ] Can update all fields
- [ ] Validations work
- [ ] Updates in Supabase
- [ ] Redirects to dashboard

### **Mobile Responsive**
- [ ] 2-column layout on desktop
- [ ] Single column on mobile
- [ ] Buttons full-width and tappable
- [ ] Text readable on mobile
- [ ] No horizontal scroll

---

## 🎯 Future Enhancements

- [ ] Email verification on sign-up
- [ ] Forgot password flow
- [ ] Social login (Google, Facebook)
- [ ] Two-factor authentication (2FA)
- [ ] Profile picture upload
- [ ] Email notifications settings
- [ ] Account deletion
- [ ] Data export (GDPR)

---

## 📝 Code Comments Reference

Key functions in `lms_app.py`:

### `show_auth_page()`
- Modern login & sign-up interface
- Uses `st.form()` to fix auto-fill
- Validates all inputs
- FIX 1: Form wrapper for auto-fill
- FIX 2: Explicit boolean check for onboarding_complete

### `show_signup_onboarding()`
- Collects post-signup personalization
- 2-column responsive layout
- Multi-select learning interests
- Combines data and saves to Supabase
- Routes to dashboard on success

### `show_onboarding()`
- Edit profile page for existing users
- Pre-fills with existing data
- Full validation
- UPSERT updates to database
- Routes back to dashboard

### Master Router
- Routes based on `logged_in` and `current_page`
- Handles auth flow
- Manages page transitions
- Fallback to dashboard if route invalid

---

## 📊 Metrics & Analytics

Track these to measure registration success:

1. **Sign-up Completion Rate** - % of users completing sign-up
2. **Onboarding Completion Rate** - % completing post-signup onboarding
3. **Profile Completeness** - % of fields filled
4. **Login Success Rate** - % of login attempts succeeding
5. **Dropout Points** - Where users abandon forms
6. **Mobile vs Desktop** - Conversion rates by device

---

## 🆘 Troubleshooting

### **Issue: "Already registered" error on sign-up**
**Cause:** Email already exists in Supabase auth
**Solution:** Use different email or show login tab

### **Issue: Profile not saving**
**Cause:** Supabase connection issue or missing SUPABASE_URL/KEY
**Solution:** Check .env file and Supabase connection

### **Issue: User stuck on onboarding after login**
**Cause:** `onboarding_complete` field is false/null
**Solution:** Check database - may need to manually update flag

### **Issue: Session state lost after redirect**
**Cause:** Supabase fetch failed
**Solution:** Check internet connection and Supabase status

---

## 📚 Related Files

- `lms_app.py` - Main authentication implementation
- `.env` - Supabase configuration (SUPABASE_URL, SUPABASE_KEY)
- Supabase dashboard - Manage auth and database
- app_v2.py - Modern UI routing (separate system)

---

## ✨ Conclusion

The new registration system provides:
- ✅ **Modern UX** - Clean, professional design
- ✅ **International** - Multiple languages, Pakistan-specific options
- ✅ **Mobile-Friendly** - Responsive 2-column layout
- ✅ **Secure** - Password validation, email verification
- ✅ **Personalized** - Collects learning preferences
- ✅ **Scalable** - Supabase backend, easy to extend

Users can now sign up, get personalized, and start learning in minutes!
