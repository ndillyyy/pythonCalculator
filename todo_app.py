#!/usr/bin/env python3
"""
Task 1: Command-Line To-Do List Application
Stores tasks in JSON format with add, delete, complete, and list functionality.
"""

import json
import os
import sys
from datetime import datetime

TASKS_FILE = "tasks.json"


def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Warning: tasks file corrupted. Starting fresh.")
        return []


def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


def add_task(title):
    tasks = load_tasks()
    task = {
        "id": (max((t["id"] for t in tasks), default=0) + 1),
        "title": title,
        "done": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"✅ Added task #{task['id']}: {title}")


def delete_task(task_id):
    tasks = load_tasks()
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        print(f"❌ Error: Task #{task_id} does not exist.")
        return
    tasks = [t for t in tasks if t["id"] != task_id]
    save_tasks(tasks)
    print(f"🗑️  Deleted task #{task_id}: {task['title']}")


def mark_done(task_id):
    tasks = load_tasks()
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        print(f"❌ Error: Task #{task_id} does not exist.")
        return
    if task["done"]:
        print(f"ℹ️  Task #{task_id} is already marked as done.")
        return
    task["done"] = True
    save_tasks(tasks)
    print(f"✔️  Marked task #{task_id} as done: {task['title']}")


def list_tasks(show_all=True):
    tasks = load_tasks()
    if not tasks:
        print("📋 No tasks found.")
        return
    print(f"\n{'ID':<5} {'Status':<10} {'Created':<22} {'Title'}")
    print("-" * 65)
    for t in tasks:
        if not show_all and t["done"]:
            continue
        status = "✔ Done" if t["done"] else "○ Todo"
        print(f"{t['id']:<5} {status:<10} {t['created_at']:<22} {t['title']}")
    print()


def print_help():
    print("""
Usage: python todo_app.py <command> [args]

Commands:
  add <title>       Add a new task
  delete <id>       Delete a task by ID
  done <id>         Mark a task as completed
  list              List all tasks
  list pending      List only pending tasks
  help              Show this help message
""")


def main():
    if len(sys.argv) < 2:
        print_help()
        return

    cmd = sys.argv[1].lower()

    if cmd == "add":
        if len(sys.argv) < 3:
            print("Usage: python todo_app.py add <title>")
            return
        add_task(" ".join(sys.argv[2:]))

    elif cmd == "delete":
        if len(sys.argv) < 3 or not sys.argv[2].isdigit():
            print("Usage: python todo_app.py delete <id>")
            return
        delete_task(int(sys.argv[2]))

    elif cmd == "done":
        if len(sys.argv) < 3 or not sys.argv[2].isdigit():
            print("Usage: python todo_app.py done <id>")
            return
        mark_done(int(sys.argv[2]))

    elif cmd == "list":
        pending_only = len(sys.argv) > 2 and sys.argv[2].lower() == "pending"
        list_tasks(show_all=not pending_only)

    elif cmd == "help":
        print_help()

    else:
        print(f"Unknown command: '{cmd}'")
        print_help()


if __name__ == "__main__":
    main()