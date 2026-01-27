---
name: ops
description: Support and operations management for outreach system
---

# /ops Command

Manage the outreach system operations — health checks, logs, cleanup, backups, and troubleshooting.

## Usage

```
/ops [action]
```

### Actions

- `/ops status` — System health check (all services)
- `/ops logs` — View recent activity logs
- `/ops cleanup` — Clean up old logs, expired exports, temp files
- `/ops backup` — Backup all data (people, workflows, templates, credentials)
- `/ops restore <file>` — Restore from a backup
- `/ops reset` — Reset rate limiters and session state
- `/ops setup` — Re-run initial setup

## System Health Check

```
/ops status
```

Checks:
| Service | What it checks |
|---------|---------------|
| Python | Python 3.x installed and accessible |
| Node.js | Node.js 18+ installed |
| Canvas | tldraw-canvas/ dependencies installed |
| Gmail OAuth | credentials.json and token.json present |
| Exa API | EXA_API_KEY set in environment |
| Browser Extension | extension directory exists |
| Output dirs | output/workflows, logs, discovery, reports exist |
| Rate limiter | rate_limits.json present and valid |
| Team config | team.json present |

## Logs

```
/ops logs                    # Last 20 log entries
/ops logs --tail 50          # Last 50 entries
/ops logs --campaign "B2B"   # Filter by campaign
/ops logs --platform linkedin # Filter by platform
/ops logs --level error      # Only errors
```

## Cleanup

```
/ops cleanup
```

Removes:
- Logs older than 30 days
- Expired export files
- Empty discovery sessions
- Orphaned workflow queue items

## Backup & Restore

```
/ops backup                              # Creates timestamped backup zip
/ops restore output/backups/backup-2026-01-28.zip
```

Backup includes:
- `output/discovery/people.json` — Discovered contacts
- `output/workflows/` — Saved workflows
- `.claude/templates/` — Custom templates
- `team.json` — Team credentials (encrypted)
- Rate limiter state

## Reset

```
/ops reset                # Reset all rate limiters
/ops reset --platform linkedin  # Reset LinkedIn limits only
```

## Re-run Setup

```
/ops setup
```

Runs `python .claude/scripts/auto_setup.py` to re-check and fix the environment.

## Implementation

```bash
# Health check
python .claude/scripts/ops_manager.py status

# Logs
python .claude/scripts/ops_manager.py logs --tail 20

# Cleanup
python .claude/scripts/ops_manager.py cleanup --days 30

# Backup
python .claude/scripts/ops_manager.py backup --output output/backups/

# Reset rate limits
python .claude/scripts/ops_manager.py reset
```
