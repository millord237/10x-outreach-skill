---
name: support-manager
description: |
  Support ticket management with SLA tracking and knowledge base. Use this skill when
  the user needs to create, track, or resolve support tickets, or search the knowledge base.
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
  - AskUserQuestion
---

# Support Manager Skill

Manages support tickets, SLA compliance, and knowledge base search.

## When to Use

- User wants to create or manage support tickets
- User asks about SLA status or overdue items
- User needs to search knowledge base for solutions
- User wants to create tickets from incoming emails

## Core Operations

### Tickets
```bash
python .claude/scripts/ticket_manager.py create "Subject" --priority P2 --category incident
python .claude/scripts/ticket_manager.py assign TICKET_ID --to agent_name
python .claude/scripts/ticket_manager.py status TICKET_ID --status in_progress
python .claude/scripts/ticket_manager.py close TICKET_ID --resolution "Fixed"
python .claude/scripts/ticket_manager.py dashboard
```

### SLA
```bash
python .claude/scripts/sla_tracker.py check
python .claude/scripts/sla_tracker.py report
```

### Knowledge Base
```bash
python .claude/scripts/knowledge_base.py search "OAuth token expired"
python .claude/scripts/knowledge_base.py add --title "Fix" --content "Steps..." --tags "auth,oauth"
```

### Email-to-Ticket
```bash
python .claude/scripts/ai_context_analyzer.py analyze --email-id EMAIL_ID
```

## Agent

The `support-router` agent (`.claude/agents/support-router.md`) auto-categorizes incoming issues and routes to the right handler.
