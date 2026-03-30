"""
PawPal+ Streamlit Web Application

A modern, user-friendly interface for managing pet care tasks and schedules.
"""

import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler


# Configure page
st.set_page_config(
    page_title="PawPal+ - Pet Care Manager",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .task-item {
        background-color: #e8f4f8;
        padding: 1rem;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
        border-radius: 0.25rem;
    }
    .conflict-warning {
        background-color: #fff3cd;
        padding: 1rem;
        border-left: 4px solid #ff6b6b;
        margin: 0.5rem 0;
        border-radius: 0.25rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "owner" not in st.session_state:
    st.session_state.owner = Owner("My Pets")
    st.session_state.scheduler = Scheduler(st.session_state.owner)

owner = st.session_state.owner
scheduler = st.session_state.scheduler


# Header
st.title("🐾 PawPal+ Smart Pet Care Manager")
st.markdown("*Intelligent scheduling and task management for your furry friends*")
st.divider()

# Sidebar Navigation
with st.sidebar:
    st.header("🗂️ Navigation")
    page = st.radio(
        "Select a page:",
        ["📊 Dashboard", "🐕 My Pets", "⏰ Schedule Tasks", "📅 Daily Schedule", "⚙️ Settings"]
    )

# PAGE 1: DASHBOARD
if page == "📊 Dashboard":
    st.header("📊 Dashboard Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Pets", len(owner.get_pets()))
    
    with col2:
        total_tasks = len(owner.get_all_tasks())
        st.metric("Total Tasks", total_tasks)
    
    with col3:
        incomplete = len(scheduler.filter_by_status(owner.get_all_tasks(), completed=False))
        st.metric("Pending Tasks", incomplete)
    
    with col4:
        complete = len(scheduler.filter_by_status(owner.get_all_tasks(), completed=True))
        st.metric("Completed", complete)
    
    st.divider()
    
    # Quick stats
    if owner.get_pets():
        st.subheader("🐾 Pet Overview")
        for pet in owner.get_pets():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{pet.name}** - {pet.species} ({pet.breed}), {pet.age} years old")
            with col2:
                st.metric("Tasks", pet.get_task_count())
    else:
        st.info("👉 Add your first pet in the 'My Pets' section!")
    
    st.divider()
    
    # Upcoming tasks
    st.subheader("📋 Next Tasks (Sorted by Time)")
    all_tasks = owner.get_all_tasks()
    
    if all_tasks:
        sorted_tasks = scheduler.sort_by_time(
            scheduler.filter_by_status(all_tasks, completed=False)
        )
        
        if sorted_tasks:
            for i, task in enumerate(sorted_tasks[:5], 1):
                status = "✅" if task.completed else "⭕"
                col1, col2, col3 = st.columns([1, 2, 1])
                with col1:
                    st.write(f"{status} {task.time}")
                with col2:
                    st.write(f"**{task.description}** ({task.pet_name})")
                with col3:
                    st.write(f"*{task.frequency}*")
        else:
            st.success("✨ All tasks completed! Great job!")
    else:
        st.info("No tasks scheduled yet. Add a pet and schedule some tasks!")

# PAGE 2: MY PETS
elif page == "🐕 My Pets":
    st.header("🐕 My Pets")
    
    tab1, tab2 = st.tabs(["View Pets", "Add New Pet"])
    
    with tab1:
        if owner.get_pets():
            for pet in owner.get_pets():
                with st.expander(f"🐾 {pet.name} - {pet.species} ({pet.breed})"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Species:** {pet.species}")
                        st.write(f"**Breed:** {pet.breed}")
                        st.write(f"**Age:** {pet.age} years")
                    
                    with col2:
                        st.write(f"**Tasks:** {pet.get_task_count()}")
                        st.write("**Status:** Active")
                    
                    st.divider()
                    st.subheader(f"{pet.name}'s Tasks")
                    
                    tasks = pet.get_tasks()
                    if tasks:
                        sorted_pet_tasks = scheduler.sort_by_time(tasks)
                        for task in sorted_pet_tasks:
                            col1, col2, col3 = st.columns([2, 2, 1])
                            with col1:
                                st.write(f"{task}")
                            with col2:
                                if st.button(
                                    f"✓ Mark Complete",
                                    key=f"complete_{id(task)}"
                                ):
                                    scheduler.mark_task_complete(task)
                                    st.success(f"Marked '{task.description}' as complete!")
                                    st.rerun()
                    else:
                        st.info(f"No tasks assigned to {pet.name} yet.")
        else:
            st.info("You haven't added any pets yet. Create one in the 'Add New Pet' tab!")
    
    with tab2:
        st.subheader("Add a New Pet")
        
        col1, col2 = st.columns(2)
        with col1:
            pet_name = st.text_input("Pet Name", placeholder="e.g., Fluffy")
        with col2:
            species = st.selectbox("Species", ["Dog", "Cat", "Rabbit", "Bird", "Hamster", "Other"])
        
        col1, col2 = st.columns(2)
        with col1:
            breed = st.text_input("Breed", placeholder="e.g., Golden Retriever")
        with col2:
            age = st.number_input("Age (years)", min_value=0, max_value=30, value=1)
        
        if st.button("➕ Add Pet", use_container_width=True):
            if pet_name.strip():
                new_pet = Pet(pet_name, species, age, breed)
                owner.add_pet(new_pet)
                st.success(f"✅ {pet_name} has been added!")
                st.balloons()
                st.rerun()
            else:
                st.error("Please enter a pet name.")

# PAGE 3: SCHEDULE TASKS
elif page == "⏰ Schedule Tasks":
    st.header("⏰ Schedule a Task")
    
    if not owner.get_pets():
        st.warning("⚠️ Please add a pet first in the 'My Pets' section.")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            pet_name = st.selectbox(
                "Select Pet",
                [pet.name for pet in owner.get_pets()]
            )
        with col2:
            description = st.text_input("Task Description", placeholder="e.g., Morning walk")
        
        col1, col2 = st.columns(2)
        with col1:
            time = st.time_input("Task Time", value=None)
        with col2:
            frequency = st.selectbox(
                "Frequency",
                ["once", "daily", "weekly"],
                help="How often should this task repeat?"
            )
        
        if st.button("➕ Schedule Task", use_container_width=True):
            if description.strip() and time:
                # Find the pet
                selected_pet = None
                for pet in owner.get_pets():
                    if pet.name == pet_name:
                        selected_pet = pet
                        break
                
                if selected_pet:
                    # Convert time object to HH:MM string
                    time_str = time.strftime("%H:%M")
                    
                    # Create and add task
                    new_task = Task(description, time_str, frequency)
                    selected_pet.add_task(new_task)
                    
                    st.success(f"✅ Task '{description}' scheduled for {pet_name} at {time_str}!")
                    st.rerun()
            else:
                st.error("Please fill in all fields.")
        
        st.divider()
        st.subheader("📋 Quick Task Templates")
        
        templates = {
            "🍽️ Feeding": ("Feeding", "08:00", "daily"),
            "🚶 Walk": ("Walk", "09:00", "daily"),
            "💊 Medication": ("Medication", "12:00", "daily"),
            "🎮 Playtime": ("Playtime", "15:00", "daily"),
            "🛁 Grooming": ("Grooming", "10:00", "weekly"),
            "🏥 Vet Checkup": ("Vet Checkup", "14:00", "once"),
        }
        
        col1, col2, col3 = st.columns(3)
        cols = [col1, col2, col3]
        
        for idx, (label, (task_desc, task_time, task_freq)) in enumerate(templates.items()):
            with cols[idx % 3]:
                if st.button(label, use_container_width=True):
                    selected_pet = None
                    for pet in owner.get_pets():
                        if pet.name == pet_name:
                            selected_pet = pet
                            break
                    
                    if selected_pet:
                        new_task = Task(task_desc, task_time, task_freq)
                        selected_pet.add_task(new_task)
                        st.success(f"✅ Added: {label}")
                        st.rerun()

# PAGE 4: DAILY SCHEDULE
elif page == "📅 Daily Schedule":
    st.header("📅 Today's Schedule")
    
    all_tasks = owner.get_all_tasks()
    
    if not all_tasks:
        st.info("📝 No tasks scheduled yet. Add some in the 'Schedule Tasks' section!")
    else:
        # Get sorted tasks
        sorted_tasks = scheduler.sort_by_time(
            scheduler.filter_by_status(all_tasks, completed=False)
        )
        
        # Check for conflicts
        conflicts = scheduler.detect_conflicts(sorted_tasks)
        
        if conflicts:
            st.subheader("⚠️ Schedule Conflicts")
            for conflict in conflicts:
                st.warning(conflict)
        
        # Display schedule
        st.subheader("🕐 Tasks by Time")
        
        if sorted_tasks:
            for task in sorted_tasks:
                col1, col2, col3, col4 = st.columns([1, 2, 1.5, 1])
                
                with col1:
                    st.write(f"🕐 **{task.time}**")
                with col2:
                    st.write(f"{task.description}")
                with col3:
                    st.write(f"🐾 {task.pet_name}")
                with col4:
                    if st.button("✓", key=f"mark_{id(task)}"):
                        scheduler.mark_task_complete(task)
                        st.success("Task completed!")
                        st.rerun()
        else:
            st.success("✨ All tasks for today are complete!")
        
        # Filter by pet
        st.divider()
        st.subheader("🔍 Filter by Pet")
        
        selected_pet = st.selectbox(
            "Select a pet to filter",
            ["All"] + [pet.name for pet in owner.get_pets()],
            key="filter_pet"
        )
        
        if selected_pet != "All":
            filtered_tasks = scheduler.filter_by_pet(sorted_tasks, selected_pet)
            if filtered_tasks:
                for task in filtered_tasks:
                    st.write(f"  {task}")
            else:
                st.info(f"No tasks for {selected_pet} today.")

# PAGE 5: SETTINGS
elif page == "⚙️ Settings":
    st.header("⚙️ Settings & Statistics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 System Statistics")
        st.metric("Total Pets", len(owner.get_pets()))
        st.metric("Total Tasks", len(owner.get_all_tasks()))
        st.metric("Completed Tasks", len(scheduler.filter_by_status(
            owner.get_all_tasks(), completed=True
        )))
    
    with col2:
        st.subheader("🎯 System Info")
        st.write(f"**Owner:** {owner.name}")
        st.write(f"**Scheduler Status:** {scheduler}")
    
    st.divider()
    
    st.subheader("🧹 Data Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Clear All Data"):
            st.session_state.owner = Owner("My Pets")
            st.session_state.scheduler = Scheduler(st.session_state.owner)
            st.success("All data has been cleared!")
            st.rerun()
    
    with col2:
        if st.button("📊 Export Summary"):
            st.info("This feature will be available in a future update.")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; margin-top: 2rem; color: #666;'>
    <p>🐾 <b>PawPal+</b> - Smart Pet Care Management System</p>
    <p>Built with ❤️ and Python | Powered by Streamlit & AI</p>
</div>
""", unsafe_allow_html=True)
