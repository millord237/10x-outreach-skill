---
name: qa-compliance
description: |
  QA review and compliance checks for outreach messages. Use this skill when the user
  wants to review messages before sending, check compliance, or enforce brand voice.
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
  - AskUserQuestion
---

# QA / Compliance Skill

Reviews outreach messages for quality, legal compliance, and brand consistency.

## When to Use

- Before sending campaigns (pre-send review gate)
- User asks to check a message for compliance
- User wants brand voice enforcement
- User needs spam score check
- Compliance audit of recent outreach

## Checks Performed

### Legal Compliance
- **CAN-SPAM**: Unsubscribe link, physical address, honest subject, sender identity
- **GDPR**: Lawful basis, data processing disclosure, right to erasure
- **Platform TOS**: Platform-specific rules for LinkedIn, Twitter, Instagram

### Quality Scoring (0-100)
- Personalization level
- Value proposition clarity
- CTA effectiveness
- Grammar and spelling
- Spam trigger words
- Tone appropriateness

### Brand Voice
- Tone consistency
- Prohibited words/phrases
- Preferred terminology
- Emoji policy
- Formatting standards

## Core Operations

```bash
python .claude/scripts/qa_checker.py review "message text"
python .claude/scripts/qa_checker.py spam-score "subject" "body"
python .claude/scripts/qa_checker.py compliance --type canspam --message "text"
python .claude/scripts/qa_checker.py brand-voice "text to check"
python .claude/scripts/qa_checker.py audit --days 7
```

## Agent

The `compliance-checker` agent (`.claude/agents/compliance-checker.md`) reviews batches of messages before campaign execution and flags issues.
