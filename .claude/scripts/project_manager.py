#!/usr/bin/env python3
"""
Project Manager — Task board, sprints, assignments, and status reports.

Usage:
  python project_manager.py dashboard
  python project_manager.py create "Project Name" [--description "desc"]
  python project_manager.py list
  python project_manager.py view <project_id>
  python project_manager.py task add <project_id> "Task title" [--priority high] [--assign skill-name]
  python project_manager.py task list <project_id>
  python project_manager.py task status <task_id> --status <status>
  python project_manager.py task assign <task_id> --to <skill>
  python project_manager.py sprint create <project_id> --name "Sprint 1" --days 7
  python project_manager.py sprint view <sprint_id>
  python project_manager.py standup
  python project_manager.py report <project_id>
  python project_manager.py milestone <project_id> "Milestone title" --due YYYY-MM-DD

Data stored in: output/projects/
"""

import argparse
import json
import sys
import uuid
from datetime import datetime, timedelta, date
from pathlib import Path
from typing import Dict, List, Optional

DATA_DIR = Path("output/projects")
PROJECTS_FILE = DATA_DIR / "projects.json"
TASKS_FILE = DATA_DIR / "tasks.json"
SPRINTS_FILE = DATA_DIR / "sprints.json"

TASK_STATUSES = ["backlog", "todo", "in_progress", "review", "done"]
PRIORITIES = ["low", "medium", "high", "critical"]


def _ensure_dirs():
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def _load(filepath: Path) -> list:
    if filepath.exists():
        return json.loads(filepath.read_text())
    return []


def _save(filepath: Path, data: list):
    _ensure_dirs()
    filepath.write_text(json.dumps(data, indent=2, default=str))


def _gen_id() -> str:
    return str(uuid.uuid4())[:8]


# ─── Projects ────────────────────────────────────────────────────────────────

def create_project(name: str, description: str = "") -> Dict:
    projects = _load(PROJECTS_FILE)
    project = {
        "id": _gen_id(),
        "name": name,
        "description": description,
        "status": "active",
        "created_at": datetime.now().isoformat(),
        "milestones": [],
    }
    projects.append(project)
    _save(PROJECTS_FILE, projects)
    return project


def list_projects() -> List[Dict]:
    projects = _load(PROJECTS_FILE)
    tasks = _load(TASKS_FILE)
    for p in projects:
        project_tasks = [t for t in tasks if t.get("project_id") == p["id"]]
        p["task_count"] = len(project_tasks)
        p["done_count"] = sum(1 for t in project_tasks if t.get("status") == "done")
        p["progress"] = round(p["done_count"] / p["task_count"] * 100) if p["task_count"] > 0 else 0
    return projects


def add_milestone(project_id: str, title: str, due: str) -> Optional[Dict]:
    projects = _load(PROJECTS_FILE)
    for p in projects:
        if p["id"] == project_id:
            milestone = {"id": _gen_id(), "title": title, "due": due, "status": "pending"}
            p.setdefault("milestones", []).append(milestone)
            _save(PROJECTS_FILE, projects)
            return milestone
    return None


# ─── Tasks ───────────────────────────────────────────────────────────────────

def add_task(project_id: str, title: str, priority: str = "medium", assignee: str = "") -> Dict:
    tasks = _load(TASKS_FILE)
    task = {
        "id": _gen_id(),
        "project_id": project_id,
        "title": title,
        "priority": priority,
        "status": "backlog",
        "assignee": assignee,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
    }
    tasks.append(task)
    _save(TASKS_FILE, tasks)
    return task


def update_task_status(task_id: str, status: str) -> Optional[Dict]:
    tasks = _load(TASKS_FILE)
    for t in tasks:
        if t["id"] == task_id:
            t["status"] = status
            t["updated_at"] = datetime.now().isoformat()
            if status == "done":
                t["completed_at"] = datetime.now().isoformat()
            _save(TASKS_FILE, tasks)
            return t
    return None


def assign_task(task_id: str, assignee: str) -> Optional[Dict]:
    tasks = _load(TASKS_FILE)
    for t in tasks:
        if t["id"] == task_id:
            t["assignee"] = assignee
            t["updated_at"] = datetime.now().isoformat()
            _save(TASKS_FILE, tasks)
            return t
    return None


def list_tasks(project_id: str) -> List[Dict]:
    tasks = _load(TASKS_FILE)
    return [t for t in tasks if t.get("project_id") == project_id]


# ─── Sprints ─────────────────────────────────────────────────────────────────

def create_sprint(project_id: str, name: str, days: int = 7) -> Dict:
    sprints = _load(SPRINTS_FILE)
    start = date.today()
    end = start + timedelta(days=days)
    sprint = {
        "id": _gen_id(),
        "project_id": project_id,
        "name": name,
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "status": "active",
        "task_ids": [],
    }
    sprints.append(sprint)
    _save(SPRINTS_FILE, sprints)
    return sprint


# ─── Reports ─────────────────────────────────────────────────────────────────

def standup() -> Dict:
    tasks = _load(TASKS_FILE)
    today = date.today().isoformat()
    yesterday = (date.today() - timedelta(days=1)).isoformat()

    done_yesterday = [t for t in tasks if t.get("completed_at", "")[:10] == yesterday]
    in_progress = [t for t in tasks if t.get("status") == "in_progress"]
    blocked = [t for t in tasks if t.get("status") == "review"]

    return {
        "date": today,
        "done_yesterday": [{"title": t["title"], "assignee": t.get("assignee", "")} for t in done_yesterday],
        "in_progress_today": [{"title": t["title"], "assignee": t.get("assignee", "")} for t in in_progress],
        "in_review": [{"title": t["title"], "assignee": t.get("assignee", "")} for t in blocked],
        "total_backlog": sum(1 for t in tasks if t.get("status") == "backlog"),
    }


def project_report(project_id: str) -> Dict:
    projects = _load(PROJECTS_FILE)
    tasks = _load(TASKS_FILE)

    project = next((p for p in projects if p["id"] == project_id), None)
    if not project:
        return {"error": "Project not found"}

    project_tasks = [t for t in tasks if t.get("project_id") == project_id]
    by_status = {}
    for t in project_tasks:
        s = t.get("status", "backlog")
        by_status.setdefault(s, []).append(t["title"])

    return {
        "project": project["name"],
        "total_tasks": len(project_tasks),
        "by_status": {s: len(items) for s, items in by_status.items()},
        "progress": round(len(by_status.get("done", [])) / len(project_tasks) * 100) if project_tasks else 0,
        "milestones": project.get("milestones", []),
        "by_assignee": _count_by(project_tasks, "assignee"),
    }


def _count_by(items: list, key: str) -> Dict:
    counts = {}
    for item in items:
        val = item.get(key, "unassigned") or "unassigned"
        counts[val] = counts.get(val, 0) + 1
    return counts


def dashboard() -> Dict:
    projects = list_projects()
    tasks = _load(TASKS_FILE)
    return {
        "active_projects": len([p for p in projects if p.get("status") == "active"]),
        "total_tasks": len(tasks),
        "tasks_in_progress": sum(1 for t in tasks if t.get("status") == "in_progress"),
        "tasks_done_today": sum(1 for t in tasks if t.get("completed_at", "")[:10] == date.today().isoformat()),
        "projects": [{"id": p["id"], "name": p["name"], "progress": p.get("progress", 0)} for p in projects[:10]],
    }


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Project Manager")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("dashboard")

    sp = subparsers.add_parser("create")
    sp.add_argument("name")
    sp.add_argument("--description", default="")

    subparsers.add_parser("list")

    sp = subparsers.add_parser("view")
    sp.add_argument("id")

    # Task subcommands
    task_parser = subparsers.add_parser("task")
    task_sub = task_parser.add_subparsers(dest="task_action")

    sp = task_sub.add_parser("add")
    sp.add_argument("project_id")
    sp.add_argument("title")
    sp.add_argument("--priority", default="medium", choices=PRIORITIES)
    sp.add_argument("--assign", default="")

    sp = task_sub.add_parser("list")
    sp.add_argument("project_id")

    sp = task_sub.add_parser("status")
    sp.add_argument("task_id")
    sp.add_argument("--status", required=True, choices=TASK_STATUSES)

    sp = task_sub.add_parser("assign")
    sp.add_argument("task_id")
    sp.add_argument("--to", required=True, dest="assignee")

    # Sprint subcommands
    sprint_parser = subparsers.add_parser("sprint")
    sprint_sub = sprint_parser.add_subparsers(dest="sprint_action")

    sp = sprint_sub.add_parser("create")
    sp.add_argument("project_id")
    sp.add_argument("--name", required=True)
    sp.add_argument("--days", type=int, default=7)

    subparsers.add_parser("standup")

    sp = subparsers.add_parser("report")
    sp.add_argument("project_id")

    sp = subparsers.add_parser("milestone")
    sp.add_argument("project_id")
    sp.add_argument("title")
    sp.add_argument("--due", required=True)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    result = None

    if args.command == "dashboard":
        result = dashboard()
    elif args.command == "create":
        result = create_project(args.name, args.description)
    elif args.command == "list":
        result = list_projects()
    elif args.command == "view":
        result = project_report(args.id)
    elif args.command == "task":
        if args.task_action == "add":
            result = add_task(args.project_id, args.title, args.priority, args.assign)
        elif args.task_action == "list":
            result = list_tasks(args.project_id)
        elif args.task_action == "status":
            result = update_task_status(args.task_id, args.status)
        elif args.task_action == "assign":
            result = assign_task(args.task_id, args.assignee)
    elif args.command == "sprint":
        if args.sprint_action == "create":
            result = create_sprint(args.project_id, args.name, args.days)
    elif args.command == "standup":
        result = standup()
    elif args.command == "report":
        result = project_report(args.project_id)
    elif args.command == "milestone":
        result = add_milestone(args.project_id, args.title, args.due)

    if result is not None:
        print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
