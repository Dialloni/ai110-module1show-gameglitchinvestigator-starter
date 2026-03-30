"""
Test Suite for PawPal+ System

Automated tests covering core functionality:
- Task management and completion
- Pet task tracking
- Sorting and filtering
- Conflict detection
- Recurring task logic
"""

import pytest
from pawpal_system import Owner, Pet, Task, Scheduler


class TestTask:
    """Tests for the Task class."""
    
    def test_task_creation(self):
        """Verify that a task can be created with all attributes."""
        task = Task("Feed dog", "09:00", "daily")
        assert task.description == "Feed dog"
        assert task.time == "09:00"
        assert task.frequency == "daily"
        assert task.completed is False
    
    def test_mark_task_complete(self):
        """Verify that marking a task complete changes its status."""
        task = Task("Morning walk", "08:00", "daily")
        assert task.completed is False
        
        task.mark_complete()
        assert task.completed is True
    
    def test_is_recurring_daily(self):
        """Verify that daily tasks are identified as recurring."""
        task = Task("Feed", "09:00", "daily")
        assert task.is_recurring() is True
    
    def test_is_recurring_weekly(self):
        """Verify that weekly tasks are identified as recurring."""
        task = Task("Grooming", "10:00", "weekly")
        assert task.is_recurring() is True
    
    def test_is_recurring_once(self):
        """Verify that one-time tasks are not recurring."""
        task = Task("Vet appointment", "14:00", "once")
        assert task.is_recurring() is False


class TestPet:
    """Tests for the Pet class."""
    
    def test_pet_creation(self):
        """Verify that a pet can be created with all attributes."""
        pet = Pet("Fluffy", "Dog", 3, "Golden Retriever")
        assert pet.name == "Fluffy"
        assert pet.species == "Dog"
        assert pet.age == 3
        assert pet.breed == "Golden Retriever"
        assert len(pet.tasks) == 0
    
    def test_add_task_to_pet(self):
        """Verify that a task can be added to a pet."""
        pet = Pet("Whiskers", "Cat", 5, "Siamese")
        task = Task("Feed", "09:00", "daily")
        
        pet.add_task(task)
        
        assert len(pet.tasks) == 1
        assert pet.tasks[0] == task
        assert task.pet_name == "Whiskers"
    
    def test_get_task_count(self):
        """Verify that pet task count increases when tasks are added."""
        pet = Pet("Buddy", "Dog", 7, "Labrador")
        assert pet.get_task_count() == 0
        
        pet.add_task(Task("Walk", "08:00", "daily"))
        assert pet.get_task_count() == 1
        
        pet.add_task(Task("Feed", "09:00", "daily"))
        assert pet.get_task_count() == 2
    
    def test_get_tasks(self):
        """Verify that get_tasks returns all tasks for a pet."""
        pet = Pet("Max", "Dog", 2, "Poodle")
        task1 = Task("Walk", "08:00", "daily")
        task2 = Task("Feed", "12:00", "daily")
        
        pet.add_task(task1)
        pet.add_task(task2)
        
        tasks = pet.get_tasks()
        assert len(tasks) == 2
        assert task1 in tasks
        assert task2 in tasks


class TestOwner:
    """Tests for the Owner class."""
    
    def test_owner_creation(self):
        """Verify that an owner can be created."""
        owner = Owner("Alice")
        assert owner.name == "Alice"
        assert len(owner.pets) == 0
    
    def test_add_pet_to_owner(self):
        """Verify that pets can be added to an owner."""
        owner = Owner("Bob")
        pet1 = Pet("Fluffy", "Dog", 3, "Poodle")
        pet2 = Pet("Whiskers", "Cat", 5, "Siamese")
        
        owner.add_pet(pet1)
        owner.add_pet(pet2)
        
        assert len(owner.pets) == 2
        assert pet1 in owner.pets
        assert pet2 in owner.pets
    
    def test_get_all_tasks(self):
        """Verify that all tasks from all pets can be retrieved."""
        owner = Owner("Charlie")
        
        pet1 = Pet("Dog", "Dog", 3, "Labrador")
        pet1.add_task(Task("Walk", "08:00", "daily"))
        pet1.add_task(Task("Feed", "09:00", "daily"))
        owner.add_pet(pet1)
        
        pet2 = Pet("Cat", "Cat", 5, "Siamese")
        pet2.add_task(Task("Feed", "10:00", "daily"))
        owner.add_pet(pet2)
        
        all_tasks = owner.get_all_tasks()
        assert len(all_tasks) == 3


class TestScheduler:
    """Tests for the Scheduler class."""
    
    @pytest.fixture
    def scheduler_with_tasks(self):
        """Create a scheduler with sample data for testing."""
        owner = Owner("Sarah")
        
        pet1 = Pet("Fluffy", "Dog", 3, "Golden Retriever")
        pet1.add_task(Task("Walk", "08:00", "daily"))
        pet1.add_task(Task("Feed", "09:00", "daily"))
        pet1.add_task(Task("Play", "15:00", "daily"))
        owner.add_pet(pet1)
        
        pet2 = Pet("Whiskers", "Cat", 5, "Siamese")
        pet2.add_task(Task("Feed", "08:30", "daily"))
        pet2.add_task(Task("Nap", "14:00", "daily"))
        owner.add_pet(pet2)
        
        scheduler = Scheduler(owner)
        return scheduler
    
    def test_scheduler_creation(self):
        """Verify that a scheduler can be created."""
        owner = Owner("David")
        scheduler = Scheduler(owner)
        assert scheduler.owner == owner
    
    def test_get_today_tasks(self, scheduler_with_tasks):
        """Verify that today's incomplete tasks are retrieved."""
        tasks = scheduler_with_tasks.get_today_tasks()
        assert len(tasks) == 5
        
        # All should be incomplete
        for task in tasks:
            assert task.completed is False
    
    def test_sort_by_time(self, scheduler_with_tasks):
        """Verify that tasks are sorted chronologically."""
        tasks = scheduler_with_tasks.get_today_tasks()
        sorted_tasks = scheduler_with_tasks.sort_by_time(tasks)
        
        # Extract times in order
        times = [t.time for t in sorted_tasks]
        assert times == ["08:00", "08:30", "09:00", "14:00", "15:00"]
    
    def test_filter_by_pet(self, scheduler_with_tasks):
        """Verify that filtering by pet name works correctly."""
        tasks = scheduler_with_tasks.owner.get_all_tasks()
        fluffy_tasks = scheduler_with_tasks.filter_by_pet(tasks, "Fluffy")
        
        assert len(fluffy_tasks) == 3
        for task in fluffy_tasks:
            assert task.pet_name == "Fluffy"
    
    def test_filter_by_status_incomplete(self, scheduler_with_tasks):
        """Verify that filtering by incomplete status works."""
        tasks = scheduler_with_tasks.owner.get_all_tasks()
        incomplete = scheduler_with_tasks.filter_by_status(tasks, completed=False)
        
        assert len(incomplete) == 5
        for task in incomplete:
            assert task.completed is False
    
    def test_filter_by_status_complete(self, scheduler_with_tasks):
        """Verify that filtering by completed status works."""
        tasks = scheduler_with_tasks.owner.get_all_tasks()
        
        # Mark one task complete
        tasks[0].mark_complete()
        
        completed = scheduler_with_tasks.filter_by_status(tasks, completed=True)
        assert len(completed) == 1
        assert completed[0].completed is True
    
    def test_detect_conflicts_no_conflict(self, scheduler_with_tasks):
        """Verify that no conflicts are detected when tasks are at different times."""
        tasks = scheduler_with_tasks.get_today_tasks()
        conflicts = scheduler_with_tasks.detect_conflicts(tasks)
        
        assert len(conflicts) == 0
    
    def test_detect_conflicts_with_conflict(self):
        """Verify that conflicts are detected when tasks overlap."""
        owner = Owner("Emily")
        
        pet1 = Pet("Dog", "Dog", 3, "Poodle")
        pet1.add_task(Task("Walk", "08:00", "daily"))
        owner.add_pet(pet1)
        
        pet2 = Pet("Cat", "Cat", 5, "Siamese")
        pet2.add_task(Task("Vet visit", "08:00", "once"))
        owner.add_pet(pet2)
        
        scheduler = Scheduler(owner)
        tasks = owner.get_all_tasks()
        conflicts = scheduler.detect_conflicts(tasks)
        
        assert len(conflicts) == 1
        assert "08:00" in conflicts[0]
    
    def test_create_recurring_task(self, scheduler_with_tasks):
        """Verify that a new task is created for recurring tasks."""
        task = Task("Feed", "09:00", "daily")
        new_task = scheduler_with_tasks.create_recurring_task(task)
        
        assert new_task is not None
        assert new_task.description == task.description
        assert new_task.time == task.time
        assert new_task.completed is False
    
    def test_create_recurring_task_once(self):
        """Verify that no new task is created for one-time tasks."""
        scheduler = Scheduler(Owner("Frank"))
        task = Task("Vet appointment", "14:00", "once")
        new_task = scheduler.create_recurring_task(task)
        
        assert new_task is None
    
    def test_mark_task_complete_non_recurring(self):
        """Verify that completing a non-recurring task doesn't create a new one."""
        owner = Owner("Grace")
        pet = Pet("Dog", "Dog", 3, "Labrador")
        task = Task("Vet visit", "10:00", "once")
        pet.add_task(task)
        owner.add_pet(pet)
        
        scheduler = Scheduler(owner)
        initial_count = pet.get_task_count()
        
        scheduler.mark_task_complete(task)
        
        assert task.completed is True
        assert pet.get_task_count() == initial_count
    
    def test_mark_task_complete_recurring(self):
        """Verify that completing a recurring task creates a new instance."""
        owner = Owner("Henry")
        pet = Pet("Dog", "Dog", 3, "Poodle")
        task = Task("Walk", "08:00", "daily")
        pet.add_task(task)
        owner.add_pet(pet)
        
        scheduler = Scheduler(owner)
        initial_count = pet.get_task_count()
        
        scheduler.mark_task_complete(task)
        
        assert task.completed is True
        assert pet.get_task_count() == initial_count + 1
        
        # The new task should be identical except for completed status
        new_task = pet.get_tasks()[-1]
        assert new_task.description == task.description
        assert new_task.time == task.time
        assert new_task.completed is False
    
    def test_get_sorted_tasks_default(self, scheduler_with_tasks):
        """Verify that get_sorted_tasks uses today's tasks by default."""
        sorted_tasks = scheduler_with_tasks.get_sorted_tasks()
        
        assert len(sorted_tasks) == 5
        times = [t.time for t in sorted_tasks]
        assert times == sorted(times)
    
    def test_get_sorted_tasks_custom_list(self, scheduler_with_tasks):
        """Verify that get_sorted_tasks can sort a custom task list."""
        owner = Owner("Iris")
        pet = Pet("Cat", "Cat", 5, "Siamese")
        
        # Add tasks out of order
        task3 = Task("Dinner", "18:00", "daily")
        task1 = Task("Breakfast", "08:00", "daily")
        task2 = Task("Lunch", "12:00", "daily")
        
        pet.add_task(task3)
        pet.add_task(task1)
        pet.add_task(task2)
        owner.add_pet(pet)
        
        scheduler = Scheduler(owner)
        custom_tasks = [task3, task1, task2]
        sorted_tasks = scheduler.get_sorted_tasks(custom_tasks)
        
        times = [t.time for t in sorted_tasks]
        assert times == ["08:00", "12:00", "18:00"]
    
    def test_get_daily_report(self, scheduler_with_tasks):
        """Verify that the daily report is generated correctly."""
        report = scheduler_with_tasks.get_daily_report()
        
        assert "TODAY'S SCHEDULE" in report
        assert "Fluffy" in report or "Walk" in report
        assert isinstance(report, str)
        assert len(report) > 0


class TestIntegration:
    """Integration tests covering complete workflows."""
    
    def test_complete_workflow(self):
        """Test a complete workflow from owner creation to task completion."""
        # Create owner and pets
        owner = Owner("Test Owner")
        dog = Pet("Rex", "Dog", 4, "German Shepherd")
        cat = Pet("Mittens", "Cat", 2, "Tabby")
        owner.add_pet(dog)
        owner.add_pet(cat)
        
        # Add tasks
        task1 = Task("Walk", "07:00", "daily")
        task2 = Task("Feed", "08:00", "daily")
        task3 = Task("Groom", "14:00", "weekly")
        
        dog.add_task(task1)
        dog.add_task(task2)
        cat.add_task(task3)
        
        # Create scheduler and verify workflow
        scheduler = Scheduler(owner)
        
        assert len(owner.get_all_tasks()) == 3
        assert scheduler.detect_conflicts(owner.get_all_tasks()) == []
        
        # Sort tasks
        sorted_tasks = scheduler.sort_by_time(owner.get_all_tasks())
        assert sorted_tasks[0].time == "07:00"
        
        # Mark task complete
        scheduler.mark_task_complete(task1)
        assert task1.completed is True
        assert len(dog.get_tasks()) == 3  # Original 2 + 1 new recurring
        
        # Filter by pet
        dog_tasks = scheduler.filter_by_pet(owner.get_all_tasks(), "Rex")
        assert len(dog_tasks) == 3
