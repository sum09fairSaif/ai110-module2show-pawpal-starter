from datetime import datetime
from pathlib import Path

from pawpal_system import Owner, Pet, Scheduler, Task


def test_task_mark_complete_changes_status() -> None:
    task = Task(
        1,
        "Feed Fluffy",
        "feeding",
        datetime(2026, 3, 29, 8, 0),
        "high",
        "pending",
        12345678,
        "once",
    )

    task.mark_complete()

    assert task.status == "complete"


def test_add_task_increases_pet_task_count() -> None:
    pet = Pet(
        12345678,
        "Fluffy",
        "Cat",
        "Persian",
        10,
        "High-quality cat food",
        "None",
        96003110,
    )
    task = Task(
        1,
        "Feed Fluffy",
        "feeding",
        datetime(2026, 3, 29, 8, 0),
        "high",
        "pending",
        pet.pet_id,
        "once",
    )

    starting_count = len(pet.view_tasks())
    pet.add_task(task)

    assert len(pet.view_tasks()) == starting_count + 1


def test_filter_tasks_by_status() -> None:
    scheduler = Scheduler()
    owner = Owner(96003110, "Alice", "alice@example.com", "217-555-1234")
    scheduler.add_owner(owner)

    fluffy = Pet(12345678, "Fluffy", "Cat", "Persian", 10, "", "", owner.owner_id)
    buddy = Pet(87654321, "Buddy", "Dog", "Golden Retriever", 5, "", "", owner.owner_id)
    scheduler.add_pet(fluffy)
    scheduler.add_pet(buddy)

    pending_task = Task(
        1,
        "Feed Fluffy",
        "feeding",
        datetime(2026, 3, 29, 8, 0),
        "high",
        "pending",
        fluffy.pet_id,
        "once",
    )
    complete_task = Task(
        2,
        "Walk Buddy",
        "walking",
        datetime(2026, 3, 29, 18, 0),
        "medium",
        "complete",
        buddy.pet_id,
        "once",
    )
    scheduler.schedule_task(pending_task)
    scheduler.schedule_task(complete_task)

    filtered = scheduler.filter_tasks(status="pending")

    assert filtered == [pending_task]


def test_filter_tasks_by_pet_name_is_case_insensitive() -> None:
    scheduler = Scheduler()
    owner = Owner(96003110, "Alice", "alice@example.com", "217-555-1234")
    scheduler.add_owner(owner)

    fluffy = Pet(12345678, "Fluffy", "Cat", "Persian", 10, "", "", owner.owner_id)
    buddy = Pet(87654321, "Buddy", "Dog", "Golden Retriever", 5, "", "", owner.owner_id)
    scheduler.add_pet(fluffy)
    scheduler.add_pet(buddy)

    fluffy_task = Task(
        1,
        "Feed Fluffy",
        "feeding",
        datetime(2026, 3, 29, 8, 0),
        "high",
        "pending",
        fluffy.pet_id,
        "once",
    )
    buddy_task = Task(
        2,
        "Walk Buddy",
        "walking",
        datetime(2026, 3, 29, 18, 0),
        "medium",
        "pending",
        buddy.pet_id,
        "once",
    )
    scheduler.schedule_task(fluffy_task)
    scheduler.schedule_task(buddy_task)

    filtered = scheduler.filter_tasks(pet_name="fluffy")

    assert filtered == [fluffy_task]


def test_filter_tasks_by_status_and_pet_name() -> None:
    scheduler = Scheduler()
    owner = Owner(96003110, "Alice", "alice@example.com", "217-555-1234")
    scheduler.add_owner(owner)

    fluffy = Pet(12345678, "Fluffy", "Cat", "Persian", 10, "", "", owner.owner_id)
    scheduler.add_pet(fluffy)

    pending_task = Task(
        1,
        "Feed Fluffy",
        "feeding",
        datetime(2026, 3, 29, 8, 0),
        "high",
        "pending",
        fluffy.pet_id,
        "once",
    )
    complete_task = Task(
        2,
        "Brush Fluffy",
        "grooming",
        datetime(2026, 3, 29, 12, 0),
        "low",
        "complete",
        fluffy.pet_id,
        "once",
    )
    scheduler.schedule_task(pending_task)
    scheduler.schedule_task(complete_task)

    filtered = scheduler.filter_tasks(status="complete", pet_name="FLUFFY")

    assert filtered == [complete_task]


def test_sort_tasks_by_time_returns_priority_then_time_order() -> None:
    scheduler = Scheduler()
    owner = Owner(96003110, "Alice", "alice@example.com", "217-555-1234")
    scheduler.add_owner(owner)

    fluffy = Pet(12345678, "Fluffy", "Cat", "Persian", 10, "", "", owner.owner_id)
    buddy = Pet(87654321, "Buddy", "Dog", "Golden Retriever", 5, "", "", owner.owner_id)
    scheduler.add_pet(fluffy)
    scheduler.add_pet(buddy)

    later_task = Task(
        1,
        "Evening walk",
        "walking",
        datetime(2026, 3, 29, 18, 0),
        "medium",
        "pending",
        buddy.pet_id,
        "once",
    )
    earlier_high_task = Task(
        2,
        "Breakfast",
        "feeding",
        datetime(2026, 3, 29, 7, 0),
        "high",
        "pending",
        fluffy.pet_id,
        "once",
    )
    later_high_task = Task(
        3,
        "Lunch meds",
        "medication",
        datetime(2026, 3, 29, 12, 0),
        "high",
        "pending",
        fluffy.pet_id,
        "once",
    )
    critical_task = Task(
        4,
        "Emergency medication",
        "medication",
        datetime(2026, 3, 29, 20, 0),
        "critical",
        "pending",
        fluffy.pet_id,
        "once",
    )

    scheduler.schedule_task(later_task)
    scheduler.schedule_task(earlier_high_task)
    scheduler.schedule_task(later_high_task)
    scheduler.schedule_task(critical_task)

    sorted_tasks = scheduler.sort_tasks_by_time()

    assert sorted_tasks == [critical_task, earlier_high_task, later_high_task, later_task]


def test_sort_tasks_by_time_can_sort_filtered_tasks() -> None:
    scheduler = Scheduler()
    owner = Owner(96003110, "Alice", "alice@example.com", "217-555-1234")
    scheduler.add_owner(owner)

    fluffy = Pet(12345678, "Fluffy", "Cat", "Persian", 10, "", "", owner.owner_id)
    scheduler.add_pet(fluffy)

    low_task = Task(
        1,
        "Brush Fluffy",
        "grooming",
        datetime(2026, 3, 29, 8, 0),
        "low",
        "pending",
        fluffy.pet_id,
        "once",
    )
    high_task = Task(
        2,
        "Give medicine",
        "medication",
        datetime(2026, 3, 29, 10, 0),
        "high",
        "pending",
        fluffy.pet_id,
        "once",
    )
    scheduler.schedule_task(low_task)
    scheduler.schedule_task(high_task)

    filtered_pending_tasks = scheduler.filter_tasks(status="pending")

    assert scheduler.sort_tasks_by_time(filtered_pending_tasks) == [high_task, low_task]


def test_mark_task_complete_creates_next_daily_task() -> None:
    scheduler = Scheduler()
    owner = Owner(96003110, "Alice", "alice@example.com", "217-555-1234")
    scheduler.add_owner(owner)

    fluffy = Pet(12345678, "Fluffy", "Cat", "Persian", 10, "", "", owner.owner_id)
    scheduler.add_pet(fluffy)

    daily_task = Task(
        1,
        "Feed Fluffy",
        "feeding",
        datetime(2026, 3, 29, 8, 0),
        "high",
        "pending",
        fluffy.pet_id,
        "daily",
    )
    scheduler.schedule_task(daily_task)

    next_task = scheduler.mark_task_complete(daily_task.task_id)

    assert daily_task.status == "complete"
    assert next_task is not None
    assert next_task.task_id == 2
    assert next_task.due_time == datetime(2026, 3, 30, 8, 0)
    assert next_task.status == "pending"
    assert next_task.frequency == "daily"


def test_mark_task_complete_for_once_task_does_not_create_recurring_task() -> None:
    scheduler = Scheduler()
    owner = Owner(96003110, "Alice", "alice@example.com", "217-555-1234")
    scheduler.add_owner(owner)

    fluffy = Pet(12345678, "Fluffy", "Cat", "Persian", 10, "", "", owner.owner_id)
    scheduler.add_pet(fluffy)

    one_time_task = Task(
        1,
        "One-time grooming",
        "grooming",
        datetime(2026, 3, 29, 15, 0),
        "low",
        "pending",
        fluffy.pet_id,
        "once",
    )
    scheduler.schedule_task(one_time_task)

    next_task = scheduler.mark_task_complete(one_time_task.task_id)

    assert one_time_task.status == "complete"
    assert next_task is None
    assert scheduler.get_all_tasks() == [one_time_task]


def test_mark_task_complete_creates_next_weekly_task() -> None:
    scheduler = Scheduler()
    owner = Owner(96003110, "Alice", "alice@example.com", "217-555-1234")
    scheduler.add_owner(owner)

    buddy = Pet(87654321, "Buddy", "Dog", "Golden Retriever", 5, "", "", owner.owner_id)
    scheduler.add_pet(buddy)

    weekly_task = Task(
        1,
        "Give Buddy medicine",
        "medication",
        datetime(2026, 3, 29, 10, 0),
        "high",
        "pending",
        buddy.pet_id,
        "weekly",
    )
    scheduler.schedule_task(weekly_task)

    next_task = scheduler.mark_task_complete(weekly_task.task_id)

    assert weekly_task.status == "complete"
    assert next_task is not None
    assert next_task.task_id == 2
    assert next_task.due_time == datetime(2026, 4, 5, 10, 0)
    assert next_task.status == "pending"
    assert next_task.frequency == "weekly"


def test_mark_task_complete_creates_next_biweekly_task() -> None:
    scheduler = Scheduler()
    owner = Owner(96003110, "Alice", "alice@example.com", "217-555-1234")
    scheduler.add_owner(owner)

    buddy = Pet(87654321, "Buddy", "Dog", "Golden Retriever", 5, "", "", owner.owner_id)
    scheduler.add_pet(buddy)

    biweekly_task = Task(
        1,
        "Apply Buddy's flea treatment",
        "medication",
        datetime(2026, 3, 29, 10, 0),
        "high",
        "pending",
        buddy.pet_id,
        "biweekly",
    )
    scheduler.schedule_task(biweekly_task)

    next_task = scheduler.mark_task_complete(biweekly_task.task_id)

    assert biweekly_task.status == "complete"
    assert next_task is not None
    assert next_task.task_id == 2
    assert next_task.due_time == datetime(2026, 4, 12, 10, 0)
    assert next_task.status == "pending"
    assert next_task.frequency == "biweekly"


def test_mark_task_complete_creates_next_monthly_task() -> None:
    scheduler = Scheduler()
    owner = Owner(96003110, "Alice", "alice@example.com", "217-555-1234")
    scheduler.add_owner(owner)

    fluffy = Pet(12345678, "Fluffy", "Cat", "Persian", 10, "", "", owner.owner_id)
    scheduler.add_pet(fluffy)

    monthly_task = Task(
        1,
        "Give Fluffy monthly treatment",
        "medication",
        datetime(2026, 1, 31, 8, 0),
        "high",
        "pending",
        fluffy.pet_id,
        "monthly",
    )
    scheduler.schedule_task(monthly_task)

    next_task = scheduler.mark_task_complete(monthly_task.task_id)

    assert monthly_task.status == "complete"
    assert next_task is not None
    assert next_task.task_id == 2
    assert next_task.due_time == datetime(2026, 2, 28, 8, 0)
    assert next_task.status == "pending"
    assert next_task.frequency == "monthly"


def test_mark_task_complete_creates_next_yearly_task() -> None:
    scheduler = Scheduler()
    owner = Owner(96003110, "Alice", "alice@example.com", "217-555-1234")
    scheduler.add_owner(owner)

    buddy = Pet(87654321, "Buddy", "Dog", "Golden Retriever", 5, "", "", owner.owner_id)
    scheduler.add_pet(buddy)

    yearly_task = Task(
        1,
        "Buddy annual vaccine",
        "vet appointment",
        datetime(2024, 2, 29, 9, 0),
        "critical",
        "pending",
        buddy.pet_id,
        "yearly",
    )
    scheduler.schedule_task(yearly_task)

    next_task = scheduler.mark_task_complete(yearly_task.task_id)

    assert yearly_task.status == "complete"
    assert next_task is not None
    assert next_task.task_id == 2
    assert next_task.due_time == datetime(2025, 2, 28, 9, 0)
    assert next_task.status == "pending"
    assert next_task.frequency == "yearly"


def test_detect_conflicts_for_same_pet_returns_warning() -> None:
    scheduler = Scheduler()
    owner = Owner(96003110, "Alice", "alice@example.com", "217-555-1234")
    scheduler.add_owner(owner)

    fluffy = Pet(12345678, "Fluffy", "Cat", "Persian", 10, "", "", owner.owner_id)
    scheduler.add_pet(fluffy)

    task_one = Task(
        1,
        "Feed Fluffy",
        "feeding",
        datetime(2026, 3, 29, 8, 0),
        "high",
        "pending",
        fluffy.pet_id,
        "once",
    )
    task_two = Task(
        2,
        "Brush Fluffy",
        "grooming",
        datetime(2026, 3, 29, 8, 0),
        "medium",
        "pending",
        fluffy.pet_id,
        "once",
    )
    scheduler.schedule_task(task_one)
    scheduler.schedule_task(task_two)

    warnings = scheduler.detect_conflicts()

    assert len(warnings) == 1
    assert "same pet" in warnings[0]


def test_detect_conflicts_for_different_pets_returns_warning() -> None:
    scheduler = Scheduler()
    owner = Owner(96003110, "Alice", "alice@example.com", "217-555-1234")
    scheduler.add_owner(owner)

    fluffy = Pet(12345678, "Fluffy", "Cat", "Persian", 10, "", "", owner.owner_id)
    buddy = Pet(87654321, "Buddy", "Dog", "Golden Retriever", 5, "", "", owner.owner_id)
    scheduler.add_pet(fluffy)
    scheduler.add_pet(buddy)

    task_one = Task(
        1,
        "Feed Fluffy",
        "feeding",
        datetime(2026, 3, 29, 9, 0),
        "high",
        "pending",
        fluffy.pet_id,
        "once",
    )
    task_two = Task(
        2,
        "Walk Buddy",
        "walking",
        datetime(2026, 3, 29, 9, 0),
        "medium",
        "pending",
        buddy.pet_id,
        "once",
    )
    scheduler.schedule_task(task_one)
    scheduler.schedule_task(task_two)

    warnings = scheduler.detect_conflicts()

    assert len(warnings) == 1
    assert "different pets" in warnings[0]


def test_detect_conflicts_returns_empty_list_when_no_times_overlap() -> None:
    scheduler = Scheduler()
    owner = Owner(96003110, "Alice", "alice@example.com", "217-555-1234")
    scheduler.add_owner(owner)

    fluffy = Pet(12345678, "Fluffy", "Cat", "Persian", 10, "", "", owner.owner_id)
    buddy = Pet(87654321, "Buddy", "Dog", "Golden Retriever", 5, "", "", owner.owner_id)
    scheduler.add_pet(fluffy)
    scheduler.add_pet(buddy)

    morning_task = Task(
        1,
        "Feed Fluffy",
        "feeding",
        datetime(2026, 3, 29, 8, 0),
        "high",
        "pending",
        fluffy.pet_id,
        "once",
    )
    evening_task = Task(
        2,
        "Walk Buddy",
        "walking",
        datetime(2026, 3, 29, 18, 0),
        "medium",
        "pending",
        buddy.pet_id,
        "once",
    )
    scheduler.schedule_task(morning_task)
    scheduler.schedule_task(evening_task)

    warnings = scheduler.detect_conflicts()

    assert warnings == []


def test_owner_save_and_load_round_trip() -> None:
    owner = Owner(96003110, "Alice", "alice@example.com", "217-555-1234")
    pet = Pet(12345678, "Fluffy", "Cat", "Persian", 10, "High-quality cat food", "None", owner.owner_id)
    task = Task(
        1,
        "Feed Fluffy",
        "feeding",
        datetime(2026, 3, 29, 8, 0),
        "high",
        "pending",
        pet.pet_id,
        "daily",
    )
    pet.add_task(task)
    owner.add_pet(pet)

    file_path = Path("test_owner_round_trip_data.json")
    if file_path.exists():
        file_path.unlink()

    try:
        owner.save_to_json(file_path)

        loaded_owner = Owner.load_from_json(file_path)
        scheduler = Scheduler()
        scheduler.add_owner(loaded_owner)

        assert loaded_owner.owner_id == owner.owner_id
        assert loaded_owner.name == owner.name
        assert loaded_owner.email == owner.email
        assert loaded_owner.phone == owner.phone
        assert loaded_owner.view_pets()[0].name == "Fluffy"
        assert loaded_owner.view_pets()[0].view_tasks()[0].due_time == datetime(2026, 3, 29, 8, 0)
        assert loaded_owner.view_pets()[0].view_tasks()[0].frequency == "daily"
        assert scheduler.find_pet(12345678) is not None
        assert scheduler.get_all_tasks()[0].title == "Feed Fluffy"
    finally:
        if file_path.exists():
            file_path.unlink()
