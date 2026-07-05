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
    col1, col2 = st.columns(2)
    with col1:
        task_date = st.date_input("Due date", value=datetime.now().date())
    with col2:
        task_time = st.time_input("Start time", value=time(9, 0))

    if st.button("Add Task"):
        new_task = pps.Task(
            task_id=f"task_{st.session_state.task_counter}",
            title=task_title,
            description=f"Task for {selected_pet_name}",
            duration_minutes=int(duration),
            priority=priority,
            frequency="daily",
            pet_id=selected_pet_id,
            due_date=datetime.combine(task_date, task_time),
        )
        selected_pet = next(p for p in st.session_state.owner.get_pets() if p.pet_id == selected_pet_id)
        selected_pet.add_task(new_task)
        st.session_state.task_counter += 1
        st.success(f"✓ Added task '{task_title}' for {selected_pet_name}!")

    # Display all tasks
    all_tasks = st.session_state.owner.get_all_tasks()
    if all_tasks:
        st.write("**All Tasks:**")
        for task in all_tasks:
            pet_name = next(p.name for p in st.session_state.owner.get_pets() if p.pet_id == task.pet_id)
            priority_emoji = "🔴" if task.priority == "high" else "🟡" if task.priority == "medium" else "🟢"
            st.write(f"• {priority_emoji} {task.title} ({pet_name}) - {task.duration_minutes} min")
else:
    st.info("Add a pet first to create tasks!")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate an optimized schedule for today.")

if st.button("Generate Schedule"):
    schedule = st.session_state.scheduler.generate_schedule(datetime.now())

    if schedule["task_count"] == 0:
        st.info("No tasks scheduled for today.")
    else:
        st.success(f"📋 {schedule['summary']}")
        st.write(f"**Total Duration:** {schedule['total_duration_minutes']} minutes")

        st.write("**Scheduled Tasks (by due time):**")
        for i, task_detail in enumerate(schedule["tasks"], 1):
            due_time = task_detail["due_date"].split("T")[1][:5] if task_detail["due_date"] else "N/A"
            pet_name = next(p.name for p in st.session_state.owner.get_pets() if p.pet_id == task_detail["pet_id"])
            priority_emoji = "🔴" if task_detail["priority"] == "high" else "🟡" if task_detail["priority"] == "medium" else "🟢"

            st.write(f"{i}. {priority_emoji} **{task_detail['title']}** ({pet_name})")
            st.write(f"   ⏰ {due_time} | ⏱️ {task_detail['duration_minutes']} min")
