---
name: analytics
description: View campaign and outreach analytics
---

# /analytics Command

View performance metrics, campaign statistics, and outreach effectiveness.

## Usage

```
/analytics [action]
```

### Actions

- `/analytics` — Show dashboard summary (all campaigns)
- `/analytics campaign <name>` — Metrics for a specific campaign
- `/analytics daily` — Today's activity summary
- `/analytics weekly` — This week's performance report
- `/analytics export` — Export analytics to CSV/JSON

## Metrics Tracked

### Email
- Sent, delivered, bounced, opened, clicked, replied
- Open rate, click rate, reply rate

### Platform Engagement
- LinkedIn: connections sent/accepted, messages, profile views, likes, comments
- Twitter: follows, DMs, likes, replies, retweets
- Instagram: follows, DMs, likes, comments, story replies

### Workflow
- Workflows started, completed, failed
- Average duration, step completion rates

## Data Sources

Analytics are collected from:
- `output/logs/campaigns/` — Campaign execution logs
- `output/logs/` — General activity logs
- `output/reports/` — Generated reports

## Examples

```
/analytics
/analytics campaign "B2B January"
/analytics weekly
/analytics export --format csv --output output/reports/weekly.csv
```

## Skill Reference

This command uses the `analytics` skill at `.claude/skills/analytics/SKILL.md`.
