---
name: verify
description: Email verification and deliverability checks
---

# /verify Command

Verify email addresses, check deliverability, and validate contact lists before campaigns.

## Usage

```
/verify [action]
```

### Actions

- `/verify <email>` — Verify a single email address
- `/verify list <file>` — Verify a list of emails from CSV/JSON
- `/verify domain <domain>` — Check domain MX records and deliverability
- `/verify sender` — Verify your own sender email setup (SPF, DKIM, DMARC)
- `/verify report` — Show verification statistics

## Single Email Verification

Checks performed:
1. **Syntax** — Valid email format
2. **Domain** — MX records exist
3. **Disposable** — Not a throwaway email provider
4. **Role-based** — Detects info@, admin@, support@ (lower reply rates)
5. **DNS** — Domain resolves and accepts mail

## Bulk Verification

```
/verify list output/discovery/targets.csv --email-column email
```

Output: Creates a verified file with status per email:
- `valid` — Safe to send
- `invalid` — Bad syntax or non-existent domain
- `risky` — Catch-all domain, may bounce
- `disposable` — Temporary email, skip
- `role` — Role-based address (info@, etc.)

## Sender Verification

```
/verify sender
```

Checks your sending domain for:
- **SPF record** — Authorized senders
- **DKIM** — Email signature
- **DMARC** — Policy alignment
- **Blacklist** — Domain reputation

## Domain Check

```
/verify domain example.com
```

Returns: MX records, SPF, DKIM, DMARC status, and whether the domain is a catch-all.

## Implementation

Uses Python scripts for DNS lookups and SMTP validation:

```bash
python .claude/scripts/email_verifier.py verify user@example.com
python .claude/scripts/email_verifier.py bulk output/targets.csv --column email
python .claude/scripts/email_verifier.py domain example.com
python .claude/scripts/email_verifier.py sender --email your@domain.com
```

## Examples

```
/verify john@company.com
/verify list contacts.csv
/verify domain company.com
/verify sender
```
