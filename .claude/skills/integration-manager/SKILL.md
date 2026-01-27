---
name: integration-manager
description: |
  Webhook and external integration management. Use this skill when the user wants to
  set up webhooks, manage event delivery, or connect to external systems.
allowed-tools:
  - Bash
  - Read
  - Write
  - AskUserQuestion
---

# Integration Manager Skill

Manages webhook endpoints, event delivery, and external system integration.

## When to Use

- User wants to set up webhooks for notifications
- User needs to integrate with external tools (Slack, CRM, etc.)
- User wants to view webhook delivery history
- User needs to retry failed webhook deliveries

## Core Operations

```bash
python .claude/scripts/webhook_api.py register "https://example.com/hook" --events workflow.completed,email.replied
python .claude/scripts/webhook_api.py list
python .claude/scripts/webhook_api.py test WEBHOOK_ID
python .claude/scripts/webhook_api.py history WEBHOOK_ID
python .claude/scripts/webhook_api.py delete WEBHOOK_ID
```

## Audit Trail

All webhook events are logged via `audit_logger.py` with hash-chained integrity.
