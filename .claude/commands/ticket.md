---
name: ticket
description: Support ticket management with SLA tracking
---

# /ticket Command

Create, manage, and resolve support tickets with SLA monitoring and knowledge base search.

## Usage

```
/ticket [action]
```

### Actions

- `/ticket` — Open tickets dashboard (sorted by priority)
- `/ticket create <subject>` — Create a new ticket
- `/ticket view <id>` — View ticket details
- `/ticket assign <id> --to <agent>` — Assign ticket to agent
- `/ticket status <id> --status <status>` — Update ticket status
- `/ticket comment <id> <comment>` — Add comment to ticket
- `/ticket close <id> --resolution <text>` — Close with resolution
- `/ticket sla` — View SLA status for all open tickets
- `/ticket search <query>` — Search tickets
- `/ticket kb <query>` — Search knowledge base for solutions
- `/ticket from-email <email_id>` — Create ticket from an email
- `/ticket report` — Generate support metrics report
- `/ticket escalate <id>` — Escalate ticket to higher priority

## Ticket Fields

| Field | Description |
|-------|-------------|
| subject | Ticket title |
| description | Full description |
| priority | P1 (critical), P2 (high), P3 (medium), P4 (low) |
| status | new, open, in_progress, pending, resolved, closed |
| assignee | Assigned agent/skill |
| category | incident, request, change, problem |
| source | email, manual, workflow, webhook |
| email_id | Linked email (if created from email) |

## SLA Targets

| Priority | Response Time | Resolution Time |
|----------|--------------|-----------------|
| P1 (Critical) | 1 hour | 4 hours |
| P2 (High) | 4 hours | 8 hours |
| P3 (Medium) | 8 hours | 2 days |
| P4 (Low) | 24 hours | 7 days |

## Knowledge Base

Search existing solutions before creating new tickets:
```
/ticket kb "OAuth token expired"
/ticket kb "email delivery failed"
```

## Integration

- `/inbox` can auto-create tickets from incoming emails
- `/ops` monitors ticket SLA compliance
- `/analytics` includes support metrics
- `ai_context_analyzer.py` auto-categorizes and prioritizes

## Implementation

```bash
python .claude/scripts/ticket_manager.py dashboard
python .claude/scripts/ticket_manager.py create "Login issues reported" --priority P2 --category incident
python .claude/scripts/ticket_manager.py assign TICKET_ID --to support-manager
python .claude/scripts/ticket_manager.py status TICKET_ID --status in_progress
python .claude/scripts/ticket_manager.py comment TICKET_ID "Investigating root cause"
python .claude/scripts/ticket_manager.py close TICKET_ID --resolution "Fixed OAuth token refresh"
python .claude/scripts/sla_tracker.py check
python .claude/scripts/knowledge_base.py search "OAuth token"
```

## Skill Reference

This command uses the `support-manager` skill at `.claude/skills/support-manager/SKILL.md`.
Agent: `support-router` at `.claude/agents/support-router.md`.
