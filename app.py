from datetime import datetime, time

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")


def build_task_rows(tasks: list[Task], scheduler: Scheduler) -> list[dict[str, str]]:
    pet_lookup = {pet.pet_id: pet.name for pet in scheduler.pets}
    return [
        {
            "Pet": pet_lookup.get(task.pet_id, f"Pet {task.pet_id}"),
            "Title": task.title,
            "Type": task.task_type,
            "Due": task.due_time.strftime("%Y-%m-%d %H:%M"),
            "Frequency": task.frequency,
            "Priority": task.priority.title(),
            "Status": task.status.title(),
        }
        for task in tasks
    ]


def initialize_state() -> None:
    if "owner" not in st.session_state:
        st.session_state.owner = Owner(1, "Jordan", "jordan67@gmail.com", "123-555-0100")

    if "scheduler" not in st.session_state:
        st.session_state.scheduler = Scheduler()
        st.session_state.scheduler.add_owner(st.session_state.owner)

    if "next_pet_id" not in st.session_state:
        st.session_state.next_pet_id = 1000

    if "next_task_id" not in st.session_state:
        st.session_state.next_task_id = 1


initialize_state()

owner: Owner = st.session_state.owner
scheduler: Scheduler = st.session_state.scheduler

st.title("🐾 PawPal+")
st.caption("Manage pet care with smart scheduling, sorted timelines, and conflict alerts.")

st.subheader("Owner")
st.write(f"Logged in as: **{owner.name}**")
st.write(f"Email: {owner.email}")
st.write(f"Phone: {owner.phone}")

st.divider()

st.subheader("Add a Pet")
with st.form("add_pet_form"):
    pet_name = st.text_input("Pet name")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    breed = st.text_input("Breed")
    age = st.number_input("Age", min_value=0, max_value=50, value=1)
    diet_notes = st.text_area("Diet notes")
    medication_notes = st.text_area("Medication notes")
    add_pet_submitted = st.form_submit_button("Add pet")

if add_pet_submitted:
    try:
        new_pet = Pet(
            st.session_state.next_pet_id,
            pet_name,
            species,
            breed,
            int(age),
            diet_notes,
            medication_notes,
            owner.owner_id,
        )
        scheduler.add_pet(new_pet)
        st.session_state.next_pet_id += 1
        st.success(f"{new_pet.name} was added successfully.")
    except ValueError as error:
        st.error(str(error))

st.subheader("Current Pets")
if owner.view_pets():
    pet_rows = [
        {
            "Pet": pet.name,
            "Species": pet.species.title(),
            "Breed": pet.breed,
            "Age": str(pet.age),
            "Pet ID": str(pet.pet_id),
        }
        for pet in owner.view_pets()
    ]
    st.table(pet_rows)
else:
    st.info("No pets added yet.")

st.divider()

st.subheader("Schedule a Task")
pet_options = {f"{pet.name} (ID: {pet.pet_id})": pet for pet in owner.view_pets()}

if pet_options:
    with st.form("schedule_task_form"):
        selected_pet_label = st.selectbox("Choose a pet", list(pet_options.keys()))
        task_title = st.text_input("Task title")
        task_type = st.selectbox(
            "Task type",
            ["feeding", "walking", "medication", "grooming", "vet appointment", "other"],
        )
        due_date = st.date_input("Due date")
        due_clock = st.time_input("Due time", value=time(9, 0))
        frequency = st.selectbox(
            "Frequency",
            ["once", "daily", "weekly", "biweekly", "monthly", "yearly"],
            index=0,
        )
        priority = st.selectbox("Priority", ["low", "medium", "high", "critical"], index=1)
        schedule_task_submitted = st.form_submit_button("Schedule task")

    if schedule_task_submitted:
        try:
            selected_pet = pet_options[selected_pet_label]
            due_time = datetime.combine(due_date, due_clock)
            new_task = Task(
                st.session_state.next_task_id,
                task_title,
                task_type,
                due_time,
                priority,
                "pending",
                selected_pet.pet_id,
                frequency,
            )
            scheduler.schedule_task(new_task)
            st.session_state.next_task_id += 1
            st.success(f"Task scheduled for {selected_pet.name}.")
        except ValueError as error:
            st.error(str(error))
else:
    st.info("Add a pet before scheduling tasks.")

st.divider()

st.subheader("Schedule Health")
conflict_warnings = scheduler.detect_conflicts()
if conflict_warnings:
    st.warning("Two or more tasks share the same scheduled time. Review these items before the day gets busy.")
    for warning in conflict_warnings:
        st.warning(warning, icon="⚠️")
else:
    st.success("No exact-time conflicts found in the current schedule.", icon="✅")

st.divider()

st.subheader("Today's Schedule")
today = datetime.now()
sorted_today_tasks = [
    task for task in scheduler.sort_tasks_by_time() if task.due_time.date() == today.date()
]

if sorted_today_tasks:
    st.table(build_task_rows(sorted_today_tasks, scheduler))
else:
    st.info("No tasks scheduled for today.")

st.divider()

st.subheader("Task Explorer")
pet_filter_options = ["All pets"] + [pet.name for pet in owner.view_pets()]
selected_pet_filter = st.selectbox("Filter by pet", pet_filter_options)
selected_status_filter = st.selectbox("Filter by status", ["All statuses", "pending", "complete"])

if selected_status_filter != "All statuses":
    filtered_tasks = scheduler.filter_tasks(
        status=selected_status_filter,
        pet_name=None if selected_pet_filter == "All pets" else selected_pet_filter,
    )
elif selected_pet_filter != "All pets":
    filtered_tasks = scheduler.filter_tasks(pet_name=selected_pet_filter)
else:
    filtered_tasks = scheduler.get_all_tasks()

filtered_tasks = sorted(filtered_tasks, key=lambda task: task.due_time)

if filtered_tasks:
    st.table(build_task_rows(filtered_tasks, scheduler))
else:
    st.info("No tasks match the selected filters.")
