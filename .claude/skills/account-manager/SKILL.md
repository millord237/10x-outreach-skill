---
name: account-manager
description: |
  CRM-style contact and deal pipeline management. Use this skill when the user wants to
  manage contacts, track deals, schedule follow-ups, or export contact lists.
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
  - AskUserQuestion
---

# Account Manager Skill

Manages contacts, deal pipelines, and follow-up scheduling like a lightweight CRM.

## When to Use

- User wants to add, view, or search contacts
- User asks about deal pipeline or sales stages
- User needs to schedule or check follow-ups
- User wants to import/export contacts
- User asks "who should I follow up with?"

## When NOT to Use

- Finding new people → use `discovery-engine`
- Sending emails → use `outreach-manager` or `email-composer`
- Platform actions → use platform adapters

## Core Operations

### Add Contact
```bash
python .claude/scripts/account_manager.py add "Name" --email e@co.com --company "Co" --role "CTO" --source exa --tags "ai,founder"
```

### Pipeline Management
```bash
python .claude/scripts/account_manager.py deal CONTACT_ID --stage qualified --value 25000
python .claude/scripts/account_manager.py pipeline
```

### Follow-ups
```bash
python .claude/scripts/account_manager.py followup CONTACT_ID --date 2026-02-01 --note "Send case study"
python .claude/scripts/account_manager.py overdue
```

### Search & Export
```bash
python .claude/scripts/account_manager.py search "CTO ai startup"
python .claude/scripts/account_manager.py export --format csv --output output/contacts.csv
```

## Data Storage

- `output/accounts/contacts.json` — Contact database
- `output/accounts/deals.json` — Deal pipeline
- `output/accounts/followups.json` — Scheduled follow-ups

## Integration Points

- `discovery-engine` → discovered people can be added as contacts
- `outreach-manager` → campaigns pull from contact lists
- `analytics` → tracks engagement per contact
- `workflow-engine` → follow-up sequences reference contacts

## Agent

The `account-planner` agent (`.claude/agents/account-planner.md`) plans multi-step follow-up sequences based on deal stage and contact history.
