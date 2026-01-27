---
name: project-manager
description: |
  Project management with task assignment, sprint planning, and status reporting.
  Use this skill when the user wants to organize work, track progress, or manage deadlines.
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
  - AskUserQuestion
---

# Project Manager Skill

Organizes work into projects, assigns tasks, tracks sprints, and generates status reports.

## When to Use

- User wants to plan a campaign or project
- User asks for task tracking or progress updates
- User needs a standup or status report
- User wants to organize work across multiple skills

## Core Operations

### Projects
```bash
python .claude/scripts/project_manager.py create "Q1 Outreach" --description "B2B outreach to AI startups"
python .claude/scripts/project_manager.py list
python .claude/scripts/project_manager.py view PROJECT_ID
```

### Tasks
```bash
python .claude/scripts/project_manager.py task add PROJECT_ID "Research AI founders" --priority high --assign discovery-engine
python .claude/scripts/project_manager.py task status TASK_ID --status in_progress
python .claude/scripts/project_manager.py task list PROJECT_ID
```

### Sprints
```bash
python .claude/scripts/project_manager.py sprint create PROJECT_ID --name "Sprint 1" --days 7
python .claude/scripts/project_manager.py sprint view SPRINT_ID
```

### Reports
```bash
python .claude/scripts/project_manager.py standup
python .claude/scripts/project_manager.py report PROJECT_ID
```

## Data Storage

- `output/projects/projects.json` — Project database
- `output/projects/tasks.json` — Task board
- `output/projects/sprints.json` — Sprint data

## Agent

The `project-coordinator` agent (`.claude/agents/project-coordinator.md`) orchestrates multi-skill task sequences and tracks dependencies.
