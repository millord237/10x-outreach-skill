---
name: project
description: Project management, task assignment, and sprint planning
---

# /project Command

Manage projects, assign tasks across agents, track progress, and generate status reports.

## Usage

```
/project [action]
```

### Actions

- `/project` — Active projects dashboard
- `/project create <name>` — Create a new project
- `/project list` — List all projects
- `/project view <id>` — View project details, tasks, and progress
- `/project task add <project> <title>` — Add a task to a project
- `/project task assign <task_id> --to <skill>` — Assign task to a skill/agent
- `/project task status <task_id> --status <status>` — Update task status
- `/project sprint create <project> --name <name> --days <n>` — Create a sprint
- `/project standup` — Generate daily standup report
- `/project report <project>` — Full project status report
- `/project milestone <project> <title> --due <date>` — Add milestone

## Task Statuses

```
backlog → todo → in_progress → review → done
```

## Task Assignment

Tasks can be assigned to any skill/agent:
- `discovery-engine` — Research tasks
- `content-marketing` — Content creation
- `outreach-manager` — Campaign execution
- `linkedin-adapter` / `twitter-adapter` / `instagram-adapter` — Platform tasks
- `qa-compliance` — Review tasks
- `account-manager` — Follow-up tasks

## Sprint Structure

| Field | Description |
|-------|-------------|
| name | Sprint name (e.g., "Week 1 Outreach") |
| start_date | Sprint start |
| end_date | Sprint end |
| tasks | Tasks included in sprint |
| velocity | Completed tasks per sprint |

## Reports

- **Daily Standup**: What was done yesterday, what's planned today, blockers
- **Sprint Report**: Tasks completed vs planned, velocity trend
- **Project Report**: Overall progress, milestones, timeline

## Implementation

```bash
python .claude/scripts/project_manager.py dashboard
python .claude/scripts/project_manager.py create "Q1 Outreach Campaign"
python .claude/scripts/project_manager.py task add PROJECT_ID "Research AI founders in SF" --priority high
python .claude/scripts/project_manager.py task assign TASK_ID --to discovery-engine
python .claude/scripts/project_manager.py task status TASK_ID --status in_progress
python .claude/scripts/project_manager.py sprint create PROJECT_ID --name "Sprint 1" --days 7
python .claude/scripts/project_manager.py standup
python .claude/scripts/project_manager.py report PROJECT_ID
```

## Skill Reference

This command uses the `project-manager` skill at `.claude/skills/project-manager/SKILL.md`.
