# 🐾 PawPal+: Smart Pet Care Management System

A professional, AI-assisted pet care management application built with Python, OOP, and Streamlit.

## 📖 Overview

PawPal+ is an intelligent pet care management system that helps pet owners maintain their furry friends' health and happiness by:
- 🐕 Managing multiple pets (dogs, cats, rabbits, etc.)
- ⏰ Scheduling daily tasks (feeding, walks, medications, vet appointments)
- 📅 Organizing schedules with automatic sorting and conflict detection
- 🔄 Automating recurring tasks with intelligent rescheduling

**Built with**: Python + OOP + Streamlit + pytest + AI Collaboration

---

## 🚀 Quick Start

### Option 1: See the System in Action (CLI Demo)
```bash
pip install -r requirements.txt
python pawpal_main.py
```

**What you'll see:**
- System creates 3 pets (Fluffy, Whiskers, Buddy)
- Schedules 9 tasks at different times
- Sorts tasks chronologically
- Detects conflicts (warning: 3 tasks at 08:00!)
- Auto-creates recurring task
- Generates daily report

### Option 2: Use the Web App (Streamlit)
```bash
streamlit run pawpal_app.py
```

**Open in browser**: http://localhost:8501

Features:
- 📊 Dashboard with pet overview
- 🐕 Manage your pets
- ⏰ Schedule tasks with quick templates
- 📅 View daily schedule
- ⚙️ System settings

### Option 3: Run the Test Suite
```bash
python -m pytest tests/test_pawpal.py -v
```

**Result**: ✅ 28 tests passing (100% pass rate)

---

## � Project Structure

```
ai110-week2/
├── pawpal_system.py       # Core logic: Owner, Pet, Task, Scheduler classes
├── pawpal_main.py         # CLI demo script for testing backend
├── pawpal_app.py          # Streamlit web UI
├── requirements.txt       # Python dependencies
├── tests/
│   └── test_pawpal.py     # Automated test suite (28 tests)
├── PAWPAL_README.md       # Detailed feature overview
├── PAWPAL_reflection.md   # Design decisions & AI collaboration
├── IMPLEMENTATION_GUIDE.md # Technical documentation
└── PAWPAL_QUICK_REFERENCE.md # Quick reference guide
```

---

## 🎯 Core Features

### ✅ Task Management
- Create tasks with specific times and frequencies (once, daily, weekly)
- Mark tasks complete with automatic recurrence handling
- Track task status across all pets

### 🧠 Smart Algorithms
- **Sorting**: Tasks ordered chronologically by time
- **Filtering**: View tasks by pet name or completion status
- **Conflict Detection**: Identify overlapping task times
- **Recurring Automation**: Daily/weekly tasks automatically reschedule

### 📊 Professional UI
- 5-page Streamlit dashboard
- Session state persistence
- Responsive design with metrics and warnings
- User-friendly task templates

---

## 📚 Documentation

- **[PAWPAL_README.md](./PAWPAL_README.md)** - Complete feature overview and architecture
- **[PAWPAL_reflection.md](./PAWPAL_reflection.md)** - Design decisions and AI collaboration details
- **[IMPLEMENTATION_GUIDE.md](./IMPLEMENTATION_GUIDE.md)** - Technical implementation guide
- **[PAWPAL_QUICK_REFERENCE.md](./PAWPAL_QUICK_REFERENCE.md)** - Quick reference card
- **[PROJECT_COMPLETION_SUMMARY.md](./PROJECT_COMPLETION_SUMMARY.md)** - Full completion report

---

## 🧪 Testing

The project includes a comprehensive automated test suite:

```bash
python -m pytest tests/test_pawpal.py -v
```

**Test Coverage:**
- ✅ Task completion and status changes
- ✅ Pet task management
- ✅ Owner pet management
- ✅ Sorting tasks chronologically
- ✅ Filtering by pet and status
- ✅ Conflict detection
- ✅ Recurring task automation
- ✅ Integration workflows

**Confidence Level**: ⭐⭐⭐⭐ (4/5 stars)

---

## 🎓 Design Highlights

### Object-Oriented Architecture
Four core classes with clear responsibilities:
- **Task**: Represents individual activities
- **Pet**: Manages pet information and task lists
- **Owner**: Manages multiple pets
- **Scheduler**: The intelligent "brain" that organizes and analyzes tasks

### Smart Algorithms
1. **Chronological Sorting**: Convert "HH:MM" to minutes for accurate ordering
2. **Status Filtering**: Simple list comprehension for performance
3. **Conflict Detection**: Group tasks by time to identify overlaps
4. **Recurring Automation**: Auto-create next occurrence when task completes

### AI Collaboration
- Used Copilot for architecture brainstorming and UML design
- Leveraged AI for algorithm suggestions and code scaffolding
- Maintained human oversight for design decisions
- Documented tradeoffs and design rationale

---

## 📸 Demo Screenshots

Run `python pawpal_main.py` to see the CLI demo, or `streamlit run pawpal_app.py` for the web interface.

---

## 📝 Reflection & Lessons Learned

See **[PAWPAL_reflection.md](./PAWPAL_reflection.md)** for detailed reflection on:
- Initial design vision
- Algorithmic tradeoffs
- Testing strategy
- AI collaboration approach
- Key learnings

---

## 🤝 Contributing

This project was built as an educational exercise in:
- System design using OOP
- Algorithmic thinking
- Test-driven development
- AI-assisted development

Feel free to fork and extend!

---

**Built with ❤️ using Python, OOP, and AI Collaboration**
