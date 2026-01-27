---
name: qa
description: QA review and compliance checks before sending outreach
---

# /qa Command

Review outreach messages for quality, compliance, and brand voice before sending.

## Usage

```
/qa [action]
```

### Actions

- `/qa review <message>` — Review a single message for compliance and quality
- `/qa campaign <campaign_id>` — Review all messages in a campaign before send
- `/qa audit` — Full compliance audit of recent outreach
- `/qa brand-voice <text>` — Check text against brand voice guidelines
- `/qa spam-score <message>` — Check spam score of an email
- `/qa blocklist` — View/manage prohibited words and phrases
- `/qa report` — Generate QA compliance report

## Compliance Checks

### CAN-SPAM (US)
- Physical mailing address present
- Unsubscribe link/mechanism included
- "From" name matches sender identity
- Subject line not deceptive
- Message identified as advertisement (if applicable)

### GDPR (EU)
- Lawful basis for contact (legitimate interest / consent)
- Data processing disclosure
- Right to erasure mentioned
- No excessive personal data collection

### Platform-Specific
- LinkedIn: No connection request spam, personalized messages
- Twitter: No aggressive DM patterns, follows TOS
- Instagram: No bulk DM violations, authentic engagement

## Quality Scoring

| Score | Rating | Action |
|-------|--------|--------|
| 90-100 | Excellent | Safe to send |
| 70-89 | Good | Minor improvements suggested |
| 50-69 | Fair | Review recommended before send |
| 0-49 | Poor | Do not send, rewrite required |

Scoring factors:
- Personalization (uses name, company, context)
- Value proposition clarity
- Call-to-action effectiveness
- Grammar and spelling
- Tone appropriateness
- Spam trigger words absent
- Compliance requirements met

## Brand Voice

Configure brand voice in `output/brand_voice.json`:
```json
{
  "tone": "professional but friendly",
  "avoid": ["synergy", "circle back", "touch base"],
  "prefer": ["collaborate", "follow up", "connect"],
  "max_exclamation_marks": 1,
  "emoji_allowed": false
}
```

## Implementation

```bash
python .claude/scripts/qa_checker.py review "Your message text here"
python .claude/scripts/qa_checker.py spam-score "Subject: Special offer!" "Body text..."
python .claude/scripts/qa_checker.py compliance --type canspam --message "text"
python .claude/scripts/qa_checker.py brand-voice "Check this text"
python .claude/scripts/qa_checker.py audit --days 7
python .claude/scripts/qa_checker.py report
```

## Integration

- Called automatically by `/outreach` before campaign send (if enabled)
- `/compose` can run QA check before sending single emails
- `/workflow` steps can include QA gate before execution

## Skill Reference

This command uses the `qa-compliance` skill at `.claude/skills/qa-compliance/SKILL.md`.
Agent: `compliance-checker` at `.claude/agents/compliance-checker.md`.
