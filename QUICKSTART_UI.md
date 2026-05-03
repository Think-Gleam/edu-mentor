# Quick Start - EduMentor Premium UI

## 🚀 Get Started in 3 Steps

### 1. Install Dependencies
```bash
pip install streamlit
```

### 2. Run the Application
```bash
streamlit run app_v2.py
```

### 3. Open in Browser
Navigate to `http://localhost:8501` (Streamlit will open automatically)

---

## 📱 What You'll See

### Home Page (Default)
- Welcome dashboard with personalized greeting
- Your learning progress at a glance
- Recommended courses based on interests
- Quick access to in-progress courses

### Navigation
Use the **left sidebar** to explore:
- 📚 **Browse Courses** - Discover new learning materials
- 🎯 **Continue Learning** - Resume where you left off
- 📊 **My Progress** - Track your achievements
- ⚙️ **Settings** - Customize your learning preferences

### Features to Explore

✨ **Course Discovery**
- Search for courses by name, topic, or instructor
- Filter by difficulty level, duration, and category
- Sort by popularity, newest, or highest rated

📖 **Lesson Player**
- 3-column layout (modules, lesson, progress)
- Interactive lesson content with transcripts
- AI Tutor chat for questions
- Note-taking functionality

📝 **Assessments**
- Adaptive quizzes matching your level
- Multiple choice and short-answer questions
- Instant scoring with feedback
- Progress tracking

---

## 🎯 Page Routes

| Page | Route | Purpose |
|------|-------|---------|
| Home | `home` | Dashboard & overview |
| Browse Courses | `catalog` | Course discovery |
| Course Details | `course_detail` | Full course information |
| Learn | `learning` | Lesson player & quiz |
| Progress | `progress` | Learning analytics |
| Settings | `settings` | User preferences |

---

## 🔧 Customization

### Change Primary Color

Edit `frontend/styles/coursera_style.css`:
```css
--primary-blue: #0056b3;  /* Change this to your brand color */
```

### Add Your Courses

Edit course data in page files:
```python
courses_data = [
    {
        "title": "Your Course Title",
        "instructor": "Instructor Name",
        "emoji": "📚",
        ...
    }
]
```

### Connect to Backend

See `README_UI_REDESIGN.md` for integration with:
- ✅ Multi-agent system (crew.py)
- ✅ Database (supabase_client.py)
- ✅ LLM fallbacks
- ✅ Voice services

---

## 📁 File Structure

```
EduMentor/
├── app_v2.py                    # Main entry point ← RUN THIS
├── frontend/
│   ├── components/
│   │   └── ui_components.py    # All 17 UI components
│   ├── pages/
│   │   ├── home.py              # Home/Dashboard
│   │   ├── course_catalog.py    # Course search
│   │   ├── course_detail.py     # Course info
│   │   └── learning_experience.py  # Lesson player
│   └── styles/
│       └── coursera_style.css   # All styling
└── README_UI_REDESIGN.md        # Full documentation
```

---

## 🎨 Design System

### Colors
- Primary Blue: `#0056b3` (Coursera blue)
- Success Green: `#28a745`
- Warning Yellow: `#ffc107`
- Neutral Grays: `#f8f9fa` - `#212529`

### Responsive Breakpoints
- 📱 Mobile: < 768px
- 📱 Tablet: 768px - 1024px
- 💻 Desktop: > 1024px

### Components (17 Total)
- Navigation (navbar, sidebar)
- Cards (course, progress, hero)
- Content (lesson player, quiz, curriculum)
- Utilities (badges, breadcrumbs, empty states)

---

## 🔗 Integration Ready

### Multi-Agent Backend
The UI connects seamlessly with your AI system:
- ✅ Planner Agent for personalized learning paths
- ✅ Teacher Agent for adaptive lessons
- ✅ Quiz Agent for intelligent assessments
- ✅ Evaluator Agent for progress tracking

### Coming Soon
- 🔜 Real-time LLM-generated lesson content
- 🔜 Adaptive difficulty based on quiz performance
- 🔜 Voice lesson narration (TTS)
- 🔜 Urdu/Pashto language support

---

## 💡 Tips & Tricks

### Development Tips
- Use `st.session_state` to persist data between reruns
- Components accept Markdown for rich formatting
- CSS classes available: `.card`, `.btn-primary`, `.progress-bar`
- All colors use CSS variables for easy theming

### Performance
- Course images use emoji placeholders (fast)
- CSS loaded once on page init
- Components are fully reactive
- No unnecessary API calls on page transitions

---

## ❓ Troubleshooting

**"Module not found" error?**
- Ensure you're running from the project root directory
- Check that all `__init__.py` files exist in frontend/ subdirectories

**Styles not loading?**
- Verify `coursera_style.css` exists at `frontend/styles/coursera_style.css`
- Check browser console for CSS errors
- Clear cache: `Ctrl+Shift+Delete` or `Cmd+Shift+Delete`

**Navigation not working?**
- Check that `st.session_state.current_page` is being set
- Verify `st.rerun()` is called after navigation
- Check browser console for JavaScript errors

---

## 📚 Learn More

- Full documentation: See `README_UI_REDESIGN.md`
- Component API: Check `frontend/components/ui_components.py`
- Page examples: Review individual page files in `frontend/pages/`
- CSS system: Explore `frontend/styles/coursera_style.css`

---

## 🎓 Welcome to Premium Learning!

Your EduMentor platform is now ready with a **Coursera-inspired premium design**. 

Start exploring, learning, and achieving! 🚀

For questions, check the documentation or explore the code—everything is well-documented and easy to customize.

**Happy Learning!** 📚✨
