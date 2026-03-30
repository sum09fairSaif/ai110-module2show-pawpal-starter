from datetime import datetime

from pawpal_system import *

Owner1 = Owner(96003110, "Alice", "alice@yahoo.com", "217-555-1234")
Pet1 = Pet(12345678, "Fluffy", "Cat", "Persian", 10, "High-quality cat food, Raw fish, Milk", "None", Owner1.owner_id)
Pet2 = Pet(87654321, "Buddy", "Dog", "Golden Retriever", 5, "High-quality dog food, Raw meat, Dog treats", "None", Owner1.owner_id)
Task1 = Task(
    1,
    "Feed Fluffy 1 cup of high-quality cat food and 1/4 cup of raw fish.",
    "feeding",
    datetime.strptime("2026-03-29 08:00", "%Y-%m-%d %H:%M"),
    "high",
    "pending",
    Pet1.pet_id,
    "once",
)
Task2 = Task(
    2,
    "Take Buddy for a 30-minute walk in the park.",
    "walking",
    datetime.strptime("2026-03-29 18:00", "%Y-%m-%d %H:%M"),
    "medium",
    "pending",
    Pet2.pet_id,
    "daily",
)
Task3 = Task(
    3,
    "Take Fluffy to the vet for a check-up.",
    "vet appointment",
    datetime.strptime("2026-03-29 10:00", "%Y-%m-%d %H:%M"),
    "critical",
    "pending",
    Pet1.pet_id,
    "once",
)
print("Today's Schedule:")
print("-" * 50)

for task in [Task1, Task2, Task3]:
    print(f"Pet ID    : {task.pet_id}")
    print(f"Title     : {task.title}")
    print(f"Due Time  : {task.due_time.strftime('%Y-%m-%d %H:%M')}")
    print(f"Frequency : {task.frequency}")
    print(f"Priority  : {task.priority}")
    print(f"Status    : {task.status}")
    print("-" * 50)
