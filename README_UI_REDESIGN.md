# EduMentor - Coursera-Inspired UI Redesign
## Premium Modern Learning Platform

### 📋 Overview

This document describes the complete UI redesign of EduMentor to match premium platforms like Coursera. The redesign features:

- ✨ **Professional Design System** - Color variables, spacing, typography, shadows
- 🎯 **Responsive Layout** - Mobile-first design with desktop optimization  
- 📱 **Component Library** - 17+ reusable UI components
- 🎨 **Consistent Styling** - CSS variable-based design tokens
- 🧭 **Modern Navigation** - Sidebar + navbar + page routing
- 📚 **Learning Experience** - Premium 3-column lesson layout
- 🔄 **Integration Ready** - Connects with multi-agent backend (crew.py)

---

## 🏗️ Architecture

### Folder Structure
```
EduMentor/
├── app_v2.py                          # Main app router (entry point)
├── frontend/
│   ├── __init__.py
│   ├── components/
│   │   ├── __init__.py
│   │   └── ui_components.py          # 17 reusable component functions
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── home.py                   # Dashboard/homepage
│   │   ├── course_catalog.py         # Course discovery & search
│   │   ├── course_detail.py          # Course information page
│   │   └── learning_experience.py    # In-course lesson + quiz player
│   └── styles/
│       ├── __init__.py
│       └── coursera_style.css        # Complete CSS design system
└── [existing multi-agent backend files]
```

---

## 🎨 Design System

### Color Palette

| Variable | Value | Usage |
|----------|-------|-------|
| `--primary-blue` | `#0056b3` | Main brand color, buttons, links |
| `--primary-blue-light` | `#e7f1ff` | Background highlights, badges |
| `--secondary-blue` | `#17a2b8` | Accents, gradients |
| `--success` | `#28a745` | Success messages, checkmarks |
| `--warning` | `#ffc107` | Ratings, warnings |
| `--danger` | `#dc3545` | Errors, removals |
| `--gray-50` to `--gray-900` | Grey scale | Text, borders, backgrounds |

### Typography

- **Font Family**: System fonts (-apple-system, Segoe UI, Roboto, etc.)
- **Font Sizes**: 
  - Body: `1rem` (16px)
  - Small: `0.875rem` (14px)
  - Large: `1.125rem` (18px)
  - Headings: 1.25rem - 2.25rem

### Spacing (8pt baseline)
- `--spacing-xs`: 0.25rem (2px)
- `--spacing-sm`: 0.5rem (4px)
- `--spacing-md`: 1rem (8px)
- `--spacing-lg`: 1.5rem (12px)
- `--spacing-xl`: 2rem (16px)
- `--spacing-2xl`: 3rem (24px)

### Shadows & Effects
- `--shadow-sm`: Subtle shadows for cards
- `--shadow-md`: Standard card shadow
- `--shadow-lg`: Elevated state (hover)
- `--shadow-xl`: Maximum elevation

---

## 🧩 Component Library (ui_components.py)

### 17 Reusable Components

#### Navigation
1. **`inject_custom_css()`** - Load CSS stylesheet
2. **`apply_page_config()`** - Set page title, icon, layout
3. **`render_navbar(user_name, show_search)`** - Top navigation bar
4. **`render_sidebar(user_profile, current_page)`** - Fixed left sidebar

#### Cards & Containers
5. **`render_course_card()`** - Course display card with thumbnail
6. **`render_hero_section()`** - Large banner with title & CTA
7. **`render_progress_card()`** - Progress tracking card
8. **`render_course_header()`** - Course detail header info

#### Course Content
9. **`render_curriculum_section()`** - Expandable course weeks/lessons
10. **`render_learning_outcomes()`** - Learning objectives list
11. **`render_lesson_player()`** - Video player + transcript area
12. **`render_module_sidebar()`** - Course module navigation
13. **`render_quiz_interface()`** - Quiz question renderer

#### Progress & Analytics
14. **`render_progress_sidebar()`** - Progress tracking with streaks
15. **`render_breadcrumb()`** - Breadcrumb navigation
16. **`render_badge()`** - Status badges
17. **`render_empty_state()`** - Empty state placeholder

#### Layout Utilities
- **`render_breadcrumb()`** - Navigation path display
- **`render_badge()`** - Status and category badges
- **`render_empty_state()`** - No content state display

---

## 📄 Pages (frontend/pages/)

### 1. Home Page (home.py)
**Route**: `home`
**Purpose**: Dashboard showing user progress and recommended courses

**Sections**:
- Welcome hero section
- Quick stats cards (in progress, completed, streak, points)
- Active courses grid (3-column)
- Recommended courses (based on interests)
- Course categories
- Footer stats (hours, certificates, streak, points)

**Key Features**:
- Personalized greeting with user name
- Progress overview at a glance
- Quick access to in-progress courses
- Recommended content discovery
- Achievement tracking

### 2. Course Catalog (course_catalog.py)
**Route**: `catalog`
**Purpose**: Discover and browse all available courses

**Sections**:
- Hero title with description
- Search bar
- Filter controls:
  - Level (Beginner/Intermediate/Advanced/Expert)
  - Duration (< 2 weeks, 2-4 weeks, 4-8 weeks, > 8 weeks)
  - Category (AI & ML, Programming, Data Science, Web Dev, Cloud)
  - Sort (Popular, Newest, Highest Rated, Most Students)
- Course grid (3-column responsive)
- Pagination controls

**Key Features**:
- Real-time search filtering
- Multi-select filters
- Course rating and enrollment indicators
- Student counts and duration info
- Continue/Explore buttons

### 3. Course Detail (course_detail.py)
**Route**: `course_detail`
**Purpose**: Detailed course information and enrollment

**Sections**:
- Hero banner with course title & emoji
- Course metadata (rating, students, duration, level)
- About course description
- Learning outcomes list
- Expandable curriculum (by week)
- Requirements section
- Right sidebar:
  - Enrollment card
  - Free price badge
  - Instructor info
- Student reviews section

**Key Features**:
- Comprehensive course information
- Curriculum overview
- Clear enrollment CTA
- Social proof (reviews, student count)
- Sticky enrollment card
- Instructor credibility

### 4. Learning Experience (learning_experience.py)
**Route**: `learning`
**Purpose**: In-course lesson and quiz player

**Layout**: 3-Column responsive
```
[Modules] [Lesson Content] [Progress Sidebar]
```

**Left Column**:
- Course content list
- Module navigation
- Completion tracking (✓ for done, ▷ for current)
- Duration info

**Main Column**:
- Lesson title
- Video player placeholder (emoji + description)
- Lesson transcript/content
- Markdown-formatted text
- Navigation buttons (Previous/Next)

**Right Column**:
- Progress percentage
- Modules completed counter
- Learning streak indicator (🔥)
- Note-taking section
- AI Tutor chat interface

**Quiz Page**:
- Quiz header with passing requirement (75%)
- Question grid (multiple choice + short answer)
- Answer submission
- Score display
- Next module button

**Key Features**:
- Immersive learning layout
- Multiple question types
- Progress tracking in real-time
- AI tutor assistance
- Note-taking capability
- Responsive on all devices

---

## 🚀 Usage Guide

### Running the Application

```bash
# Install dependencies
pip install streamlit streamlit-option-menu

# Run the main app
streamlit run app_v2.py
```

### Navigation

1. **Home Page** - Default landing page
   - See dashboard, progress, recommendations

2. **Browse Courses** - Search & discover
   - Use filters to find courses
   - Click "View Course" to see details

3. **Course Detail** - Learn about course
   - Read full description
   - Review curriculum
   - Click "Enroll" to start

4. **Learning Experience** - Study materials
   - Watch lessons
   - Take quizzes
   - Track progress

5. **Settings** - User preferences
   - Edit profile
   - Set learning preferences
   - Configure notifications

### Sidebar Navigation

The left sidebar provides persistent navigation with:
- Quick links to all pages
- User profile summary
- Learning statistics
- Account management

---

## 🔧 Integration Points

### With Multi-Agent System (crew.py)

The learning experience page is designed to integrate with your AI backend:

```python
# In learning_experience.py
from crew.crew import EduMentorCrew

# Generate lesson content
crew = EduMentorCrew()
lesson = crew.run_quick_lesson(
    user_id=user_profile['id'],
    topic="History of AI"
)

# Render the generated lesson
render_lesson_player(
    lesson_title=lesson['title'],
    lesson_content=lesson['explanation']
)

# Generate adaptive quiz
quiz_data = crew.run_quiz_only(
    user_id=user_profile['id'],
    topic="History of AI",
    difficulty=user_difficulty_level
)
```

### Database Integration (supabase_client.py)

```python
# Save quiz results
db.save_quiz_result(
    user_id=user_id,
    topic="AI Fundamentals",
    score=quiz_score,
    answers=user_answers,
    time_spent_seconds=time_spent
)

# Track progress
db.update_progress(
    user_id=user_id,
    topic="AI Fundamentals",
    mastery_level=calculated_mastery,
    attempts=attempt_count
)
```

---

## 🎨 Customization

### Changing Colors

Edit CSS variables in `coursera_style.css`:

```css
:root {
    --primary-blue: #0056b3;  /* Change to any color */
    --secondary-blue: #17a2b8;
    /* ... other colors ... */
}
```

### Adjusting Spacing

Modify spacing variables:

```css
--spacing-md: 1rem;   /* Change from 1rem to 0.75rem */
--spacing-lg: 1.5rem; /* Adjust all spacing */
```

### Adding New Components

1. Create function in `ui_components.py`:
```python
def render_custom_component(title, content):
    st.markdown(f"""
    <div class='card'>
        <h3>{title}</h3>
        <p>{content}</p>
    </div>
    """, unsafe_allow_html=True)
```

2. Import and use in page:
```python
from frontend.components.ui_components import render_custom_component
render_custom_component("Title", "Content")
```

---

## 📱 Responsive Design

### Breakpoints

| Screen | Width | Layout |
|--------|-------|--------|
| Mobile | < 768px | Single column |
| Tablet | 768px - 1024px | 2-column (reduced sidebar) |
| Desktop | > 1024px | Full 3-column layout |

### Mobile Optimizations

- Sidebar collapses to hamburger menu
- Navigation moves to bottom or top
- Font sizes scale down appropriately
- Cards stack vertically
- Learning layout becomes single column

---

## 🧪 Testing Checklist

- [ ] Home page loads correctly
- [ ] Course catalog search works
- [ ] Filters update course grid
- [ ] Course detail shows all sections
- [ ] Quiz questions render properly
- [ ] Progress bar updates correctly
- [ ] Sidebar navigation works on mobile
- [ ] Navigation persists across pages
- [ ] Buttons have proper hover effects
- [ ] Forms validate input
- [ ] Styles load correctly
- [ ] No console errors

---

## 📊 Performance Tips

1. **Lazy load course images** - Use emoji placeholders instead of real images
2. **Cache component rendering** - Use Streamlit caching for expensive functions
3. **Optimize CSS** - CSS is loaded once on page load
4. **Minimize state updates** - Group updates to reduce reruns

---

## 🔮 Future Enhancements

- [ ] Dark mode toggle
- [ ] Real-time collaboration on notes
- [ ] Video streaming integration
- [ ] Certificate generation and sharing
- [ ] Social features (discussion forums)
- [ ] Advanced analytics dashboard
- [ ] Mobile native app
- [ ] Offline learning support

---

## 📚 File Reference

| File | Lines | Purpose |
|------|-------|---------|
| `app_v2.py` | ~280 | Main router & entry point |
| `ui_components.py` | ~520 | Component library |
| `coursera_style.css` | ~600+ | CSS design system |
| `home.py` | ~140 | Dashboard page |
| `course_catalog.py` | ~120 | Course discovery |
| `course_detail.py` | ~180 | Course info page |
| `learning_experience.py` | ~200 | Learning player |

---

## 🤝 Contributing

When adding new features:

1. **Use existing components** - Don't duplicate HTML/CSS
2. **Follow naming conventions** - Use `render_*` for components
3. **Update CSS variables** - Don't hardcode colors/spacing
4. **Test responsiveness** - Ensure mobile compatibility
5. **Document changes** - Update this README

---

## 📞 Support

For issues or questions:
1. Check existing components for similar patterns
2. Review CSS variables before custom styling
3. Test on multiple screen sizes
4. Consult integration docs for backend features

---

## 📄 License

Part of the EduMentor project. All rights reserved.
