import pytest
from datetime import datetime
from pawpal_system import Task, Pet, Owner, TaskStatus


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
            age=5,
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
            age=5,
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

    def test_pet_info_reflects_task_count(self):
        """Verify that pet.get_info() returns the correct task count."""
        pet = Pet(
            pet_id="pet_1",
            name="TestPet",
            species="dog",
            age=5,
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

        # Add a task
        pet.add_task(task)

        # Get pet info
        pet_info = pet.get_info()

        # Task count in info should match actual task count
        assert pet_info["task_count"] == 1
        assert pet_info["task_count"] == len(pet.get_tasks())

    def test_add_task_with_wrong_pet_id_raises_error(self):
        """Verify that adding a task with mismatched pet_id raises ValueError."""
        pet = Pet(
            pet_id="pet_1",
            name="TestPet",
            species="dog",
            age=5,
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
