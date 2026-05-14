# ToDo

Python CLI task manager organized by projects. Each project is a directory under `Projects/` containing a `tasks.json` file.

## Setup

```bash
pip install rich
```

## Run

```bash
python main.py
```

## Architecture

- `main.py` — CLI entrypoint with project manager and task editor menus
- `project.py` — `Project` class: CRUD for project directories under `Projects/`
- `todo.py` — `ToDoList` class: CRUD for tasks stored as JSON in a project's `tasks.json`
- `AppData/system.log` — logging destination (gitignored)

Tasks are JSON objects with keys: `title`, `status`, `description`, `preconditions`, `reproduction_steps`, `actual`, `expected`, `priority`. Statuses: `New`, `Pending`, `On Hold`, `Complete`.

## Gotchas

- No tests, no linter, no formatter, no type checker configured
- Uses `console.clear()` (rich) for screen clearing — no external `clear` dependency
- `DISPLAY_COUNT` is a module-level global in `todo.py` used as a display-index counter across status columns
- Task indexes in the UI are 1-based display positions (not array indices); `get_task_index_from_display_selection()` maps them back
- Both `Projects/` and `AppData/` are gitignored — fresh clone has no data
- Only dependency outside stdlib is `rich` (includes `rich.table.Table` used for task display)
