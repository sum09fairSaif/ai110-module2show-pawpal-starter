# PawPal+ Project Reflection

## 1. System Design

### Three (3) Core Actions that can be done on the PawPal+ App

- Be able to enter and store relevant, important information about the owner and the pet they own.
- Keep track of every dietary habits and nutritional needs (what the pet has for breakfast, lunch, dinner, midday/late afternoon snack, midnight meals, etc.), as well as any medications they have to take in on a regular basis
- Any vaccinations they need to take, they are yet to take, they have already taken, and any appointments pending and upcoming, and completed, with the veterinarian

**a. Initial design**

- My initial UML design used four main classes: `Owner`, `Pet`, `Task`, and `Scheduler`.
- The `Owner` class is responsible for storing the pet owner's account and contact information, as well as keeping track of the pets they manage.
- The `Pet` class represents each individual pet and stores details such as its name, type, age, dietary notes, medication reminders, and task history.
- The `Task` class represents a care activity that needs to happen for a pet, such as feeding, walking, giving medicine, or attending a vet visit. It stores the due time, status, priority, and task type.
- The `Scheduler` class coordinates all tasks. Its job is to add tasks, organize them by date and time, and generate the list of tasks due for a particular day.

### Building Blocks

#### `Owner`

- Attributes: `owner_id`, `name`, `email`, `phone`, `pets`
- Methods: `add_pet()`, `remove_pet()`, `view_pets()`

#### `Pet`

- Attributes: `pet_id`, `name`, `species`, `breed`, `age`, `diet_notes`, `medication_notes`, `owner_id`
- Methods: `update_profile()`, `add_task()`, `view_tasks()`

#### `Task`

- Attributes: `task_id`, `title`, `task_type`, `due_time`, `priority`, `status`, `pet_id`
- Methods: `mark_complete()`, `reschedule()`, `get_summary()`

#### `Scheduler`

- Attributes: `tasks`, `pets`, `owners`
- Methods: `schedule_task()`, `get_tasks_for_day()`, `get_overdue_tasks()`, `sort_tasks_by_time()`

### Mermaid UML Draft

```mermaid
classDiagram
    class Owner {
        +int owner_id
        +string name
        +string email
        +string phone
        +list pets
        +add_pet(pet)
        +remove_pet(pet_id)
        +view_pets()
    }

    class Pet {
        +int pet_id
        +string name
        +string species
        +string breed
        +int age
        +string diet_notes
        +string medication_notes
        +int owner_id
        +update_profile()
        +add_task(task)
        +view_tasks()
    }

    class Task {
        +int task_id
        +string title
        +string task_type
        +datetime due_time
        +string priority
        +string status
        +int pet_id
        +mark_complete()
        +reschedule(new_time)
        +get_summary()
    }

    class Scheduler {
        +list tasks
        +list pets
        +list owners
        +schedule_task(task)
        +get_tasks_for_day(date)
        +get_overdue_tasks()
        +sort_tasks_by_time()
    }

    Owner "1" --> "*" Pet : owns
    Pet "1" --> "*" Task : has
    Scheduler --> Owner : manages
    Scheduler --> Pet : tracks
    Scheduler --> Task : organizes
```

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
