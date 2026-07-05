# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
    -User should be able to add a pet and link it to an owner
    - User should be able to add a task to a pet
    - User should be able to see all the tasks for an owner's pets
- What classes did you include, and what responsibilities did you assign to each?
    -Task - activity with description, time/frequency, completion/priority. methods should include a getter and something to change the completion/priority
    -Pet - stores details and list of tasks. methods should include getters and setters for tasks and details
    -Owner - can own multiple pets, store basic contact info. methods to include adding/removing pets and getting tasks
    -Scheduler - 1 per owner, organizes/prioritizes tasks, generates schedules. methods should include functions for performing the former.

**b. Design changes**

- Did your design change during implementation?
    - yes
- If yes, describe at least one change and why you made it.
    - the initial skeleton started to include a setup for repeating tasks and state tracking, but it wasn't fully flushed out. also, while owner > pet and pet > task logic was noted, there weren't references the other way, so AI noted this could add unnecessary complexity 

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
    - manual priority, overdue status, due date/start time, pet ownership, task status/recurrence/duration
- How did you decide which constraints mattered most?
    - Overdue status takes absolute priority, then manual priority level, then chronological due date. I think overdue/missed tasks should be most important, then the whatever the user deems important should be next. 

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
    - It checks conflicting tasks based on duration and prints a warning instead of trying to fix it. 
- Why is that tradeoff reasonable for this scenario?
    - It's lightweight (O(n^2) on same-day tasks for a pet) and it would be more nuanced logic to reschedule which task and when. Since this is still a simple demo, it makes sense to save that implementation for later.
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
    - Used Claude for debugging and refactoring mainly - removing unused methods, adding/cleaning up logic for recurrence/conflict detection, debugging Python/Streamlit issues. 
    - Also used it to generate the updated UML diagram which I backchecked.
- What kinds of prompts or questions were most helpful?
    - "Can you explain how timedelta works for recurring tasks?" — conceptual explanations helped me understand the code better
    - "Remove unused methods and attributes" — directing refactoring was easier than doing it manually, and I was able to supervise and make sure things were unused prior to removal
    - other than those, a lot of exploratory questions were helpful in understanding and shaping direction

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
    - When AI suggested removing priority from the Task class and basing scheduling only on time/overdue status, I asked to keep manual priority. The suggestion was technically cleaner but lost user control over task importance.
- How did you evaluate or verify what the AI suggested?
    - I tested the changes in main.py to verify behavior. For refactoring, I checked that all tests still passed after changes. For UI changes, I inspected the Streamlit app to confirm the feature worked as intended.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
    - Empty states/null handling, task sorting/filtering, task conflict detection, recurring task creation, schedule summary generation, priority ordering
- Why were these tests important?
    - Testing empty states ensures the app doesn't crash when users have no data. Sorting tests and conflict detection tests verify expected behavior. In general testing edge cases is important to reveal bugs that could crash the app or produce wrong output. 

**b. Confidence**

- How confident are you that your scheduler works correctly?
    - 4/5? The logic seems solid and I think the primary functions work - sorting/filtering, conflict detection, task recurrence. I left a star off because there are probably additional edge cases I haven't considered.
- What edge cases would you test next if you had more time?
    - tasks with zero duration 
    - tasks due at midnight
    - recurring task chains (marking tomorrow's occurrence complete and checking the day-after appears)
    - completing all tasks on a given day and regenerating the schedule
    - tasks with very long durations (>12 hours)
    - scheduling across multiple days in one view

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
    - I thought the conflict detection and the recurring tasks methods were nice. The conflict detection was just an interval overlap check and the recurring tasks was just a timedelta calc, but I thought both brought strong benefit to the user without lengthy or complex implementation.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
    - Add time-slot auto-shifting - basically extending the detect conflicts to detect conflicts and suggest/auto-move one task to the next available slot instead of just warning
    - Support flexible due-date windows, like sometime this week
    - Add pet-specific constraints, like maybe certain breeds need a certain set of tasks or each pet has personality preferences for activity types
    - Multi-day scheduling view
    - Undo/redo for task edits and completions
    - Better recurring task UI, show which occurrences exist and let users skip or reschedule individual ones

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
    - I think the best way to work with AI is to ask for the reasoning and the implementation. Also starting with a clear UML even if it is rough helps direct the AI during implementation and makes refactoring easier. Ultimately both these takeaways just mean that you should decide what the system should do yourself and use AI to supplement. 
