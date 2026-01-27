---
name: access-manager
description: |
  User access control, roles, permissions, and multi-tenant management. Use this skill when
  the user wants to manage users, roles, permissions, tenants, or credentials.
allowed-tools:
  - Bash
  - Read
  - Write
  - AskUserQuestion
---

# Access Manager Skill

Manages users, roles, permissions, multi-tenant configs, and credential vault.

## When to Use

- User wants to create or manage user accounts
- User needs to assign or change roles
- User wants to set up multi-tenant isolation
- User needs to manage credentials securely

## Core Operations

### Users & Roles
```bash
python .claude/scripts/rbac.py users
python .claude/scripts/rbac.py create john --role agent
python .claude/scripts/rbac.py role john --role admin
python .claude/scripts/rbac.py grant john --permission platform.linkedin
```

### Multi-Tenant
```bash
python .claude/scripts/multi_tenant.py list
python .claude/scripts/multi_tenant.py create "Acme Corp"
python .claude/scripts/multi_tenant.py config TENANT_ID --feature email_campaigns true
```

### Credentials
```bash
python .claude/scripts/secure_credentials.py list
python .claude/scripts/secure_credentials.py set EXA_API_KEY "key-value"
python .claude/scripts/secure_credentials.py get EXA_API_KEY
```

### Audit
```bash
python .claude/scripts/audit_logger.py query --type auth --days 7
```
