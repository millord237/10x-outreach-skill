---
name: access
description: User access control, roles, and multi-tenant management
---

# /access Command

Manage user accounts, roles, permissions, and multi-tenant configurations.

## Usage

```
/access [action]
```

### Actions

- `/access` — Show current user and permissions
- `/access users` — List all users
- `/access create <username> --role <role>` — Create a user
- `/access role <username> --role <role>` — Change user role
- `/access grant <username> --permission <perm>` — Grant custom permission
- `/access revoke <username> --permission <perm>` — Revoke permission
- `/access tenants` — List tenants (multi-tenant mode)
- `/access tenant create <name>` — Create a tenant
- `/access credentials` — Manage credential vault
- `/access audit` — View access audit log

## Roles

| Role | Permissions |
|------|------------|
| admin | All permissions (user management, config, execution, viewing) |
| agent | Create/execute workflows, use platforms, view analytics, manage contacts |
| viewer | Read-only access to dashboards, reports, contacts |

## Custom Permissions

| Permission | Description |
|------------|-------------|
| `workflow.create` | Create new workflows |
| `workflow.execute` | Execute workflows |
| `platform.linkedin` | Use LinkedIn adapter |
| `platform.twitter` | Use Twitter adapter |
| `platform.instagram` | Use Instagram adapter |
| `email.send` | Send emails |
| `contacts.manage` | Add/edit/delete contacts |
| `analytics.view` | View analytics |
| `admin.users` | Manage other users |
| `admin.config` | Change system configuration |

## Multi-Tenant

Each tenant gets:
- Isolated data directories
- Separate rate limits
- Custom feature flags
- Resource quotas (max users, workflows, targets)

## Credential Vault

Securely store and manage API keys, OAuth tokens, and platform credentials:
```
/access credentials list
/access credentials set EXA_API_KEY "your-key"
/access credentials rotate LINKEDIN_ACCESS_TOKEN
```

Uses AES-256 encryption with PBKDF2 key derivation.

## Implementation

```bash
python .claude/scripts/rbac.py users
python .claude/scripts/rbac.py create john --role agent
python .claude/scripts/rbac.py role john --role admin
python .claude/scripts/rbac.py grant john --permission platform.linkedin
python .claude/scripts/multi_tenant.py list
python .claude/scripts/multi_tenant.py create "Acme Corp"
python .claude/scripts/secure_credentials.py list
python .claude/scripts/audit_logger.py query --type auth --days 7
```

## Skill Reference

This command uses the `access-manager` skill at `.claude/skills/access-manager/SKILL.md`.
