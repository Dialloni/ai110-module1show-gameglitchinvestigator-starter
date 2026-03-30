"""
PawPal+ CLI Demo Script

This script demonstrates the core functionality of the PawPal+ system
by creating an owner, multiple pets, and scheduling various tasks.
"""

from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    """Run a complete demo of the PawPal+ system."""
    
    print("\n" + "=" * 60)
    print("🐾 PAWPAL+ SMART PET CARE MANAGEMENT SYSTEM 🐾")
    print("=" * 60)
    
    # PHASE 2: Create an Owner and Pets
    print("\n📝 Creating pet owner and pets...\n")
    
    owner = Owner("Sarah")
    print(f"✅ {owner}")
    
    # Create pets
    fluffy = Pet("Fluffy", "Dog", 3, "Golden Retriever")
    owner.add_pet(fluffy)
    print(f"✅ {fluffy}")
    
    whiskers = Pet("Whiskers", "Cat", 5, "Siamese")
    owner.add_pet(whiskers)
    print(f"✅ {whiskers}")
    
    buddy = Pet("Buddy", "Dog", 7, "Labrador")
    owner.add_pet(buddy)
    print(f"✅ {buddy}")
    
    # PHASE 2: Schedule Tasks
    print("\n⏰ Scheduling tasks...\n")
    
    # Fluffy's tasks
    task1 = Task("Morning walk", "08:00", "daily")
    fluffy.add_task(task1)
    print(f"✅ Added task: {task1}")
    
    task2 = Task("Breakfast", "08:30", "daily")
    fluffy.add_task(task2)
    print(f"✅ Added task: {task2}")
    
    task3 = Task("Afternoon walk", "14:00", "daily")
    fluffy.add_task(task3)
    print(f"✅ Added task: {task3}")
    
    # Whiskers's tasks
    task4 = Task("Breakfast", "09:00", "daily")
    whiskers.add_task(task4)
    print(f"✅ Added task: {task4}")
    
    task5 = Task("Lunch", "12:30", "daily")
    whiskers.add_task(task5)
    print(f"✅ Added task: {task5}")
    
    task6 = Task("Playtime", "15:00", "daily")
    whiskers.add_task(task6)
    print(f"✅ Added task: {task6}")
    
    # Buddy's tasks
    task7 = Task("Evening walk", "18:00", "daily")
    buddy.add_task(task7)
    print(f"✅ Added task: {task7}")
    
    task8 = Task("Medication", "08:00", "daily")
    buddy.add_task(task8)
    print(f"✅ Added task: {task8}")
    
    # Add a conflicting task (same time as another task)
    task9 = Task("Vet appointment", "08:00", "once")
    fluffy.add_task(task9)
    print(f"✅ Added task: {task9} (CONFLICT with Buddy's medication!)")
    
    # PHASE 3: Create Scheduler and demonstrate smart features
    print("\n" + "=" * 60)
    print("🧠 SMART SCHEDULING FEATURES")
    print("=" * 60)
    
    scheduler = Scheduler(owner)
    print(f"\n✅ {scheduler}")
    
    # Get all tasks
    all_tasks = owner.get_all_tasks()
    print(f"\n📋 Total tasks across all pets: {len(all_tasks)}")
    
    # PHASE 3: Sorting
    print("\n" + "-" * 60)
    print("📊 SORTING: Tasks by Time (Chronological Order)")
    print("-" * 60)
    
    sorted_tasks = scheduler.sort_by_time(all_tasks)
    for task in sorted_tasks:
        print(f"  {task}")
    
    # PHASE 3: Filtering by Pet
    print("\n" + "-" * 60)
    print("🐕 FILTERING: Fluffy's Tasks")
    print("-" * 60)
    
    fluffy_tasks = scheduler.filter_by_pet(all_tasks, "Fluffy")
    sorted_fluffy = scheduler.sort_by_time(fluffy_tasks)
    for task in sorted_fluffy:
        print(f"  {task}")
    
    # PHASE 3: Filtering by Status
    print("\n" + "-" * 60)
    print("✅ FILTERING: Only Completed Tasks")
    print("-" * 60)
    
    # Mark a task as complete
    task1.mark_complete()
    print(f"  Marked as complete: {task1}")
    
    completed_tasks = scheduler.filter_by_status(all_tasks, completed=True)
    if completed_tasks:
        for task in completed_tasks:
            print(f"  {task}")
    else:
        print("  (Now showing completed tasks)")
    
    # PHASE 3: Conflict Detection
    print("\n" + "-" * 60)
    print("⚠️  CONFLICT DETECTION")
    print("-" * 60)
    
    conflicts = scheduler.detect_conflicts(sorted_tasks)
    if conflicts:
        for warning in conflicts:
            print(f"  {warning}")
    else:
        print("  No conflicts detected.")
    
    # PHASE 3: Recurring Tasks
    print("\n" + "-" * 60)
    print("🔄 RECURRING TASKS: Auto-Rescheduling")
    print("-" * 60)
    
    print(f"\n  Before marking complete: {len(fluffy.get_tasks())} tasks")
    print(f"  Task to complete: {task1}")
    
    scheduler.mark_task_complete(task1)
    
    print(f"\n  After marking complete: {len(fluffy.get_tasks())} tasks")
    new_task = fluffy.get_tasks()[-1]
    print(f"  New recurring task created: {new_task}")
    
    # Final Report
    print("\n" + "=" * 60)
    print("📅 FINAL DAILY REPORT")
    print("=" * 60)
    
    report = scheduler.get_daily_report()
    print(report)
    
    print("\n" + "=" * 60)
    print("✨ Demo completed successfully! ✨")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
