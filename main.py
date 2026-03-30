from datetime import datetime

from pawpal_system import Owner, Pet, Scheduler, Task


def print_tasks(label: str, tasks: list[Task]) -> None:
    print(label)
    print("-" * 50)
    for task in tasks:
        print(f"Pet ID    : {task.pet_id}")
        print(f"Title     : {task.title}")
        print(f"Due Time  : {task.due_time.strftime('%Y-%m-%d %H:%M')}")
        print(f"Frequency : {task.frequency}")
        print(f"Priority  : {task.priority}")
        print(f"Status    : {task.status}")
        print("-" * 50)


def main() -> None:
    scheduler = Scheduler()

    owner = Owner(96003110, "Alice", "alice@yahoo.com", "217-555-1234")
    scheduler.add_owner(owner)

    fluffy = Pet(
        12345678,
        "Fluffy",
        "Cat",
        "Persian",
        10,
        "High-quality cat food, Raw fish, Milk",
        "None",
        owner.owner_id,
    )
    buddy = Pet(
        87654321,
        "Buddy",
        "Dog",
        "Golden Retriever",
        5,
        "High-quality dog food, Raw meat, Dog treats",
        "None",
        owner.owner_id,
    )

    scheduler.add_pet(fluffy)
    scheduler.add_pet(buddy)

    # Add tasks out of chronological order so sorting can be verified in the terminal.
    task1 = Task(
        1,
        "Take Buddy for a 30-minute walk in the park.",
        "walking",
        datetime.strptime("2026-03-29 18:00", "%Y-%m-%d %H:%M"),
        "medium",
        "pending",
        buddy.pet_id,
        "daily",
    )
    task2 = Task(
        2,
        "Feed Fluffy 1 cup of high-quality cat food and 1/4 cup of raw fish.",
        "feeding",
        datetime.strptime("2026-03-29 08:00", "%Y-%m-%d %H:%M"),
        "high",
        "complete",
        fluffy.pet_id,
        "once",
    )
    task3 = Task(
        3,
        "Take Fluffy to the vet for a check-up.",
        "vet appointment",
        datetime.strptime("2026-03-29 10:00", "%Y-%m-%d %H:%M"),
        "critical",
        "pending",
        fluffy.pet_id,
        "once",
    )
    task4 = Task(
        4,
        "Give Buddy his morning medication.",
        "medication",
        datetime.strptime("2026-03-29 10:00", "%Y-%m-%d %H:%M"),
        "high",
        "pending",
        buddy.pet_id,
        "weekly",
    )

    for task in [task1, task2, task3, task4]:
        scheduler.schedule_task(task)

    print_tasks("All Tasks (Added Out of Order):", scheduler.get_all_tasks())
    print_tasks("Tasks Sorted By Time:", scheduler.sort_tasks_by_time())
    print_tasks("Pending Tasks:", scheduler.filter_tasks(status="pending"))
    print_tasks("Tasks For Fluffy:", scheduler.filter_tasks(pet_name="fluffy"))

    print("Conflict Warnings:")
    print("-" * 50)
    warnings = scheduler.detect_conflicts()
    if warnings:
        for warning in warnings:
            print(warning)
    else:
        print("No conflicts found.")
    print("-" * 50)

    next_task = scheduler.mark_task_complete(4)
    if next_task is not None:
        print("Recurring Task Created:")
        print("-" * 50)
        print(f"New Task ID: {next_task.task_id}")
        print(f"Title      : {next_task.title}")
        print(f"Due Time   : {next_task.due_time.strftime('%Y-%m-%d %H:%M')}")
        print(f"Frequency  : {next_task.frequency}")
        print(f"Status     : {next_task.status}")
        print("-" * 50)


if __name__ == "__main__":
    main()
