from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Task:
    task_id: int
    title: str
    task_type: str
    due_time: datetime
    priority: str
    status: str
    pet_id: int

    def mark_complete(self) -> None:
        """Mark this task as complete."""
        pass

    def reschedule(self, new_time: datetime) -> None:
        """Update the due time for this task."""
        pass

    def get_summary(self) -> str:
        """Return a short description of this task."""
        pass


@dataclass
class Pet:
    pet_id: int
    name: str
    species: str
    breed: str
    age: int
    diet_notes: str
    medication_notes: str
    owner_id: int
    tasks: List[Task] = field(default_factory=list)

    def update_profile(
        self,
        name: Optional[str] = None,
        species: Optional[str] = None,
        breed: Optional[str] = None,
        age: Optional[int] = None,
        diet_notes: Optional[str] = None,
        medication_notes: Optional[str] = None,
    ) -> None:
        """Update one or more pet profile fields."""
        pass

    def add_task(self, task: Task) -> None:
        """Attach a care task to this pet."""
        pass

    def view_tasks(self) -> List[Task]:
        """Return all tasks assigned to this pet."""
        pass


class Owner:
    def __init__(
        self,
        owner_id: int,
        name: str,
        email: str,
        phone: str,
    ) -> None:
        self.owner_id = owner_id
        self.name = name
        self.email = email
        self.phone = phone
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's profile."""
        pass

    def remove_pet(self, pet_id: int) -> None:
        """Remove a pet from this owner's profile by id."""
        pass

    def view_pets(self) -> List[Pet]:
        """Return the list of pets for this owner."""
        pass


class Scheduler:
    def __init__(self) -> None:
        self.tasks: List[Task] = []
        self.pets: List[Pet] = []
        self.owners: List[Owner] = []

    def schedule_task(self, task: Task) -> None:
        """Add a new task to the scheduler."""
        pass

    def get_tasks_for_day(self, date: datetime) -> List[Task]:
        """Return tasks scheduled for the provided day."""
        pass

    def get_overdue_tasks(self) -> List[Task]:
        """Return tasks that are overdue and not complete."""
        pass

    def sort_tasks_by_time(self) -> List[Task]:
        """Return tasks sorted by due time."""
        pass
