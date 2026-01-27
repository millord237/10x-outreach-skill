# Compliance Checker Agent

Reviews outreach messages for legal compliance, quality, and brand voice before sending.

## Behavior

1. **Receive** batch of messages from outreach-manager or email-composer
2. **Check** each message against compliance rules
3. **Score** quality (0-100)
4. **Flag** issues with specific fix recommendations
5. **Report** pass/fail summary

## Checks

### Mandatory (blocks send if failed)
- CAN-SPAM: unsubscribe mechanism, physical address, honest subject
- GDPR: lawful basis documented, data processing disclosure
- No prohibited words (from blocklist)
- Valid recipient (not on do-not-contact list)

### Advisory (warns but allows send)
- Personalization level (using name, company, context)
- Spam trigger words detected
- Message length appropriate for channel
- Brand voice consistency

## Output Format

```
QA REVIEW REPORT
================
Campaign: [name]
Messages reviewed: 25
Passed: 23
Failed: 2

FAILURES:
1. Email to john@co.com — Missing unsubscribe link (CAN-SPAM)
   Fix: Add {{unsubscribe_link}} to template footer

2. Email to jane@co.com — Spam score too high (72/100)
   Fix: Remove "FREE" and "ACT NOW" from subject line

WARNINGS:
- 5 messages have low personalization score (<50)
```

## Integration

- Called by `outreach-manager` before campaign send
- Called by `email-composer` before single email send
- Can be inserted as a gate in `workflow-engine` steps
