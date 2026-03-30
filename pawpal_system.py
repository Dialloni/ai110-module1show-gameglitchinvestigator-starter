"""
PawPal+ System Architecture

Core classes for managing pets, tasks, and schedules in an intelligent pet care system.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional


@dataclass
class Task:
    """
    Represents a single pet care task (feeding, walk, medication, etc.).
    
    Attributes:
        description: What the task is (e.g., "Morning walk")
        time: When the task should occur in "HH:MM" format (e.g., "09:00")
        frequency: How often the task repeats ("once", "daily", "weekly")
        completed: Whether the task has been marked as done
        pet_name: Name of the pet this task belongs to
    """
    description: str
    time: str  # Format: "HH:MM"
    frequency: str  # "once", "daily", "weekly"
    completed: bool = False
    pet_name: str = ""
    
    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True
    
    def is_recurring(self) -> bool:
        """Return True if task repeats (daily or weekly)."""
        return self.frequency in ["daily", "weekly"]
    
    def __repr__(self) -> str:
        status = "✓" if self.completed else "○"
        return f"{status} [{self.time}] {self.description} ({self.frequency})"


@dataclass
class Pet:
    """
    Represents a pet owned by the user.
    
    Attributes:
        name: Pet's name
        species: Type of animal (dog, cat, rabbit, etc.)
        age: Age in years
        breed: Breed information
        tasks: List of Task objects assigned to this pet
    """
    name: str
    species: str
    age: int
    breed: str
    tasks: List[Task] = field(default_factory=list)
    
    def add_task(self, task: Task) -> None:
        """Add a new task to this pet's schedule."""
        task.pet_name = self.name
        self.tasks.append(task)
    
    def get_tasks(self) -> List[Task]:
        """Return all tasks for this pet."""
        return self.tasks
    
    def get_task_count(self) -> int:
        """Return the number of tasks assigned to this pet."""
        return len(self.tasks)
    
    def __repr__(self) -> str:
        return f"🐾 {self.name} ({self.species}, {self.breed}, {self.age}y) - {self.get_task_count()} tasks"


@dataclass
class Owner:
    """
    Represents a pet owner who manages one or more pets.
    
    Attributes:
        name: Owner's name
        pets: List of Pet objects owned by this person
    """
    name: str
    pets: List[Pet] = field(default_factory=list)
    
    def add_pet(self, pet: Pet) -> None:
        """Add a new pet to this owner's collection."""
        self.pets.append(pet)
    
    def get_pets(self) -> List[Pet]:
        """Return all pets owned by this person."""
        return self.pets
    
    def get_all_tasks(self) -> List[Task]:
        """Return a flat list of all tasks from all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks
    
    def __repr__(self) -> str:
        return f"👤 {self.name} owns {len(self.pets)} pet(s)"


class Scheduler:
    """
    The "brain" of PawPal+ that manages, organizes, and intelligently schedules tasks.
    
    Attributes:
        owner: The Owner object whose pets and tasks are being managed
    """
    
    def __init__(self, owner: Owner):
        """Initialize scheduler with an owner."""
        self.owner = owner
    
    def get_today_tasks(self) -> List[Task]:
        """Retrieve all non-completed tasks for today."""
        all_tasks = self.owner.get_all_tasks()
        return [task for task in all_tasks if not task.completed]
    
    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """
        Sort tasks chronologically by their time.
        
        Args:
            tasks: List of tasks to sort
            
        Returns:
            Sorted list of tasks (earliest time first)
        """
        return sorted(tasks, key=lambda t: self._time_to_minutes(t.time))
    
    def _time_to_minutes(self, time_str: str) -> int:
        """Convert 'HH:MM' string to minutes since midnight."""
        try:
            hours, minutes = map(int, time_str.split(":"))
            return hours * 60 + minutes
        except (ValueError, AttributeError):
            return 0
    
    def filter_by_pet(self, tasks: List[Task], pet_name: str) -> List[Task]:
        """
        Filter tasks to only show those for a specific pet.
        
        Args:
            tasks: List of tasks to filter
            pet_name: Name of the pet to filter by
            
        Returns:
            List of tasks belonging to the specified pet
        """
        return [task for task in tasks if task.pet_name == pet_name]
    
    def filter_by_status(self, tasks: List[Task], completed: bool) -> List[Task]:
        """
        Filter tasks by completion status.
        
        Args:
            tasks: List of tasks to filter
            completed: True to get completed tasks, False for incomplete
            
        Returns:
            List of tasks matching the specified status
        """
        return [task for task in tasks if task.completed == completed]
    
    def detect_conflicts(self, tasks: List[Task]) -> List[str]:
        """
        Detect if multiple tasks are scheduled at the same time.
        
        Args:
            tasks: List of tasks to check for conflicts
            
        Returns:
            List of warning messages describing detected conflicts
        """
        warnings = []
        time_map = {}
        
        for task in tasks:
            if task.time not in time_map:
                time_map[task.time] = []
            time_map[task.time].append(task)
        
        for time_slot, task_list in time_map.items():
            if len(task_list) > 1:
                pet_names = [t.pet_name for t in task_list]
                warning = f"⚠️  Conflict at {time_slot}: {', '.join(pet_names)}"
                warnings.append(warning)
        
        return warnings
    
    def create_recurring_task(self, task: Task) -> Optional[Task]:
        """
        Create a new task instance for the next occurrence of a recurring task.
        
        Args:
            task: The completed task to recur
            
        Returns:
            New Task object for the next occurrence, or None if task doesn't recur
        """
        if not task.is_recurring():
            return None
        
        new_task = Task(
            description=task.description,
            time=task.time,
            frequency=task.frequency,
            completed=False,
            pet_name=task.pet_name
        )
        
        return new_task
    
    def mark_task_complete(self, task: Task) -> None:
        """
        Mark a task as complete and handle recurring tasks.
        
        Args:
            task: The task to complete
        """
        task.mark_complete()
        
        # If the task recurs, create a new instance
        if task.is_recurring():
            new_task = self.create_recurring_task(task)
            if new_task:
                # Find the pet and add the new task
                for pet in self.owner.get_pets():
                    if pet.name == task.pet_name:
                        pet.add_task(new_task)
                        break
    
    def get_sorted_tasks(self, tasks: Optional[List[Task]] = None) -> List[Task]:
        """
        Get all tasks sorted by time.
        
        Args:
            tasks: Optional list of tasks to sort. If None, uses today's tasks.
            
        Returns:
            Sorted list of tasks
        """
        if tasks is None:
            tasks = self.get_today_tasks()
        return self.sort_by_time(tasks)
    
    def get_daily_report(self) -> str:
        """
        Generate a human-readable daily schedule report.
        
        Returns:
            Formatted string showing all tasks for the day with warnings
        """
        tasks = self.get_sorted_tasks()
        conflicts = self.detect_conflicts(tasks)
        
        report = "\n📅 TODAY'S SCHEDULE\n"
        report += "=" * 50 + "\n"
        
        if not tasks:
            report += "No tasks scheduled for today.\n"
        else:
            for task in tasks:
                report += f"{task}\n"
        
        if conflicts:
            report += "\n⚠️  CONFLICTS DETECTED:\n"
            for warning in conflicts:
                report += f"{warning}\n"
        
        return report
    
    def __repr__(self) -> str:
        total_tasks = len(self.owner.get_all_tasks())
        return f"📅 Scheduler managing {len(self.owner.get_pets())} pet(s) with {total_tasks} task(s)"
