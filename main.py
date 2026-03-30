"""
PawPal+ Demo Script

This script demonstrates the core functionality of the PawPal+ system:
- Creating owners and pets
- Adding tasks to pets
- Viewing daily schedules
- Detecting conflicts
- Marking tasks complete (with recurring task creation)
"""

from pawpal_system import Task, Pet, Owner, Scheduler


def main():
    """Run the PawPal+ demo."""
    
    print("\n" + "=" * 60)
    print("🐾 WELCOME TO PAWPAL+ DEMO 🐾".center(60))
    print("=" * 60 + "\n")
    
    # Step 1: Create an Owner
    print("📝 Creating Owner...")
    owner = Owner(name="Sarah")
    print(f"✓ {owner}\n")
    
    # Step 2: Create Pets
    print("📝 Creating Pets...")
    dog = Pet(name="Max", species="Dog", age=3, breed="Golden Retriever")
    cat = Pet(name="Whiskers", species="Cat", age=2, breed="Siamese")
    rabbit = Pet(name="Hop", species="Rabbit", age=1, breed="Holland Lop")
    
    owner.add_pet(dog)
    owner.add_pet(cat)
    owner.add_pet(rabbit)
    
    print(f"✓ {dog}")
    print(f"✓ {cat}")
    print(f"✓ {rabbit}\n")
    
    # Step 3: Add Tasks to Pets
    print("📝 Adding Tasks to Pets...\n")
    
    # Max (Dog) tasks
    dog.add_task(Task(description="Morning walk", time="08:00", frequency="daily"))
    dog.add_task(Task(description="Breakfast", time="07:30", frequency="daily"))
    dog.add_task(Task(description="Evening walk", time="18:00", frequency="daily"))
    dog.add_task(Task(description="Dinner", time="19:00", frequency="daily"))
    
    # Whiskers (Cat) tasks
    cat.add_task(Task(description="Breakfast", time="07:30", frequency="daily"))
    cat.add_task(Task(description="Lunch", time="12:00", frequency="daily"))
    cat.add_task(Task(description="Dinner", time="19:00", frequency="daily"))
    cat.add_task(Task(description="Play session", time="20:00", frequency="daily"))
    
    # Hop (Rabbit) tasks
    rabbit.add_task(Task(description="Morning hay", time="08:00", frequency="daily"))
    rabbit.add_task(Task(description="Vegetables", time="12:00", frequency="daily"))
    rabbit.add_task(Task(description="Evening hay", time="18:00", frequency="daily"))
    rabbit.add_task(Task(description="Clean cage", time="10:00", frequency="weekly"))
    
    print("✓ Tasks added successfully!\n")
    
    # Step 4: Create Scheduler
    print("📝 Initializing Scheduler...")
    scheduler = Scheduler(owner)
    print(f"✓ {scheduler}\n")
    
    # Step 5: Display Daily Schedule
    print(scheduler.get_daily_report())
    
    # Step 6: Test Filtering by Pet
    print("\n" + "=" * 60)
    print("🔍 FILTERING: Tasks for Max (Dog) Only".center(60))
    print("=" * 60)
    all_tasks = owner.get_all_tasks()
    max_tasks = scheduler.filter_by_pet(all_tasks, "Max")
    for task in scheduler.sort_by_time(max_tasks):
        print(f"  {task}")
    
    # Step 7: Test Sorting
    print("\n" + "=" * 60)
    print("📊 SORTING: All Tasks by Time".center(60))
    print("=" * 60)
    sorted_tasks = scheduler.get_sorted_tasks(all_tasks)
    for task in sorted_tasks:
        print(f"  {task}")
    
    # Step 8: Create and Test Conflict Detection
    print("\n" + "=" * 60)
    print("⚠️  TESTING: Conflict Detection".center(60))
    print("=" * 60)
    conflicts = scheduler.detect_conflicts(all_tasks)
    if conflicts:
        for conflict in conflicts:
            print(f"  {conflict}")
    else:
        print("  ✓ No conflicts detected in current schedule")
    
    # Step 9: Test Mark Complete and Recurring Tasks
    print("\n" + "=" * 60)
    print("✅ TESTING: Mark Task Complete & Recurring Tasks".center(60))
    print("=" * 60)
    
    # Get Max's breakfast task (daily recurring)
    breakfast_task = None
    for task in dog.get_tasks():
        if "Breakfast" in task.description and task.frequency == "daily":
            breakfast_task = task
            break
    
    if breakfast_task:
        print(f"\n  Before: {breakfast_task}")
        print(f"  Task completed count before: {len(dog.get_tasks())}")
        
        # Mark as complete (should create a new recurring task)
        scheduler.mark_task_complete(breakfast_task)
        
        print(f"\n  After: {breakfast_task}")
        print(f"  Task completed count after: {len(dog.get_tasks())}")
        print(f"  ✓ New recurring task created: {dog.get_tasks()[-1]}")
    
    # Step 10: Test Incomplete Tasks Filter
    print("\n" + "=" * 60)
    print("📋 FILTERING: Incomplete Tasks Only".center(60))
    print("=" * 60)
    incomplete_tasks = scheduler.filter_by_status(all_tasks, completed=False)
    print(f"  Total incomplete tasks: {len(incomplete_tasks)}")
    print(f"  Sample: {incomplete_tasks[:3] if incomplete_tasks else 'None'}")
    
    # Step 11: Summary Statistics
    print("\n" + "=" * 60)
    print("📊 SYSTEM SUMMARY".center(60))
    print("=" * 60)
    total_tasks = len(owner.get_all_tasks())
    print(f"  👤 Owner: {owner.name}")
    print(f"  🐾 Total Pets: {len(owner.get_pets())}")
    print(f"  📋 Total Tasks: {total_tasks}")
    print(f"  ✅ Completed: {len(scheduler.filter_by_status(all_tasks, True))}")
    print(f"  ⏳ Pending: {len(scheduler.filter_by_status(all_tasks, False))}")
    
    print("\n" + "=" * 60)
    print("✨ DEMO COMPLETE! ✨".center(60))
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
