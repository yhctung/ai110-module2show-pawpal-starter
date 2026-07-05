import pytest
from datetime import datetime, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler, TaskStatus


class TestTaskCompletion:
    """Test that marking a task complete changes its status."""

    def test_mark_complete_changes_status(self):
        """Verify that mark_complete() changes status from PENDING to COMPLETED."""
        task = Task(
            task_id="test_task_1",
            title="Test Task",
            description="A test task",
            duration_minutes=30,
            priority="high",
            frequency="daily",
            pet_id="pet_1",
            due_date=datetime.now(),
            status=TaskStatus.PENDING,
        )

        # Initial state should be PENDING
        assert task.status == TaskStatus.PENDING

        # Call mark_complete
        task.mark_complete()

        # Status should now be COMPLETED
        assert task.status == TaskStatus.COMPLETED

    def test_mark_complete_updates_last_completed(self):
        """Verify that mark_complete() sets the last_completed timestamp."""
        task = Task(
            task_id="test_task_1",
            title="Test Task",
            description="A test task",
            duration_minutes=30,
            priority="high",
            frequency="daily",
            pet_id="pet_1",
            due_date=datetime.now(),
        )

        # Initial state should have no last_completed
        assert task.last_completed is None

        # Call mark_complete
        task.mark_complete()

        # last_completed should now be set
        assert task.last_completed is not None
        assert isinstance(task.last_completed, datetime)


class TestTaskAddition:
    """Test that adding a task to a Pet increases the task count."""

    def test_add_task_increases_task_count(self):
        """Verify that adding a task to a pet increases the task count."""
        pet = Pet(
            pet_id="pet_1",
            name="TestPet",
            species="dog",
            owner_id="owner_1",
        )
        task = Task(
            task_id="test_task_1",
            title="Test Task",
            description="A test task",
            duration_minutes=20,
            priority="medium",
            frequency="daily",
            pet_id="pet_1",
            due_date=datetime.now(),
        )

        # Initial task count should be 0
        assert len(pet.get_tasks()) == 0

        # Add a task
        pet.add_task(task)

        # Task count should now be 1
        assert len(pet.get_tasks()) == 1

    def test_add_multiple_tasks_increments_count(self):
        """Verify that adding multiple tasks increments the task count correctly."""
        pet = Pet(
            pet_id="pet_1",
            name="TestPet",
            species="dog",
            owner_id="owner_1",
        )
        task_1 = Task(
            task_id="test_task_1",
            title="Test Task",
            description="A test task",
            duration_minutes=20,
            priority="medium",
            frequency="daily",
            pet_id="pet_1",
            due_date=datetime.now(),
        )
        task_2 = Task(
            task_id="test_task_2",
            title="Another Task",
            description="Another test task",
            duration_minutes=15,
            priority="low",
            frequency="weekly",
            pet_id="pet_1",
            due_date=datetime.now(),
        )

        # Add first task
        pet.add_task(task_1)
        assert len(pet.get_tasks()) == 1

        # Add second task
        pet.add_task(task_2)

        # Task count should now be 2
        assert len(pet.get_tasks()) == 2

    def test_add_task_with_wrong_pet_id_raises_error(self):
        """Verify that adding a task with mismatched pet_id raises ValueError."""
        pet = Pet(
            pet_id="pet_1",
            name="TestPet",
            species="dog",
            owner_id="owner_1",
        )
        wrong_pet_task = Task(
            task_id="test_task_2",
            title="Wrong Pet Task",
            description="This task belongs to another pet",
            duration_minutes=10,
            priority="high",
            frequency="daily",
            pet_id="pet_2",
            due_date=datetime.now(),
        )

        # Should raise ValueError
        with pytest.raises(ValueError):
            pet.add_task(wrong_pet_task)


class TestSortingCorrectness:
    """Test that tasks are sorted correctly by time, priority, and overdue status."""

    def test_sort_by_time_chronological_order(self):
        """Verify that sort_by_time() returns tasks in chronological order."""
        base_date = datetime(2026, 7, 5, 8, 0)
        owner = Owner(owner_id="owner_1", name="John")
        pet = Pet(pet_id="pet_1", name="Fido", species="dog", owner_id="owner_1")
        owner.add_pet(pet)
        scheduler = Scheduler(scheduler_id="sch_1", owner=owner)

        # Create tasks at different times
        task_9am = Task(
            task_id="task_9am",
            title="Morning Walk",
            description="Walk at 9 AM",
            duration_minutes=30,
            priority="medium",
            frequency="daily",
            pet_id="pet_1",
            due_date=datetime(2026, 7, 5, 9, 0),
        )
        task_2pm = Task(
            task_id="task_2pm",
            title="Afternoon Nap",
            description="Nap at 2 PM",
            duration_minutes=60,
            priority="low",
            frequency="daily",
            pet_id="pet_1",
            due_date=datetime(2026, 7, 5, 14, 0),
        )
        task_5am = Task(
            task_id="task_5am",
            title="Early Breakfast",
            description="Breakfast at 5 AM",
            duration_minutes=15,
            priority="high",
            frequency="daily",
            pet_id="pet_1",
            due_date=datetime(2026, 7, 5, 5, 0),
        )

        tasks = [task_9am, task_2pm, task_5am]
        sorted_tasks = scheduler.sort_by_time(tasks)

        # Should be in chronological order: 5 AM, 9 AM, 2 PM
        assert sorted_tasks[0].due_date.hour == 5
        assert sorted_tasks[1].due_date.hour == 9
        assert sorted_tasks[2].due_date.hour == 14

    def test_sort_by_time_same_hour_different_minutes(self):
        """Verify tasks at the same hour but different minutes are sorted correctly."""
        owner = Owner(owner_id="owner_1", name="John")
        pet = Pet(pet_id="pet_1", name="Fido", species="dog", owner_id="owner_1")
        owner.add_pet(pet)
        scheduler = Scheduler(scheduler_id="sch_1", owner=owner)

        task_930 = Task(
            task_id="task_930",
            title="Task at 9:30",
            description="9:30 AM",
            duration_minutes=20,
            priority="medium",
            frequency="daily",
            pet_id="pet_1",
            due_date=datetime(2026, 7, 5, 9, 30),
        )
        task_915 = Task(
            task_id="task_915",
            title="Task at 9:15",
            description="9:15 AM",
            duration_minutes=20,
            priority="medium",
            frequency="daily",
            pet_id="pet_1",
            due_date=datetime(2026, 7, 5, 9, 15),
        )

        tasks = [task_930, task_915]
        sorted_tasks = scheduler.sort_by_time(tasks)

        # Should be in order: 9:15, 9:30
        assert sorted_tasks[0].due_date.minute == 15
        assert sorted_tasks[1].due_date.minute == 30

    def test_prioritize_tasks_overdue_first(self):
        """Verify that overdue tasks appear first regardless of priority."""
        owner = Owner(owner_id="owner_1", name="John")
        pet = Pet(pet_id="pet_1", name="Fido", species="dog", owner_id="owner_1")
        owner.add_pet(pet)
        scheduler = Scheduler(scheduler_id="sch_1", owner=owner)

        # Overdue low-priority task
        overdue_low = Task(
            task_id="overdue_low",
            title="Overdue Low Priority",
            description="This was due yesterday",
            duration_minutes=20,
            priority="low",
            frequency="daily",
            pet_id="pet_1",
            due_date=datetime.now() - timedelta(days=1),
        )

        # Pending high-priority task
        pending_high = Task(
            task_id="pending_high",
            title="Pending High Priority",
            description="Due tomorrow",
            duration_minutes=30,
            priority="high",
            frequency="daily",
            pet_id="pet_1",
            due_date=datetime.now() + timedelta(days=1),
        )

        tasks = [pending_high, overdue_low]
        prioritized = scheduler.prioritize_tasks(tasks)

        # Overdue should come first even though it's low priority
        assert prioritized[0].task_id == "overdue_low"
        assert prioritized[1].task_id == "pending_high"

    def test_prioritize_tasks_high_priority_before_medium(self):
        """Verify that high-priority pending tasks come before medium-priority pending tasks."""
        owner = Owner(owner_id="owner_1", name="John")
        pet = Pet(pet_id="pet_1", name="Fido", species="dog", owner_id="owner_1")
        owner.add_pet(pet)
        scheduler = Scheduler(scheduler_id="sch_1", owner=owner)

        future_date = datetime.now() + timedelta(hours=2)

        # High-priority task
        high_task = Task(
            task_id="high_task",
            title="High Priority",
            description="Important",
            duration_minutes=30,
            priority="high",
            frequency="daily",
            pet_id="pet_1",
            due_date=future_date,
        )

        # Medium-priority task
        medium_task = Task(
            task_id="medium_task",
            title="Medium Priority",
            description="Less important",
            duration_minutes=20,
            priority="medium",
            frequency="daily",
            pet_id="pet_1",
            due_date=future_date,
        )

        tasks = [medium_task, high_task]
        prioritized = scheduler.prioritize_tasks(tasks)

        # High priority should come first
        assert prioritized[0].task_id == "high_task"
        assert prioritized[1].task_id == "medium_task"


class TestRecurrenceLogic:
    """Test that recurring tasks create next occurrences correctly."""

    def test_daily_task_creates_next_occurrence(self):
        """Verify that marking a daily task complete creates a new task for the next day."""
        owner = Owner(owner_id="owner_1", name="John")
        pet = Pet(pet_id="pet_1", name="Fido", species="dog", owner_id="owner_1")
        owner.add_pet(pet)
        scheduler = Scheduler(scheduler_id="sch_1", owner=owner)

        # Create a daily task
        task = Task(
            task_id="daily_task",
            title="Daily Walk",
            description="Walk every day",
            duration_minutes=30,
            priority="high",
            frequency="daily",
            pet_id="pet_1",
            due_date=datetime(2026, 7, 5, 9, 0),
        )
        pet.add_task(task)

        # Complete the task
        next_task = scheduler.complete_task(task)

        # Verify original task is marked complete
        assert task.status == TaskStatus.COMPLETED

        # Verify next task was created
        assert next_task is not None
        assert next_task.task_id == "daily_task_next"
        assert next_task.title == "Daily Walk"
        assert next_task.frequency == "daily"

        # Verify next task is scheduled for the next day
        assert next_task.due_date == datetime(2026, 7, 6, 9, 0)

        # Verify next task is in PENDING status
        assert next_task.status == TaskStatus.PENDING

        # Verify next task was added to the pet's task list
        assert next_task in pet.get_tasks()

    def test_weekly_task_creates_next_occurrence(self):
        """Verify that marking a weekly task complete creates a new task for the following week."""
        owner = Owner(owner_id="owner_1", name="John")
        pet = Pet(pet_id="pet_1", name="Fido", species="dog", owner_id="owner_1")
        owner.add_pet(pet)
        scheduler = Scheduler(scheduler_id="sch_1", owner=owner)

        # Create a weekly task
        task = Task(
            task_id="weekly_task",
            title="Weekly Grooming",
            description="Groom once a week",
            duration_minutes=60,
            priority="medium",
            frequency="weekly",
            pet_id="pet_1",
            due_date=datetime(2026, 7, 5, 10, 0),
        )
        pet.add_task(task)

        # Complete the task
        next_task = scheduler.complete_task(task)

        # Verify next task was created for the following week
        assert next_task is not None
        assert next_task.due_date == datetime(2026, 7, 12, 10, 0)
        assert next_task.frequency == "weekly"

    def test_one_time_task_creates_no_next_occurrence(self):
        """Verify that marking a one-time task complete does not create a next task."""
        owner = Owner(owner_id="owner_1", name="John")
        pet = Pet(pet_id="pet_1", name="Fido", species="dog", owner_id="owner_1")
        owner.add_pet(pet)
        scheduler = Scheduler(scheduler_id="sch_1", owner=owner)

        # Create a one-time task
        task = Task(
            task_id="one_time",
            title="Vet Appointment",
            description="One-time visit",
            duration_minutes=45,
            priority="high",
            frequency="once",
            pet_id="pet_1",
            due_date=datetime(2026, 7, 8, 14, 0),
        )
        pet.add_task(task)

        # Complete the task
        next_task = scheduler.complete_task(task)

        # Verify no next task was created
        assert next_task is None

    def test_recurring_task_chain(self):
        """Verify that multiple occurrences of a daily task can be created in sequence."""
        owner = Owner(owner_id="owner_1", name="John")
        pet = Pet(pet_id="pet_1", name="Fido", species="dog", owner_id="owner_1")
        owner.add_pet(pet)
        scheduler = Scheduler(scheduler_id="sch_1", owner=owner)

        # Create initial daily task
        task1 = Task(
            task_id="daily_task",
            title="Meal",
            description="Feed the dog",
            duration_minutes=15,
            priority="high",
            frequency="daily",
            pet_id="pet_1",
            due_date=datetime(2026, 7, 5, 8, 0),
        )
        pet.add_task(task1)

        # Complete first task, get second
        task2 = scheduler.complete_task(task1)
        assert task2.due_date.day == 6

        # Complete second task, get third
        task3 = scheduler.complete_task(task2)
        assert task3.due_date.day == 7

        # Verify all are in pet's task list
        assert len(pet.get_tasks()) == 3


class TestConflictDetection:
    """Test that the scheduler correctly detects conflicting task times."""

    def test_detect_overlapping_tasks_same_pet(self):
        """Verify that overlapping tasks for the same pet are flagged as conflicts."""
        owner = Owner(owner_id="owner_1", name="John")
        pet = Pet(pet_id="pet_1", name="Fido", species="dog", owner_id="owner_1")
        owner.add_pet(pet)
        scheduler = Scheduler(scheduler_id="sch_1", owner=owner)

        # Create two overlapping tasks
        task1 = Task(
            task_id="task1",
            title="Walk",
            description="Morning walk",
            duration_minutes=30,
            priority="high",
            frequency="daily",
            pet_id="pet_1",
            due_date=datetime(2026, 7, 5, 9, 0),
        )
        task2 = Task(
            task_id="task2",
            title="Training",
            description="Training session",
            duration_minutes=30,
            priority="medium",
            frequency="daily",
            pet_id="pet_1",
            due_date=datetime(2026, 7, 5, 9, 15),
        )
        pet.add_task(task1)
        pet.add_task(task2)

        # Detect conflicts
        conflicts = scheduler.detect_conflicts(datetime(2026, 7, 5, 9, 0))

        # Should detect one conflict
        assert len(conflicts) == 1
        assert "CONFLICT" in conflicts[0]
        assert "Walk" in conflicts[0]
        assert "Training" in conflicts[0]

    def test_no_conflict_adjacent_times(self):
        """Verify that tasks ending exactly when another starts are not flagged as conflicts."""
        owner = Owner(owner_id="owner_1", name="John")
        pet = Pet(pet_id="pet_1", name="Fido", species="dog", owner_id="owner_1")
        owner.add_pet(pet)
        scheduler = Scheduler(scheduler_id="sch_1", owner=owner)

        # Create adjacent tasks (one ends at 9:30, next starts at 9:30)
        task1 = Task(
            task_id="task1",
            title="Walk",
            description="9:00-9:30",
            duration_minutes=30,
            priority="high",
            frequency="daily",
            pet_id="pet_1",
            due_date=datetime(2026, 7, 5, 9, 0),
        )
        task2 = Task(
            task_id="task2",
            title="Feeding",
            description="9:30-10:00",
            duration_minutes=30,
            priority="high",
            frequency="daily",
            pet_id="pet_1",
            due_date=datetime(2026, 7, 5, 9, 30),
        )
        pet.add_task(task1)
        pet.add_task(task2)

        # Detect conflicts
        conflicts = scheduler.detect_conflicts(datetime(2026, 7, 5, 9, 0))

        # Should NOT detect a conflict (adjacent is allowed)
        assert len(conflicts) == 0

    def test_no_conflict_different_pets(self):
        """Verify that overlapping tasks for different pets are not flagged as conflicts."""
        owner = Owner(owner_id="owner_1", name="John")
        pet1 = Pet(pet_id="pet_1", name="Fido", species="dog", owner_id="owner_1")
        pet2 = Pet(pet_id="pet_2", name="Whiskers", species="cat", owner_id="owner_1")
        owner.add_pet(pet1)
        owner.add_pet(pet2)
        scheduler = Scheduler(scheduler_id="sch_1", owner=owner)

        # Create overlapping tasks for different pets
        task1 = Task(
            task_id="task1",
            title="Dog Walk",
            description="Walk the dog",
            duration_minutes=30,
            priority="high",
            frequency="daily",
            pet_id="pet_1",
            due_date=datetime(2026, 7, 5, 9, 0),
        )
        task2 = Task(
            task_id="task2",
            title="Cat Play",
            description="Play with cat",
            duration_minutes=30,
            priority="medium",
            frequency="daily",
            pet_id="pet_2",
            due_date=datetime(2026, 7, 5, 9, 0),
        )
        pet1.add_task(task1)
        pet2.add_task(task2)

        # Detect conflicts
        conflicts = scheduler.detect_conflicts(datetime(2026, 7, 5, 9, 0))

        # Should NOT detect a conflict (different pets)
        assert len(conflicts) == 0

    def test_detect_multiple_conflicts(self):
        """Verify that multiple conflicts are all detected."""
        owner = Owner(owner_id="owner_1", name="John")
        pet = Pet(pet_id="pet_1", name="Fido", species="dog", owner_id="owner_1")
        owner.add_pet(pet)
        scheduler = Scheduler(scheduler_id="sch_1", owner=owner)

        # Create three tasks where task1 overlaps with task2 and task3
        task1 = Task(
            task_id="task1",
            title="Long Walk",
            description="9:00-10:00",
            duration_minutes=60,
            priority="high",
            frequency="daily",
            pet_id="pet_1",
            due_date=datetime(2026, 7, 5, 9, 0),
        )
        task2 = Task(
            task_id="task2",
            title="Training",
            description="9:30-10:30",
            duration_minutes=60,
            priority="medium",
            frequency="daily",
            pet_id="pet_1",
            due_date=datetime(2026, 7, 5, 9, 30),
        )
        task3 = Task(
            task_id="task3",
            title="Playtime",
            description="9:45-10:45",
            duration_minutes=60,
            priority="low",
            frequency="daily",
            pet_id="pet_1",
            due_date=datetime(2026, 7, 5, 9, 45),
        )
        pet.add_task(task1)
        pet.add_task(task2)
        pet.add_task(task3)

        # Detect conflicts
        conflicts = scheduler.detect_conflicts(datetime(2026, 7, 5, 9, 0))

        # Should detect three conflicts: task1 vs task2, task1 vs task3, and task2 vs task3
        assert len(conflicts) == 3

    def test_no_conflict_different_dates(self):
        """Verify that overlapping tasks on different dates are not flagged as conflicts."""
        owner = Owner(owner_id="owner_1", name="John")
        pet = Pet(pet_id="pet_1", name="Fido", species="dog", owner_id="owner_1")
        owner.add_pet(pet)
        scheduler = Scheduler(scheduler_id="sch_1", owner=owner)

        # Create overlapping tasks on different dates
        task1 = Task(
            task_id="task1",
            title="Walk",
            description="July 5",
            duration_minutes=30,
            priority="high",
            frequency="daily",
            pet_id="pet_1",
            due_date=datetime(2026, 7, 5, 9, 0),
        )
        task2 = Task(
            task_id="task2",
            title="Walk",
            description="July 6",
            duration_minutes=30,
            priority="high",
            frequency="daily",
            pet_id="pet_1",
            due_date=datetime(2026, 7, 6, 9, 0),
        )
        pet.add_task(task1)
        pet.add_task(task2)

        # Detect conflicts for July 5
        conflicts = scheduler.detect_conflicts(datetime(2026, 7, 5, 9, 0))

        # Should NOT detect a conflict (different dates)
        assert len(conflicts) == 0


class TestEdgeCasesEmptyStates:
    """Test scheduler behavior with empty or missing data."""

    def test_empty_pet_no_tasks_schedule(self):
        """Verify that generate_schedule() handles pet with zero tasks."""
        owner = Owner(owner_id="owner_1", name="John")
        pet = Pet(pet_id="pet_1", name="Fido", species="dog", owner_id="owner_1")
        owner.add_pet(pet)
        scheduler = Scheduler(scheduler_id="sch_1", owner=owner)

        # Generate schedule for empty pet
        schedule = scheduler.generate_schedule(datetime(2026, 7, 5, 9, 0))

        # Should return empty task list and appropriate summary
        assert schedule["task_count"] == 0
        assert schedule["tasks"] == []
        assert "No tasks scheduled" in schedule["summary"]
        assert schedule["total_duration_minutes"] == 0

    def test_owner_with_no_pets_returns_empty_tasks(self):
        """Verify that get_all_tasks() returns empty list when owner has no pets."""
        owner = Owner(owner_id="owner_1", name="John")
        scheduler = Scheduler(scheduler_id="sch_1", owner=owner)

        # Get all tasks from owner with no pets
        all_tasks = owner.get_all_tasks()

        # Should return empty list, not None
        assert all_tasks == []
        assert isinstance(all_tasks, list)

    def test_filter_by_nonexistent_pet_name(self):
        """Verify that filtering by non-existent pet name returns all tasks (no filtering applied)."""
        owner = Owner(owner_id="owner_1", name="John")
        pet = Pet(pet_id="pet_1", name="Fido", species="dog", owner_id="owner_1")
        owner.add_pet(pet)
        scheduler = Scheduler(scheduler_id="sch_1", owner=owner)

        task = Task(
            task_id="task1",
            title="Walk",
            description="Walk Fido",
            duration_minutes=30,
            priority="high",
            frequency="daily",
            pet_id="pet_1",
            due_date=datetime(2026, 7, 5, 9, 0),
        )
        pet.add_task(task)

        # Filter by non-existent pet name
        all_tasks = owner.get_all_tasks()
        filtered = scheduler.filter_tasks(all_tasks, pet_name="NonExistent")

        # When pet doesn't exist, no filter is applied, so all tasks are returned
        assert len(filtered) == 1
        assert filtered == all_tasks

    def test_filter_by_unknown_status(self):
        """Verify that filtering by unknown status returns empty list."""
        owner = Owner(owner_id="owner_1", name="John")
        pet = Pet(pet_id="pet_1", name="Fido", species="dog", owner_id="owner_1")
        owner.add_pet(pet)
        scheduler = Scheduler(scheduler_id="sch_1", owner=owner)

        task = Task(
            task_id="task1",
            title="Walk",
            description="Walk Fido",
            duration_minutes=30,
            priority="high",
            frequency="daily",
            pet_id="pet_1",
            due_date=datetime(2026, 7, 5, 9, 0),
        )
        pet.add_task(task)

        # Filter by unknown status
        filtered = scheduler.filter_tasks(owner.get_all_tasks(), status="unknown")

        # Should return empty list
        assert filtered == []

    def test_aggregate_tasks_across_multiple_pets(self):
        """Verify that get_all_tasks() correctly aggregates from multiple pets."""
        owner = Owner(owner_id="owner_1", name="John")
        pet1 = Pet(pet_id="pet_1", name="Fido", species="dog", owner_id="owner_1")
        pet2 = Pet(pet_id="pet_2", name="Whiskers", species="cat", owner_id="owner_1")
        owner.add_pet(pet1)
        owner.add_pet(pet2)

        task1 = Task(
            task_id="task1",
            title="Dog Walk",
            description="Walk dog",
            duration_minutes=30,
            priority="high",
            frequency="daily",
            pet_id="pet_1",
            due_date=datetime(2026, 7, 5, 9, 0),
        )
        task2 = Task(
            task_id="task2",
            title="Cat Feed",
            description="Feed cat",
            duration_minutes=15,
            priority="high",
            frequency="daily",
            pet_id="pet_2",
            due_date=datetime(2026, 7, 5, 8, 0),
        )
        task3 = Task(
            task_id="task3",
            title="Dog Groom",
            description="Groom dog",
            duration_minutes=60,
            priority="medium",
            frequency="weekly",
            pet_id="pet_1",
            due_date=datetime(2026, 7, 5, 14, 0),
        )
        pet1.add_task(task1)
        pet2.add_task(task2)
        pet1.add_task(task3)

        # Get all tasks
        all_tasks = owner.get_all_tasks()

        # Should have 3 tasks total
        assert len(all_tasks) == 3
        # Should include tasks from both pets
        assert any(t.pet_id == "pet_1" for t in all_tasks)
        assert any(t.pet_id == "pet_2" for t in all_tasks)


class TestEdgeCasesSortingBoundaries:
    """Test sorting edge cases at time boundaries."""

    def test_tasks_at_exact_midnight(self):
        """Verify that tasks at 00:00 sort correctly with other times."""
        owner = Owner(owner_id="owner_1", name="John")
        pet = Pet(pet_id="pet_1", name="Fido", species="dog", owner_id="owner_1")
        owner.add_pet(pet)
        scheduler = Scheduler(scheduler_id="sch_1", owner=owner)

        task_midnight = Task(
            task_id="midnight",
            title="Midnight Task",
            description="At midnight",
            duration_minutes=30,
            priority="medium",
            frequency="daily",
            pet_id="pet_1",
            due_date=datetime(2026, 7, 5, 0, 0),
        )
        task_morning = Task(
            task_id="morning",
            title="Morning Task",
            description="At 6 AM",
            duration_minutes=30,
            priority="medium",
            frequency="daily",
            pet_id="pet_1",
            due_date=datetime(2026, 7, 5, 6, 0),
        )
        task_evening = Task(
            task_id="evening",
            title="Evening Task",
            description="At 11:59 PM",
            duration_minutes=30,
            priority="medium",
            frequency="daily",
            pet_id="pet_1",
            due_date=datetime(2026, 7, 5, 23, 59),
        )

        tasks = [task_evening, task_midnight, task_morning]
        sorted_tasks = scheduler.sort_by_time(tasks)

        # Should be ordered: midnight (0:00), morning (6:00), evening (23:59)
        assert sorted_tasks[0].due_date.hour == 0
        assert sorted_tasks[1].due_date.hour == 6
        assert sorted_tasks[2].due_date.hour == 23

    def test_two_tasks_exact_same_time(self):
        """Verify that tasks at exact same time maintain stable order."""
        owner = Owner(owner_id="owner_1", name="John")
        pet = Pet(pet_id="pet_1", name="Fido", species="dog", owner_id="owner_1")
        owner.add_pet(pet)
        scheduler = Scheduler(scheduler_id="sch_1", owner=owner)

        task1 = Task(
            task_id="task1",
            title="First Task",
            description="Same time",
            duration_minutes=30,
            priority="high",
            frequency="daily",
            pet_id="pet_1",
            due_date=datetime(2026, 7, 5, 9, 0),
        )
        task2 = Task(
            task_id="task2",
            title="Second Task",
            description="Same time",
            duration_minutes=30,
            priority="high",
            frequency="daily",
            pet_id="pet_1",
            due_date=datetime(2026, 7, 5, 9, 0),
        )

        tasks = [task1, task2]
        sorted_tasks = scheduler.sort_by_time(tasks)

        # Both should have same time
        assert sorted_tasks[0].due_date == sorted_tasks[1].due_date
        # Order should be preserved (stable sort)
        assert sorted_tasks[0].task_id == "task1"
        assert sorted_tasks[1].task_id == "task2"

    def test_unknown_priority_sorts_last(self):
        """Verify that tasks with unknown priority sort after known priorities."""
        owner = Owner(owner_id="owner_1", name="John")
        pet = Pet(pet_id="pet_1", name="Fido", species="dog", owner_id="owner_1")
        owner.add_pet(pet)
        scheduler = Scheduler(scheduler_id="sch_1", owner=owner)

        future_date = datetime.now() + timedelta(hours=2)

        high_task = Task(
            task_id="high",
            title="High Priority",
            description="Known priority",
            duration_minutes=30,
            priority="high",
            frequency="daily",
            pet_id="pet_1",
            due_date=future_date,
        )
        unknown_task = Task(
            task_id="unknown",
            title="Unknown Priority",
            description="Unknown priority",
            duration_minutes=30,
            priority="urgent",  # Not in priority_order dict
            frequency="daily",
            pet_id="pet_1",
            due_date=future_date,
        )

        tasks = [unknown_task, high_task]
        prioritized = scheduler.prioritize_tasks(tasks)

        # High priority should come before unknown priority
        assert prioritized[0].task_id == "high"
        assert prioritized[1].task_id == "unknown"


class TestEdgeCasesConflictDetection:
    """Test conflict detection edge cases."""

    def test_two_tasks_exact_same_start_time(self):
        """Verify that two tasks starting at exact same time are flagged as conflicts."""
        owner = Owner(owner_id="owner_1", name="John")
        pet = Pet(pet_id="pet_1", name="Fido", species="dog", owner_id="owner_1")
        owner.add_pet(pet)
        scheduler = Scheduler(scheduler_id="sch_1", owner=owner)

        task1 = Task(
            task_id="task1",
            title="Task A",
            description="Starts at 9:00",
            duration_minutes=30,
            priority="high",
            frequency="daily",
            pet_id="pet_1",
            due_date=datetime(2026, 7, 5, 9, 0),
        )
        task2 = Task(
            task_id="task2",
            title="Task B",
            description="Also starts at 9:00",
            duration_minutes=30,
            priority="high",
            frequency="daily",
            pet_id="pet_1",
            due_date=datetime(2026, 7, 5, 9, 0),
        )
        pet.add_task(task1)
        pet.add_task(task2)

        conflicts = scheduler.detect_conflicts(datetime(2026, 7, 5, 9, 0))

        # Should detect conflict (both 9:00-9:30)
        assert len(conflicts) == 1

    def test_task_completely_contains_another(self):
        """Verify that a task completely containing another is flagged as conflict."""
        owner = Owner(owner_id="owner_1", name="John")
        pet = Pet(pet_id="pet_1", name="Fido", species="dog", owner_id="owner_1")
        owner.add_pet(pet)
        scheduler = Scheduler(scheduler_id="sch_1", owner=owner)

        outer_task = Task(
            task_id="outer",
            title="Long Activity",
            description="9:00-11:00",
            duration_minutes=120,
            priority="high",
            frequency="daily",
            pet_id="pet_1",
            due_date=datetime(2026, 7, 5, 9, 0),
        )
        inner_task = Task(
            task_id="inner",
            title="Short Activity",
            description="9:30-10:30",
            duration_minutes=60,
            priority="high",
            frequency="daily",
            pet_id="pet_1",
            due_date=datetime(2026, 7, 5, 9, 30),
        )
        pet.add_task(outer_task)
        pet.add_task(inner_task)

        conflicts = scheduler.detect_conflicts(datetime(2026, 7, 5, 9, 0))

        # Should detect conflict (inner is inside outer)
        assert len(conflicts) == 1

    def test_overlap_by_one_minute(self):
        """Verify that overlapping by 1 minute is flagged as conflict."""
        owner = Owner(owner_id="owner_1", name="John")
        pet = Pet(pet_id="pet_1", name="Fido", species="dog", owner_id="owner_1")
        owner.add_pet(pet)
        scheduler = Scheduler(scheduler_id="sch_1", owner=owner)

        task1 = Task(
            task_id="task1",
            title="Task 1",
            description="9:00-9:31",
            duration_minutes=31,
            priority="high",
            frequency="daily",
            pet_id="pet_1",
            due_date=datetime(2026, 7, 5, 9, 0),
        )
        task2 = Task(
            task_id="task2",
            title="Task 2",
            description="9:30-10:00",
            duration_minutes=30,
            priority="high",
            frequency="daily",
            pet_id="pet_1",
            due_date=datetime(2026, 7, 5, 9, 30),
        )
        pet.add_task(task1)
        pet.add_task(task2)

        conflicts = scheduler.detect_conflicts(datetime(2026, 7, 5, 9, 0))

        # Should detect conflict (overlap by 1 minute: 9:30-9:31)
        assert len(conflicts) == 1


class TestEdgeCasesRecurrence:
    """Test recurrence logic edge cases."""

    def test_unknown_frequency_returns_none(self):
        """Verify that task with unknown frequency returns None for next occurrence."""
        task = Task(
            task_id="task1",
            title="Task",
            description="Unknown frequency",
            duration_minutes=30,
            priority="high",
            frequency="monthly",  # Not "daily" or "weekly"
            pet_id="pet_1",
            due_date=datetime(2026, 7, 5, 9, 0),
        )

        # Try to create next occurrence
        next_task = task.create_next_occurrence()

        # Should return None for unknown frequency
        assert next_task is None

    def test_recurring_task_with_zero_duration(self):
        """Verify that zero-duration recurring tasks still create next occurrence."""
        owner = Owner(owner_id="owner_1", name="John")
        pet = Pet(pet_id="pet_1", name="Fido", species="dog", owner_id="owner_1")
        owner.add_pet(pet)
        scheduler = Scheduler(scheduler_id="sch_1", owner=owner)

        task = Task(
            task_id="zero_duration",
            title="Instant Task",
            description="0 minutes",
            duration_minutes=0,
            priority="high",
            frequency="daily",
            pet_id="pet_1",
            due_date=datetime(2026, 7, 5, 9, 0),
        )
        pet.add_task(task)

        next_task = scheduler.complete_task(task)

        # Should create next occurrence despite 0 duration
        assert next_task is not None
        assert next_task.duration_minutes == 0
        assert next_task.due_date.day == 6

    def test_schedule_summary_with_all_low_priority(self):
        """Verify schedule summary correctly counts high-priority tasks when none exist."""
        owner = Owner(owner_id="owner_1", name="John")
        pet = Pet(pet_id="pet_1", name="Fido", species="dog", owner_id="owner_1")
        owner.add_pet(pet)
        scheduler = Scheduler(scheduler_id="sch_1", owner=owner)

        task1 = Task(
            task_id="task1",
            title="Low Priority 1",
            description="Low",
            duration_minutes=30,
            priority="low",
            frequency="daily",
            pet_id="pet_1",
            due_date=datetime(2026, 7, 5, 9, 0),
        )
        task2 = Task(
            task_id="task2",
            title="Low Priority 2",
            description="Low",
            duration_minutes=20,
            priority="low",
            frequency="daily",
            pet_id="pet_1",
            due_date=datetime(2026, 7, 5, 10, 0),
        )
        pet.add_task(task1)
        pet.add_task(task2)

        schedule = scheduler.generate_schedule(datetime(2026, 7, 5, 9, 0))

        # Summary should say 0 high priority tasks
        assert "High priority: 0" in schedule["summary"]
        assert schedule["task_count"] == 2
        assert schedule["total_duration_minutes"] == 50

    def test_filter_completed_tasks(self):
        """Verify that filtering by 'completed' status returns only completed tasks."""
        owner = Owner(owner_id="owner_1", name="John")
        pet = Pet(pet_id="pet_1", name="Fido", species="dog", owner_id="owner_1")
        owner.add_pet(pet)
        scheduler = Scheduler(scheduler_id="sch_1", owner=owner)

        task1 = Task(
            task_id="task1",
            title="Completed Task",
            description="Done",
            duration_minutes=30,
            priority="high",
            frequency="daily",
            pet_id="pet_1",
            due_date=datetime(2026, 7, 5, 9, 0),
        )
        task2 = Task(
            task_id="task2",
            title="Pending Task",
            description="Not done",
            duration_minutes=30,
            priority="high",
            frequency="daily",
            pet_id="pet_1",
            due_date=datetime(2026, 7, 5, 10, 0),
        )
        pet.add_task(task1)
        pet.add_task(task2)

        # Mark first task as completed
        task1.mark_complete()

        # Filter by completed
        completed = scheduler.filter_tasks(owner.get_all_tasks(), status="completed")

        # Should only have 1 completed task
        assert len(completed) == 1
        assert completed[0].task_id == "task1"
        assert completed[0].status == TaskStatus.COMPLETED

    def test_filter_pending_tasks(self):
        """Verify that filtering by 'pending' status returns only pending tasks."""
        owner = Owner(owner_id="owner_1", name="John")
        pet = Pet(pet_id="pet_1", name="Fido", species="dog", owner_id="owner_1")
        owner.add_pet(pet)
        scheduler = Scheduler(scheduler_id="sch_1", owner=owner)

        task1 = Task(
            task_id="task1",
            title="Completed Task",
            description="Done",
            duration_minutes=30,
            priority="high",
            frequency="daily",
            pet_id="pet_1",
            due_date=datetime(2026, 7, 5, 9, 0),
        )
        task2 = Task(
            task_id="task2",
            title="Pending Task",
            description="Not done",
            duration_minutes=30,
            priority="high",
            frequency="daily",
            pet_id="pet_1",
            due_date=datetime(2026, 7, 5, 10, 0),
        )
        pet.add_task(task1)
        pet.add_task(task2)

        # Mark first task as completed
        task1.mark_complete()

        # Filter by pending
        pending = scheduler.filter_tasks(owner.get_all_tasks(), status="pending")

        # Should only have 1 pending task
        assert len(pending) == 1
        assert pending[0].task_id == "task2"
        assert pending[0].status == TaskStatus.PENDING
