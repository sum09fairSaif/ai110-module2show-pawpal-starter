from datetime import datetime

from pawpal_system import Pet, Task


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
