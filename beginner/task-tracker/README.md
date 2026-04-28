# Task Tracker

Source: [roadmap.sh/projects/task-tracker](https://roadmap.sh/projects/task-tracker)

A CLI app to create, update, and track tasks stored in a local JSON file. No external libraries -- just the language's native filesystem module.

## Requirements

The app runs from the command line and accepts user actions as positional arguments. Tasks are persisted to a `tasks.json` file in the current directory, which should be created automatically if it doesn't exist.

Users must be able to:

- Add, update, and delete tasks
- Mark a task as in-progress or done
- List all tasks, or filter by status (`todo`, `in-progress`, `done`)

Constraints:

- Positional arguments only for CLI inputs
- No external libraries or frameworks
- Use the language's native filesystem module for all file operations
- Handle errors and edge cases gracefully

## Task Schema

Each task stored in the JSON file should have the following properties:

| Property | Type | Description |
|----------|------|-------------|
| `id` | number | Unique identifier |
| `description` | string | Short description of the task |
| `status` | string | `todo`, `in-progress`, or `done` |
| `createdAt` | datetime | Timestamp when the task was created |
| `updatedAt` | datetime | Timestamp when the task was last updated |

## Commands

```bash
# Add a task
task-cli add "Buy groceries"
# Output: Task added successfully (ID: 1)

# Update and delete
task-cli update 1 "Buy groceries and cook dinner"
task-cli delete 1

# Change status
task-cli mark-in-progress 1
task-cli mark-done 1

# List tasks
task-cli list
task-cli list done
task-cli list todo
task-cli list in-progress
```
