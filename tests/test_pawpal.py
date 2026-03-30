from datetime import datetime

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


def test_sort_tasks_by_time_returns_chronological_order() -> None:
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
    earliest_task = Task(
        2,
        "Breakfast",
        "feeding",
        datetime(2026, 3, 29, 7, 0),
        "high",
        "pending",
        fluffy.pet_id,
        "once",
    )
    middle_task = Task(
        3,
        "Lunch meds",
        "medication",
        datetime(2026, 3, 29, 12, 0),
        "high",
        "pending",
        fluffy.pet_id,
        "once",
    )

    scheduler.schedule_task(later_task)
    scheduler.schedule_task(earliest_task)
    scheduler.schedule_task(middle_task)

    sorted_tasks = scheduler.sort_tasks_by_time()

    assert sorted_tasks == [earliest_task, middle_task, later_task]


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
