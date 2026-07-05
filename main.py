import sys
from datetime import datetime, timedelta
from pawpal_system import Owner, Pet, Task, TaskStatus, Scheduler

sys.stdout.reconfigure(encoding='utf-8')


def main():
    """Demo: Create owner, pets, tasks, and generate today's schedule."""

    # Create an Owner
    owner = Owner(
        owner_id="owner_1",
        name="Ryan",
    )

    # Create two Pets
    mochi = Pet(
        pet_id="pet_1",
        name="Mochi",
        species="dog",
        owner_id="owner_1",
    )

    dave = Pet(
        pet_id="pet_2",
        name="Dave",
        species="cat",
        owner_id="owner_1",
    )

    # Add pets to owner
    owner.add_pet(mochi)
    owner.add_pet(dave)

    # Get today and create tasks with different times (added out of order)
    today = datetime.now()

    # Task 4: Grooming for Dave - 4:00 PM
    grooming = Task(
        task_id="task_4",
        title="Brush Dave",
        description="Brush Dave's fur to prevent matting",
        duration_minutes=15,
        priority="low",
        frequency="3-times-a-week",
        pet_id="pet_2",
        due_date=today.replace(hour=16, minute=0),
        status=TaskStatus.PENDING,
    )

    # Task 1: Morning walk for Mochi - 8:00 AM
    morning_walk = Task(
        task_id="task_1",
        title="Morning Walk",
        description="Take Mochi for a 30-minute walk in the park",
        duration_minutes=30,
        priority="high",
        frequency="daily",
        pet_id="pet_1",
        due_date=today.replace(hour=8, minute=0),
        status=TaskStatus.PENDING,
    )

    # Task 3: Afternoon playtime for Mochi - 2:30 PM
    afternoon_play = Task(
        task_id="task_3",
        title="Afternoon Playtime",
        description="Play fetch with Mochi in the backyard",
        duration_minutes=20,
        priority="medium",
        frequency="daily",
        pet_id="pet_1",
        due_date=today.replace(hour=14, minute=30),
        status=TaskStatus.PENDING,
    )

    # Task 2: Feeding Dave - 12:00 PM
    cat_feeding = Task(
        task_id="task_2",
        title="Feed Dave",
        description="Give Dave his lunch",
        duration_minutes=10,
        priority="high",
        frequency="daily",
        pet_id="pet_2",
        due_date=today.replace(hour=12, minute=0),
        status=TaskStatus.COMPLETED,
    )

    # Task 5: Conflicting task - Grooming for Mochi at 8:15 AM (overlaps with 8:00-8:30 walk)
    grooming_mochi = Task(
        task_id="task_5",
        title="Groom Mochi",
        description="Brush Mochi's coat",
        duration_minutes=25,
        priority="medium",
        frequency="weekly",
        pet_id="pet_1",
        due_date=today.replace(hour=8, minute=15),
        status=TaskStatus.PENDING,
    )

    # Add tasks to pets (in original order, then mark one completed)
    mochi.add_task(morning_walk)
    mochi.add_task(afternoon_play)
    mochi.add_task(grooming_mochi)
    dave.add_task(cat_feeding)
    dave.add_task(grooming)

    # Create a Scheduler and generate today's schedule
    scheduler = Scheduler(scheduler_id="scheduler_1", owner=owner)

    print("\n" + "=" * 60)
    print("🐾 PAWPAL+ - TODAY'S SCHEDULE")
    print("=" * 60)
    print(f"Owner: {owner.name}")
    print(f"Date: {today.date()}")
    print(f"Pets: {', '.join([pet.name for pet in owner.get_pets()])}")
    print("=" * 60 + "\n")

    # Generate schedule for today
    schedule = scheduler.generate_schedule(today)

    # Display tasks
    if schedule["task_count"] == 0:
        print("No tasks scheduled for today.")
    else:
        print(f"📋 Total Tasks: {schedule['task_count']}")
        print(f"⏱️  Total Duration: {schedule['total_duration_minutes']} minutes\n")

        for i, task_detail in enumerate(schedule["tasks"], 1):
            due_time = task_detail["due_date"].split("T")[1][:5] if task_detail["due_date"] else "N/A"
            priority_emoji = "🔴" if task_detail["priority"] == "high" else "🟡" if task_detail["priority"] == "medium" else "🟢"

            # Get pet name from pet_id
            pet = next((p for p in owner.get_pets() if p.pet_id == task_detail["pet_id"]), None)
            pet_name = pet.name if pet else "Unknown"

            print(f"{i}. {priority_emoji} {task_detail['title']}")
            print(f"   Time: {due_time} | Duration: {task_detail['duration_minutes']} min")
            print(f"   Pet: {pet_name} | {task_detail['description']}")
            print()

    print("=" * 60)
    print(f"📝 Summary: {schedule['summary']}")
    print("=" * 60 + "\n")

    # Test sort_by_time method
    print("=" * 60)
    print("🕐 TASKS SORTED BY TIME")
    print("=" * 60)
    all_tasks = owner.get_all_tasks()
    sorted_by_time = scheduler.sort_by_time(all_tasks)
    for i, task in enumerate(sorted_by_time, 1):
        due_time = task.due_date.strftime("%H:%M") if task.due_date else "N/A"
        print(f"{i}. {task.title} - {due_time}")
    print()

    # Test filter_tasks by pet name
    print("=" * 60)
    print("🐕 MOCHI'S TASKS")
    print("=" * 60)
    mochi_tasks = scheduler.filter_tasks(all_tasks, pet_name="Mochi")
    for i, task in enumerate(mochi_tasks, 1):
        print(f"{i}. {task.title} ({task.status.value})")
    print()

    # Test filter_tasks by status
    print("=" * 60)
    print("✅ COMPLETED TASKS")
    print("=" * 60)
    completed_tasks = scheduler.filter_tasks(all_tasks, status="completed")
    if completed_tasks:
        for i, task in enumerate(completed_tasks, 1):
            pet_name = next((p.name for p in owner.get_pets() if p.pet_id == task.pet_id), "Unknown")
            print(f"{i}. {task.title} ({pet_name})")
    else:
        print("No completed tasks.")
    print()

    # Test filter_tasks by pet name AND status
    print("=" * 60)
    print("🐱 DAVE'S PENDING TASKS")
    print("=" * 60)
    dave_pending = scheduler.filter_tasks(all_tasks, status="pending", pet_name="Dave")
    for i, task in enumerate(dave_pending, 1):
        print(f"{i}. {task.title}")
    print()

    # Test recurring task logic
    print("=" * 60)
    print("♻️  RECURRING TASK TEST")
    print("=" * 60)
    print(f"Before: Mochi has {len(mochi.get_tasks())} tasks")
    for task in mochi.get_tasks():
        print(f"  - {task.title} (due: {task.due_date.strftime('%Y-%m-%d %H:%M')})")

    morning_walk_task = mochi.get_tasks()[0]
    print(f"\nMarking '{morning_walk_task.title}' as complete...")
    next_occurrence = scheduler.complete_task(morning_walk_task)

    print(f"\nAfter: Mochi has {len(mochi.get_tasks())} tasks")
    for task in mochi.get_tasks():
        status_icon = "✅" if task.status.value == "completed" else "⏳"
        print(f"  {status_icon} {task.title} (due: {task.due_date.strftime('%Y-%m-%d %H:%M')}, status: {task.status.value})")

    if next_occurrence:
        print(f"\n✨ Next occurrence created: {next_occurrence.title}")
        print(f"   Task ID: {next_occurrence.task_id}")
        print(f"   Due date: {next_occurrence.due_date.strftime('%Y-%m-%d %H:%M')}")
    print()

    # Test conflict detection
    print("=" * 60)
    print("🔍 CONFLICT DETECTION TEST")
    print("=" * 60)
    conflicts = scheduler.detect_conflicts(today)
    if conflicts:
        print(f"Found {len(conflicts)} conflict(s):\n")
        for conflict_warning in conflicts:
            print(f"  {conflict_warning}")
    else:
        print("✅ No conflicts detected!")
    print()


if __name__ == "__main__":
    main()
