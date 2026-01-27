---
name: webhook
description: Manage webhooks and external integrations
---

# /webhook Command

Register webhook endpoints, manage event delivery, and integrate with external systems.

## Usage

```
/webhook [action]
```

### Actions

- `/webhook` — List all registered webhooks
- `/webhook register <url> --events <events>` — Register a new webhook
- `/webhook test <id>` — Send test event to webhook
- `/webhook history <id>` — View delivery history
- `/webhook delete <id>` — Remove a webhook
- `/webhook events` — List all available event types
- `/webhook retry <delivery_id>` — Retry a failed delivery

## Event Types

| Event | Description |
|-------|-------------|
| `workflow.started` | Workflow execution began |
| `workflow.completed` | Workflow finished successfully |
| `workflow.failed` | Workflow failed |
| `email.sent` | Email sent |
| `email.replied` | Email reply received |
| `email.bounced` | Email bounced |
| `ticket.created` | Support ticket created |
| `ticket.resolved` | Support ticket resolved |
| `campaign.started` | Campaign execution began |
| `campaign.completed` | Campaign finished |
| `platform.action` | Social platform action executed |
| `system.error` | System error occurred |
| `system.rate_limit` | Rate limit warning |

## Webhook Security

- HMAC-SHA256 payload signing
- Signature in `X-Webhook-Signature` header
- Secret key per webhook endpoint
- Automatic retry: 3 attempts with exponential backoff

## Implementation

```bash
python .claude/scripts/webhook_api.py list
python .claude/scripts/webhook_api.py register "https://example.com/hook" --events workflow.completed,email.replied
python .claude/scripts/webhook_api.py test WEBHOOK_ID
python .claude/scripts/webhook_api.py history WEBHOOK_ID
python .claude/scripts/webhook_api.py delete WEBHOOK_ID
```

## Skill Reference

This command uses the `integration-manager` skill at `.claude/skills/integration-manager/SKILL.md`.
