# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
python -m pytest

# Run with coverage:
python -m pytest --cov
```

Sample test output:

```
From main.py

============================================================
🐾 PAWPAL+ - TODAY'S SCHEDULE
============================================================
Owner: Ryan
Date: 2026-07-05
Pets: Mochi, Dave
============================================================

📋 Total Tasks: 4
⏱️  Total Duration: 75 minutes

1. 🔴 Morning Walk
   Time: 08:00 | Duration: 30 min
   Pet: Mochi | Take Mochi for a 30-minute walk in the park

2. 🔴 Feed Dave
   Time: 12:00 | Duration: 10 min
   Pet: Dave | Give Dave his lunch

3. 🟡 Afternoon Playtime
   Time: 14:30 | Duration: 20 min
   Pet: Mochi | Play fetch with Mochi in the backyard

4. 🟢 Brush Dave
   Time: 16:00 | Duration: 15 min
   Pet: Dave | Brush Dave's fur to prevent matting

============================================================
📝 Summary: Scheduled 4 task(s) for 2026-07-05. Total duration: 75 minutes. High priority: 2 task(s).
============================================================
```

```
What it checks:
Empty States & Null Handling (5 tests)
✅ Empty pet with no tasks returns "No tasks scheduled"
✅ Owner with no pets returns empty task list (not crash)
✅ Filter by non-existent pet name doesn't apply filter (returns all)
✅ Filter by unknown status returns empty list
✅ Aggregate tasks across multiple pets works correctly
Sorting & Time Boundary Cases (3 tests)
✅ Tasks at exact midnight (00:00) sort correctly
✅ Two tasks at exact same time maintain stable order
✅ Unknown priority values sort last (after high/medium/low)
Conflict Detection Edge Cases (3 tests)
✅ Two tasks starting at exact same time flagged as conflict
✅ One task completely containing another detected as conflict
✅ Tasks overlapping by 1 minute detected as conflict
Recurrence & Filtering Edge Cases (5 tests)
✅ Unknown frequency (monthly, etc.) returns None safely
✅ Zero-duration recurring tasks still create next occurrence
✅ Schedule summary correctly counts 0 high-priority tasks
✅ Filter by "completed" status returns only completed tasks
✅ Filter by "pending" status returns only pending tasks

# Paste your pytest output here

platform win32 -- Python 3.13.13, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\Dell User\Desktop\Codepath\ai110-module2show-pawpal-starter
plugins: anyio-4.14.1
collected 34 items                                                                                                                       

tests\test_pawpal.py ..................................                                                                            [100%]

========================================================== 34 passed in 0.55s ====

Confidence Level : ⭐⭐⭐⭐☆
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | Scheduler.prioritize_tasks, Scheduler.sort_by_time | 1st sorts tasks by urgency: overdue tasks first, then by due date (soonest first). 2nd sorts tasks chronologically by time of day (HH:MM), which is useful for viewing schedule in strict time order. |
| Filtering | Scheduler.filter_tasks | filters tasks by completion status and/or pet name, or neither. Enables skipping completed tasks or focusing on specific pet |
| Conflict handling | Scheduler.detect_conflicts | detects overlapping time slots by calculating time windows. returns warning string |
| Recurring tasks | Scheduler.complete_task, Task.create_next_occurrence| Marks task as completed with timestamp, then calls create_next_occurrence() on the task. If it's recurring, it auto-adds the next occurrence to the pet's task list. Task.create_next_occurrence returns the next task instance (or None if not recurring) |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. Add a pet with an owner, just name and species
2. Add a task for the pet, including description, duration, and due date
3. Add pets and tasks as desired
4. Generate schedule for all pets, prioritized by due date. Can filter by pet or task completion
5. Warning will be printed if tasks for one pet overlap or occur simultaneously

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
