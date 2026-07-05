from dataclasses import dataclass, field
from typing import List
from datetime import datetime, timedelta
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

    def create_next_occurrence(self) -> 'Task':
        """Create a new task instance for the next occurrence (daily or weekly)."""
        if self.frequency not in ("daily", "weekly"):
            return None

        next_due_date = self.due_date
        if self.frequency == "daily":
            next_due_date = self.due_date + timedelta(days=1)
        elif self.frequency == "weekly":
            next_due_date = self.due_date + timedelta(weeks=1)

        new_task = Task(
            task_id=f"{self.task_id}_next",
            title=self.title,
            description=self.description,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            frequency=self.frequency,
            pet_id=self.pet_id,
            due_date=next_due_date,
            status=TaskStatus.PENDING,
        )
        return new_task

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
    owner_id: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to the pet's task list."""
        if task.pet_id != self.pet_id:
            raise ValueError(f"Task {task.task_id} does not belong to pet {self.pet_id}")
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        """Return the list of tasks for this pet."""
        return self.tasks


@dataclass
class Owner:
    """Manages multiple pets and provides access to all their tasks."""
    owner_id: str
    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's pet list."""
        if pet.owner_id != self.owner_id:
            raise ValueError(f"Pet {pet.pet_id} does not belong to owner {self.owner_id}")
        self.pets.append(pet)

    def get_pets(self) -> List[Pet]:
        """Return the list of pets owned by this owner."""
        return self.pets

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks across all pets."""
        return [t for pet in self.pets for t in pet.get_tasks()]


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
        """Sort and prioritize tasks by due date (overdue first, then soonest due)."""
        def sort_key(task):
            is_overdue = 0 if task.is_overdue() else 1
            return (is_overdue, task.due_date if task.due_date else datetime.max)

        return sorted(tasks, key=sort_key)

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks chronologically by their due_date time (HH:MM)."""
        return sorted(tasks, key=lambda task: (task.due_date.hour, task.due_date.minute) if task.due_date else (23, 59))

    def filter_tasks(self, tasks: List[Task], status: str = None, pet_name: str = None) -> List[Task]:
        """Filter tasks by completion status or pet name."""
        filtered = tasks

        if status:
            filtered = [t for t in filtered if t.status.value == status]

        if pet_name:
            pet_id = next((p.pet_id for p in self.owner.get_pets() if p.name == pet_name), None)
            if pet_id:
                filtered = [t for t in filtered if t.pet_id == pet_id]

        return filtered

    def complete_task(self, task: Task) -> Task:
        """Mark a task as complete and create next occurrence if recurring. Returns the next task instance or None."""
        task.mark_complete()
        next_task = task.create_next_occurrence()

        if next_task:
            pet = next((p for p in self.owner.get_pets() if p.pet_id == task.pet_id), None)
            if pet:
                pet.add_task(next_task)
            return next_task

        return None

    def detect_conflicts(self, date: datetime) -> list:
        """Detect overlapping tasks for the same pet on the same day. Returns list of conflict warnings."""
        scheduled_tasks = self._get_tasks_for_date(date)
        conflicts = []

        for i, task1 in enumerate(scheduled_tasks):
            for task2 in scheduled_tasks[i + 1:]:
                if task1.pet_id != task2.pet_id:
                    continue

                start1 = task1.due_date
                end1 = task1.due_date + timedelta(minutes=task1.duration_minutes)
                start2 = task2.due_date
                end2 = task2.due_date + timedelta(minutes=task2.duration_minutes)

                if start1 < end2 and start2 < end1:
                    pet_name = next((p.name for p in self.owner.get_pets() if p.pet_id == task1.pet_id), "Unknown")
                    warning = f"⚠️  CONFLICT: '{task1.title}' ({start1.strftime('%H:%M')}-{end1.strftime('%H:%M')}) overlaps with '{task2.title}' ({start2.strftime('%H:%M')}-{end2.strftime('%H:%M')}) for {pet_name}"
                    conflicts.append(warning)

        return conflicts

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
