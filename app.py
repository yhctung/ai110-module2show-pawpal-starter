import streamlit as st
import pawpal_system as pps

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

# Initialize owner and scheduler in session state
if "owner" not in st.session_state:
    st.session_state.owner = pps.Owner(
        owner_id="owner_1",
        name="Ryan",
    )

if "scheduler" not in st.session_state:
    st.session_state.scheduler = pps.Scheduler(
        scheduler_id="scheduler_1",
        owner=st.session_state.owner,
    )

if "task_counter" not in st.session_state:
    st.session_state.task_counter = 1

if "pet_counter" not in st.session_state:
    st.session_state.pet_counter = 1

st.subheader("Add a Pet")
col1, col2 = st.columns(2)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add Pet"):
    new_pet = pps.Pet(
        pet_id=f"pet_{st.session_state.pet_counter}",
        name=pet_name,
        species=species,
        owner_id="owner_1",
    )
    st.session_state.owner.add_pet(new_pet)
    st.session_state.pet_counter += 1
    st.success(f"✓ Added {pet_name} the {species}!")

# Display current pets
if st.session_state.owner.get_pets():
    st.write("**Your Pets:**")
    for pet in st.session_state.owner.get_pets():
        st.write(f"• {pet.name} ({pet.species}) - {len(pet.get_tasks())} task(s)")

st.markdown("### Add Tasks")
st.caption("Select a pet and add a task for them.")

if st.session_state.owner.get_pets():
    pet_options = {pet.name: pet.pet_id for pet in st.session_state.owner.get_pets()}
    selected_pet_name = st.selectbox("Pet", list(pet_options.keys()))
    selected_pet_id = pet_options[selected_pet_name]

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    from datetime import datetime, timedelta, time
    col1, col2, col3 = st.columns(3)
    with col1:
        task_date = st.date_input("Due date", value=datetime.now().date())
    with col2:
        task_time = st.time_input("Start time", value=time(9, 0))
    with col3:
        frequency = st.selectbox("Recurrence", ["once", "daily", "weekly"], index=0)

    if st.button("Add Task"):
        new_task = pps.Task(
            task_id=f"task_{st.session_state.task_counter}",
            title=task_title,
            description=f"Task for {selected_pet_name}",
            duration_minutes=int(duration),
            priority=priority,
            frequency=frequency,
            pet_id=selected_pet_id,
            due_date=datetime.combine(task_date, task_time),
        )
        selected_pet = next(p for p in st.session_state.owner.get_pets() if p.pet_id == selected_pet_id)
        selected_pet.add_task(new_task)
        st.session_state.task_counter += 1
        st.success(f"✓ Added task '{task_title}' for {selected_pet_name}! (Recurs: {frequency})")

    # Display all tasks with edit/complete options
    all_tasks = st.session_state.owner.get_all_tasks()
    if all_tasks:
        st.write("**All Tasks:**")
        for task in all_tasks:
            pet_name = next(p.name for p in st.session_state.owner.get_pets() if p.pet_id == task.pet_id)
            priority_emoji = "🔴" if task.priority == "high" else "🟡" if task.priority == "medium" else "🟢"
            status_icon = "✅" if task.status.value == "completed" else "⏳"

            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"{status_icon} {priority_emoji} {task.title} ({pet_name}) - {task.duration_minutes} min")
            with col2:
                if task.status.value == "pending":
                    if st.button("✓ Complete", key=f"complete_{task.task_id}"):
                        st.session_state.scheduler.complete_task(task)
                        st.success(f"Marked '{task.title}' as complete!")
                        st.rerun()
            with col3:
                if st.button("Edit", key=f"edit_{task.task_id}"):
                    st.session_state.editing_task_id = task.task_id
                    st.rerun()

        # Edit task form
        if "editing_task_id" in st.session_state:
            task_to_edit = next((t for t in all_tasks if t.task_id == st.session_state.editing_task_id), None)
            if task_to_edit:
                st.divider()
                st.subheader(f"Edit Task: {task_to_edit.title}")

                col1, col2, col3 = st.columns(3)
                with col1:
                    new_title = st.text_input("Task title", value=task_to_edit.title, key="edit_title")
                with col2:
                    new_duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=task_to_edit.duration_minutes, key="edit_duration")
                with col3:
                    new_priority = st.selectbox("Priority", ["low", "medium", "high"], index=["low", "medium", "high"].index(task_to_edit.priority), key="edit_priority")

                col1, col2, col3 = st.columns(3)
                with col1:
                    new_time = task_to_edit.due_date.time()
                    new_time_input = st.time_input("Start time", value=new_time, key="edit_time")
                with col2:
                    new_date = task_to_edit.due_date.date()
                    new_date_input = st.date_input("Due date", value=new_date, key="edit_date")
                with col3:
                    new_frequency = st.selectbox("Recurrence", ["once", "daily", "weekly"], index=["once", "daily", "weekly"].index(task_to_edit.frequency) if task_to_edit.frequency in ["once", "daily", "weekly"] else 0, key="edit_frequency")

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Save Changes"):
                        task_to_edit.title = new_title
                        task_to_edit.duration_minutes = new_duration
                        task_to_edit.priority = new_priority
                        task_to_edit.frequency = new_frequency
                        task_to_edit.due_date = datetime.combine(new_date_input, new_time_input)
                        st.session_state.editing_task_id = None
                        st.success(f"Updated '{new_title}'!")
                        st.rerun()
                with col2:
                    if st.button("Cancel"):
                        st.session_state.editing_task_id = None
                        st.rerun()
else:
    st.info("Add a pet first to create tasks!")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate an optimized schedule for today with filters.")

col1, col2 = st.columns(2)
with col1:
    filter_pet = st.selectbox("Filter by Pet", ["All"] + [p.name for p in st.session_state.owner.get_pets()]) if st.session_state.owner.get_pets() else None
with col2:
    filter_status = st.selectbox("Filter by Status", ["All", "pending", "completed"])

col1, col2 = st.columns(2)
with col1:
    filter_priority = st.selectbox("Filter by Priority", ["All", "high", "medium", "low"])
with col2:
    sort_by = st.selectbox("Sort by", ["Priority + Time", "Time Only"])

if st.button("Generate Schedule"):
    all_tasks = st.session_state.owner.get_all_tasks()

    # Apply filters
    filtered_tasks = all_tasks
    filters_applied = []

    if filter_status != "All":
        filtered_tasks = st.session_state.scheduler.filter_tasks(filtered_tasks, status=filter_status)
        filters_applied.append(f"status={filter_status}")

    if filter_pet and filter_pet != "All":
        filtered_tasks = st.session_state.scheduler.filter_tasks(filtered_tasks, pet_name=filter_pet)
        filters_applied.append(f"pet={filter_pet}")

    if filter_priority != "All":
        filtered_tasks = [t for t in filtered_tasks if t.priority == filter_priority]
        filters_applied.append(f"priority={filter_priority}")

    # Apply sorting
    if sort_by == "Time Only":
        filtered_tasks = st.session_state.scheduler.sort_by_time(filtered_tasks)
    else:
        filtered_tasks = st.session_state.scheduler.prioritize_tasks(filtered_tasks)

    # Display what's being considered
    st.info(f"📊 Considering {len(filtered_tasks)} task(s) • Filters: {', '.join(filters_applied) if filters_applied else 'None'} • Sorting: {sort_by}")

    if len(filtered_tasks) == 0:
        st.warning("No tasks match the selected filters.")
    else:
        st.success(f"📋 {len(filtered_tasks)} task(s) scheduled")
        total_duration = sum(t.duration_minutes for t in filtered_tasks)
        st.write(f"**Total Duration:** {total_duration} minutes")

        st.write("**Filtered & Sorted Tasks:**")
        for i, task in enumerate(filtered_tasks, 1):
            due_time = task.due_date.strftime("%H:%M") if task.due_date else "N/A"
            pet_name = next(p.name for p in st.session_state.owner.get_pets() if p.pet_id == task.pet_id)
            priority_emoji = "🔴" if task.priority == "high" else "🟡" if task.priority == "medium" else "🟢"
            status_icon = "✅" if task.status.value == "completed" else "⏳"

            st.write(f"{i}. {status_icon} {priority_emoji} **{task.title}** ({pet_name})")
            st.write(f"   ⏰ {due_time} | ⏱️ {task.duration_minutes} min")
