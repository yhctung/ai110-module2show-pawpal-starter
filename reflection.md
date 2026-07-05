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
    - 
- How did you decide which constraints mattered most?
    - 

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
    - It checks conflicting tasks based on duration and prints a warning instead of trying to fix it. 
- Why is that tradeoff reasonable for this scenario?
    - It's lightweight (O(n^2) on same-day tasks for a pet) and it would be more nuanced logic to reschedule which task and when. Since this is still a simple demo, it makes sense to save that implementation for later.
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
