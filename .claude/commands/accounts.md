---
name: accounts
description: CRM-style contact and deal pipeline management
---

# /accounts Command

Manage contacts, deals, and follow-up sequences like a CRM.

## Usage

```
/accounts [action]
```

### Actions

- `/accounts` — Dashboard overview (pipeline summary, upcoming follow-ups)
- `/accounts add <name> --email <email> --company <company>` — Add a contact
- `/accounts list` — List all contacts
- `/accounts search <query>` — Search contacts by name, company, or tag
- `/accounts view <id>` — View contact details + interaction history
- `/accounts deal <id> --stage <stage>` — Update deal stage
- `/accounts followup <id> --date <date> --note <note>` — Schedule follow-up
- `/accounts import <file>` — Import contacts from CSV/JSON
- `/accounts export` — Export contacts to CSV
- `/accounts pipeline` — View deal pipeline by stage
- `/accounts overdue` — Show overdue follow-ups

## Deal Pipeline Stages

```
lead → qualified → proposal → negotiation → closed_won | closed_lost
```

## Contact Fields

| Field | Description |
|-------|-------------|
| name | Full name |
| email | Email address |
| company | Company name |
| role | Job title |
| phone | Phone number |
| linkedin | LinkedIn profile URL |
| twitter | Twitter handle |
| tags | Custom tags (comma-separated) |
| source | How discovered (exa, linkedin, manual, import) |
| deal_stage | Current pipeline stage |
| deal_value | Estimated deal value |
| notes | Free-text notes |

## Integration

- `/discover` results can be added directly to accounts
- `/outreach` campaigns pull recipients from account lists
- `/analytics` tracks engagement per contact
- `/workflow` sequences reference account contacts

## Implementation

```bash
python .claude/scripts/account_manager.py dashboard
python .claude/scripts/account_manager.py add "John Doe" --email john@company.com --company "Acme Inc" --role "CTO"
python .claude/scripts/account_manager.py list --stage qualified --tag ai-startup
python .claude/scripts/account_manager.py deal CONTACT_ID --stage proposal --value 50000
python .claude/scripts/account_manager.py followup CONTACT_ID --date 2026-02-05 --note "Send proposal"
python .claude/scripts/account_manager.py pipeline
python .claude/scripts/account_manager.py overdue
python .claude/scripts/account_manager.py export --format csv --output output/contacts.csv
```

## Skill Reference

This command uses the `account-manager` skill at `.claude/skills/account-manager/SKILL.md`.
