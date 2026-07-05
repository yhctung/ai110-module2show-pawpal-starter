from datetime import datetime, timedelta
from pawpal_system import Owner, Pet, Task, TaskStatus, Scheduler


def main():
    """Demo: Create owner, pets, tasks, and generate today's schedule."""

    # Create an Owner
    owner = Owner(
        owner_id="owner_1",
        name="Ryan",
        email="ryan@example.com",
    )

    # Create two Pets
    mochi = Pet(
        pet_id="pet_1",
        name="Mochi",
        species="dog",
        age=3,
        owner_id="owner_1",
        health_notes="Needs regular exercise",
    )

    dave = Pet(
        pet_id="pet_2",
        name="Dave",
        species="cat",
        age=2,
        owner_id="owner_1",
        health_notes="Prefers quiet time in afternoon",
    )

    # Add pets to owner
    owner.add_pet(mochi)
    owner.add_pet(dave)

    # Get today and create tasks with different times
    today = datetime.now()

    # Task 1: Morning walk for Mochi (high priority)
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

    # Task 2: Feeding Dave (high priority)
    cat_feeding = Task(
        task_id="task_2",
        title="Feed Dave",
        description="Give Dave his lunch",
        duration_minutes=10,
        priority="high",
        frequency="daily",
        pet_id="pet_2",
        due_date=today.replace(hour=12, minute=0),
        status=TaskStatus.PENDING,
    )

    # Task 3: Afternoon playtime for Mochi (medium priority)
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

    # Task 4: Grooming for Dave (low priority)
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

    # Add tasks to pets
    mochi.add_task(morning_walk)
    mochi.add_task(afternoon_play)
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
            pet_name = next((p.name for p in owner.get_pets() if p.pet_id == task_detail["pet_id"]), "Unknown")

            print(f"{i}. {priority_emoji} {task_detail['title']}")
            print(f"   Time: {due_time} | Duration: {task_detail['duration_minutes']} min")
            print(f"   Pet: {pet_name} | {task_detail['description']}")
            print()

    print("=" * 60)
    print(f"📝 Summary: {schedule['summary']}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
