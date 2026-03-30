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
    frequency: str = "once"

    def mark_complete(self) -> None:
        """Mark this task as complete."""
        self.status = "complete"

    def reschedule(self, new_time: datetime) -> None:
        """Update the due time for this task."""
        self.due_time = new_time
        if self.status == "complete":
            self.status = "pending"

    def get_summary(self) -> str:
        """Return a short description of this task."""
        return (
            f"{self.title} for pet {self.pet_id} at "
            f"{self.due_time.strftime('%Y-%m-%d %H:%M')} "
            f"({self.frequency}, {self.status})"
        )


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
        if name is not None:
            self.name = name
        if species is not None:
            self.species = species
        if breed is not None:
            self.breed = breed
        if age is not None:
            self.age = age
        if diet_notes is not None:
            self.diet_notes = diet_notes
        if medication_notes is not None:
            self.medication_notes = medication_notes

    def add_task(self, task: Task) -> None:
        """Attach a care task to this pet."""
        if task.pet_id != self.pet_id:
            raise ValueError("Task pet_id must match the pet receiving the task.")
        if any(existing_task.task_id == task.task_id for existing_task in self.tasks):
            raise ValueError(f"Task with id {task.task_id} already exists for this pet.")
        self.tasks.append(task)

    def view_tasks(self) -> List[Task]:
        """Return all tasks assigned to this pet."""
        return list(self.tasks)


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

    def update_profile(
        self,
        name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
    ) -> None:
        """Update one or more owner profile fields."""
        if name is not None:
            self.name = name
        if email is not None:
            self.email = email
        if phone is not None:
            self.phone = phone

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's profile."""
        if pet.owner_id != self.owner_id:
            raise ValueError("Pet owner_id must match the owner receiving the pet.")
        if any(existing_pet.pet_id == pet.pet_id for existing_pet in self.pets):
            raise ValueError(f"Pet with id {pet.pet_id} is already registered.")
        self.pets.append(pet)

    def remove_pet(self, pet_id: int) -> None:
        """Remove a pet from this owner's profile by id."""
        for index, pet in enumerate(self.pets):
            if pet.pet_id == pet_id:
                del self.pets[index]
                return
        raise ValueError(f"Pet with id {pet_id} was not found.")

    def view_pets(self) -> List[Pet]:
        """Return the list of pets for this owner."""
        return list(self.pets)

    def get_all_tasks(self) -> List[Task]:
        """Return every task across all pets owned by this owner."""
        all_tasks: List[Task] = []
        for pet in self.pets:
            all_tasks.extend(pet.view_tasks())
        return all_tasks


class Scheduler:
    def __init__(self) -> None:
        self.tasks: List[Task] = []
        self.pets: List[Pet] = []
        self.owners: List[Owner] = []

    def add_owner(self, owner: Owner) -> None:
        """Register an owner with the scheduler."""
        if self.find_owner(owner.owner_id) is not None:
            raise ValueError(f"Owner with id {owner.owner_id} is already registered.")
        self.owners.append(owner)
        self._sync_tasks()

    def add_pet(self, pet: Pet) -> None:
        """Register a pet with the scheduler."""
        owner = self.find_owner(pet.owner_id)
        if owner is None:
            raise ValueError("Pet cannot be registered without a matching owner.")
        owner.add_pet(pet)
        self._sync_tasks()

    def find_owner(self, owner_id: int) -> Optional[Owner]:
        """Find a registered owner by id."""
        for owner in self.owners:
            if owner.owner_id == owner_id:
                return owner
        return None

    def find_pet(self, pet_id: int) -> Optional[Pet]:
        """Find a registered pet by id."""
        for pet in self.pets:
            if pet.pet_id == pet_id:
                return pet
        return None

    def schedule_task(self, task: Task) -> None:
        """Add a new task to the scheduler."""
        pet = self.find_pet(task.pet_id)
        if pet is None:
            raise ValueError("Task cannot be scheduled for an unknown pet.")
        if any(existing_task.task_id == task.task_id for existing_task in self.tasks):
            raise ValueError(f"Task with id {task.task_id} is already scheduled.")

        pet.add_task(task)
        self._sync_tasks()

    def get_all_tasks(self) -> List[Task]:
        """Return every task across all registered owners and pets."""
        self._sync_tasks()
        return list(self.tasks)

    def get_tasks_for_day(self, date: datetime) -> List[Task]:
        """Return tasks scheduled for the provided day."""
        return [
            task
            for task in self.get_all_tasks()
            if task.due_time.date() == date.date()
        ]

    def get_overdue_tasks(self) -> List[Task]:
        """Return tasks that are overdue and not complete."""
        now = datetime.now()
        return [
            task
            for task in self.get_all_tasks()
            if task.due_time < now and task.status != "complete"
        ]

    def sort_tasks_by_time(self) -> List[Task]:
        """Return tasks sorted by due time."""
        return sorted(self.get_all_tasks(), key=lambda task: task.due_time)

    def _sync_tasks(self) -> None:
        """Rebuild the scheduler's task list from each owner's pets."""
        synced_tasks: List[Task] = []
        synced_pets: List[Pet] = []

        for owner in self.owners:
            for pet in owner.view_pets():
                synced_pets.append(pet)
                synced_tasks.extend(pet.view_tasks())

        self.pets = synced_pets
        self.tasks = synced_tasks
