from dataclasses import dataclass, field
from typing import List
from datetime import datetime
from enum import Enum


class TaskStatus(Enum):
    """Task completion status."""
    PENDING = "pending"
    COMPLETED = "completed"


@dataclass
class Task:
    """Represents a single pet care activity."""
    task_id: str
    title: str
    description: str
    duration_minutes: int
    priority: str
    frequency: str
    pet_id: str
    due_date: datetime
    status: TaskStatus = TaskStatus.PENDING
    last_completed: datetime = None

    def get_details(self) -> dict:
        """Return task details as a dictionary."""
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "duration_minutes": self.duration_minutes,
            "priority": self.priority,
            "frequency": self.frequency,
            "pet_id": self.pet_id,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "status": self.status.value,
            "last_completed": self.last_completed.isoformat() if self.last_completed else None,
        }

    def mark_complete(self) -> None:
        """Mark the task as completed and update last_completed timestamp."""
        self.status = TaskStatus.COMPLETED
        self.last_completed = datetime.now()

    def update_priority(self, priority: str) -> None:
        """Update the task priority."""
        self.priority = priority

    def is_overdue(self) -> bool:
        """Check if task is past due date and not completed."""
        if self.status == TaskStatus.COMPLETED:
            return False
        return datetime.now() > self.due_date if self.due_date else False


@dataclass
class Pet:
    """Stores pet details and manages a list of tasks."""
    pet_id: str
    name: str
    species: str
    age: int
    owner_id: str
    health_notes: str = ""
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to the pet's task list."""
        if task.pet_id != self.pet_id:
            raise ValueError(f"Task {task.task_id} does not belong to pet {self.pet_id}")
        self.tasks.append(task)

    def remove_task(self, task_id: str) -> None:
        """Remove a task from the pet's task list by ID."""
        self.tasks = [t for t in self.tasks if t.task_id != task_id]

    def _filter_tasks(self, predicate) -> List[Task]:
        """Filter tasks by a predicate function."""
        return [t for t in self.tasks if predicate(t)]

    def get_tasks(self) -> List[Task]:
        """Return the list of tasks for this pet."""
        return self.tasks

    def get_tasks_by_priority(self, priority: str) -> List[Task]:
        """Return tasks filtered by priority level."""
        return self._filter_tasks(lambda t: t.priority == priority)

    def get_overdue_tasks(self) -> List[Task]:
        """Return all overdue tasks for this pet."""
        return self._filter_tasks(lambda t: t.is_overdue())

    def get_info(self) -> dict:
        """Return pet information as a dictionary."""
        return {
            "pet_id": self.pet_id,
            "name": self.name,
            "species": self.species,
            "age": self.age,
            "owner_id": self.owner_id,
            "health_notes": self.health_notes,
            "task_count": len(self.tasks),
        }


@dataclass
class Owner:
    """Manages multiple pets and provides access to all their tasks."""
    owner_id: str
    name: str
    email: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's pet list."""
        if pet.owner_id != self.owner_id:
            raise ValueError(f"Pet {pet.pet_id} does not belong to owner {self.owner_id}")
        self.pets.append(pet)

    def remove_pet(self, pet_id: str) -> None:
        """Remove a pet from the owner's pet list by ID."""
        self.pets = [p for p in self.pets if p.pet_id != pet_id]

    def get_pets(self) -> List[Pet]:
        """Return the list of pets owned by this owner."""
        return self.pets

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks across all pets."""
        return [t for pet in self.pets for t in pet.get_tasks()]

    def get_all_tasks_by_priority(self, priority: str) -> List[Task]:
        """Return all tasks across all pets filtered by priority."""
        return [t for t in self.get_all_tasks() if t.priority == priority]

    def get_all_overdue_tasks(self) -> List[Task]:
        """Return all overdue tasks across all pets."""
        return [t for t in self.get_all_tasks() if t.is_overdue()]


class Scheduler:
    """The 'brain' that retrieves, organizes, and manages tasks across pets."""

    def __init__(self, scheduler_id: str, owner: Owner):
        """Initialize the scheduler with an owner."""
        self.scheduler_id = scheduler_id
        self.owner = owner

    def _get_tasks_for_date(self, date: datetime) -> List[Task]:
        """Get all tasks scheduled for a specific date."""
        return [t for t in self.owner.get_all_tasks() if t.due_date.date() == date.date()]

    def generate_schedule(self, date: datetime) -> dict:
        """Generate a schedule for a given date."""
        scheduled_tasks = self._get_tasks_for_date(date)
        organized = self.prioritize_tasks(scheduled_tasks)
        total_duration = sum(t.duration_minutes for t in organized)

        return {
            "date": date.date().isoformat(),
            "tasks": [t.get_details() for t in organized],
            "total_duration_minutes": total_duration,
            "task_count": len(organized),
            "summary": self.get_schedule_summary(date),
        }

    def prioritize_tasks(self, tasks: List[Task]) -> List[Task]:
        """Sort and prioritize tasks based on priority and frequency."""
        priority_order = {"high": 0, "medium": 1, "low": 2}

        def sort_key(task):
            priority_value = priority_order.get(task.priority, 3)
            is_overdue = 0 if task.is_overdue() else 1
            return (is_overdue, priority_value, task.due_date if task.due_date else datetime.max)

        return sorted(tasks, key=sort_key)

    def get_schedule_summary(self, date: datetime) -> str:
        """Return a summary of the schedule for a given date."""
        scheduled_tasks = self._get_tasks_for_date(date)

        if not scheduled_tasks:
            return f"No tasks scheduled for {date.date().isoformat()}"

        high_priority = [t for t in scheduled_tasks if t.priority == "high"]
        total_duration = sum(t.duration_minutes for t in scheduled_tasks)

        summary = f"Scheduled {len(scheduled_tasks)} task(s) for {date.date().isoformat()}. "
        summary += f"Total duration: {total_duration} minutes. "
        summary += f"High priority: {len(high_priority)} task(s)."

        return summary
