#!/usr/bin/env python3
"""
Email Verification Script
Validates email addresses before outreach campaigns.

Checks:
  1. Syntax validation (RFC 5322)
  2. Domain MX record lookup
  3. Disposable email provider detection
  4. Role-based address detection (info@, admin@, etc.)
  5. SPF/DKIM/DMARC record checks for sender verification

Usage:
  python email_verifier.py verify user@example.com
  python email_verifier.py bulk contacts.csv --column email
  python email_verifier.py domain example.com
  python email_verifier.py sender --email your@domain.com
"""

import argparse
import csv
import dns.resolver
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Common disposable email domains
DISPOSABLE_DOMAINS = {
    "mailinator.com", "guerrillamail.com", "tempmail.com", "throwaway.email",
    "yopmail.com", "sharklasers.com", "guerrillamailblock.com", "grr.la",
    "dispostable.com", "maildrop.cc", "10minutemail.com", "trashmail.com",
    "temp-mail.org", "fakeinbox.com", "getnada.com", "mohmal.com",
    "burnermail.io", "tempail.com", "emailondeck.com", "mintemail.com",
}

ROLE_PREFIXES = {
    "info", "admin", "support", "sales", "contact", "help", "office",
    "billing", "accounts", "hr", "marketing", "press", "media",
    "webmaster", "postmaster", "abuse", "noreply", "no-reply",
}


def validate_syntax(email: str) -> bool:
    """Check if email matches RFC 5322 basic pattern."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def check_mx(domain: str) -> Dict:
    """Look up MX records for domain."""
    try:
        answers = dns.resolver.resolve(domain, 'MX')
        records = sorted(
            [{"priority": r.preference, "host": str(r.exchange).rstrip('.')} for r in answers],
            key=lambda x: x["priority"]
        )
        return {"valid": True, "records": records}
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        return {"valid": False, "records": [], "error": "No MX records found"}
    except dns.resolver.NoNameservers:
        return {"valid": False, "records": [], "error": "Domain DNS not responding"}
    except Exception as e:
        return {"valid": False, "records": [], "error": str(e)}


def check_spf(domain: str) -> Dict:
    """Check SPF record for domain."""
    try:
        answers = dns.resolver.resolve(domain, 'TXT')
        for rdata in answers:
            txt = str(rdata).strip('"')
            if txt.startswith('v=spf1'):
                return {"valid": True, "record": txt}
        return {"valid": False, "error": "No SPF record found"}
    except Exception as e:
        return {"valid": False, "error": str(e)}


def check_dkim(domain: str, selector: str = "default") -> Dict:
    """Check DKIM record for domain."""
    dkim_domain = f"{selector}._domainkey.{domain}"
    try:
        answers = dns.resolver.resolve(dkim_domain, 'TXT')
        for rdata in answers:
            txt = str(rdata).strip('"')
            if 'v=DKIM1' in txt or 'p=' in txt:
                return {"valid": True, "selector": selector, "record": txt[:100] + "..."}
        return {"valid": False, "error": f"No DKIM record at {dkim_domain}"}
    except Exception as e:
        return {"valid": False, "error": str(e)}


def check_dmarc(domain: str) -> Dict:
    """Check DMARC record for domain."""
    dmarc_domain = f"_dmarc.{domain}"
    try:
        answers = dns.resolver.resolve(dmarc_domain, 'TXT')
        for rdata in answers:
            txt = str(rdata).strip('"')
            if txt.startswith('v=DMARC1'):
                return {"valid": True, "record": txt}
        return {"valid": False, "error": "No DMARC record found"}
    except Exception as e:
        return {"valid": False, "error": str(e)}


def is_disposable(domain: str) -> bool:
    """Check if domain is a disposable email provider."""
    return domain.lower() in DISPOSABLE_DOMAINS


def is_role_based(local_part: str) -> bool:
    """Check if the local part is a role-based prefix."""
    return local_part.lower().split('+')[0] in ROLE_PREFIXES


def verify_email(email: str) -> Dict:
    """Full verification of a single email address."""
    email = email.strip().lower()
    result = {
        "email": email,
        "status": "invalid",
        "checks": {},
    }

    # Syntax
    if not validate_syntax(email):
        result["checks"]["syntax"] = False
        result["reason"] = "Invalid email syntax"
        return result
    result["checks"]["syntax"] = True

    local, domain = email.rsplit('@', 1)

    # Disposable
    if is_disposable(domain):
        result["checks"]["disposable"] = True
        result["status"] = "disposable"
        result["reason"] = "Disposable email provider"
        return result
    result["checks"]["disposable"] = False

    # Role-based
    result["checks"]["role_based"] = is_role_based(local)
    if result["checks"]["role_based"]:
        result["status"] = "role"
        result["reason"] = "Role-based address (lower reply rates)"

    # MX records
    mx = check_mx(domain)
    result["checks"]["mx"] = mx["valid"]
    if not mx["valid"]:
        result["status"] = "invalid"
        result["reason"] = mx.get("error", "No MX records")
        return result

    result["mx_records"] = mx["records"]

    # If we got here and status is still invalid, it's valid
    if result["status"] == "invalid":
        result["status"] = "valid"
        result["reason"] = "All checks passed"

    return result


def verify_bulk(filepath: str, email_column: str = "email") -> List[Dict]:
    """Verify a list of emails from a CSV file."""
    results = []
    path = Path(filepath)

    if not path.exists():
        print(f"ERROR: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        if email_column not in reader.fieldnames:
            print(f"ERROR: Column '{email_column}' not found. Available: {reader.fieldnames}", file=sys.stderr)
            sys.exit(1)

        for row in reader:
            email = row.get(email_column, '').strip()
            if email:
                result = verify_email(email)
                results.append(result)

    return results


def verify_domain(domain: str) -> Dict:
    """Full domain verification."""
    return {
        "domain": domain,
        "mx": check_mx(domain),
        "spf": check_spf(domain),
        "dkim": check_dkim(domain),
        "dmarc": check_dmarc(domain),
    }


def verify_sender(email: str) -> Dict:
    """Verify sender email configuration."""
    _, domain = email.rsplit('@', 1)
    domain_checks = verify_domain(domain)

    score = 0
    if domain_checks["mx"]["valid"]:
        score += 25
    if domain_checks["spf"]["valid"]:
        score += 25
    if domain_checks["dkim"]["valid"]:
        score += 25
    if domain_checks["dmarc"]["valid"]:
        score += 25

    return {
        "sender": email,
        "domain": domain,
        "deliverability_score": score,
        "rating": "excellent" if score >= 75 else "good" if score >= 50 else "poor",
        **domain_checks,
    }


def main():
    parser = argparse.ArgumentParser(description="Email Verification")
    subparsers = parser.add_subparsers(dest="command")

    sp = subparsers.add_parser("verify", help="Verify a single email")
    sp.add_argument("email")

    sp = subparsers.add_parser("bulk", help="Verify emails from CSV")
    sp.add_argument("file", help="Path to CSV file")
    sp.add_argument("--column", default="email", help="Email column name")
    sp.add_argument("--output", help="Output file path (JSON)")

    sp = subparsers.add_parser("domain", help="Check domain records")
    sp.add_argument("domain")

    sp = subparsers.add_parser("sender", help="Verify sender email setup")
    sp.add_argument("--email", required=True)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "verify":
        result = verify_email(args.email)
        print(json.dumps(result, indent=2))

    elif args.command == "bulk":
        results = verify_bulk(args.file, args.column)
        summary = {
            "total": len(results),
            "valid": sum(1 for r in results if r["status"] == "valid"),
            "invalid": sum(1 for r in results if r["status"] == "invalid"),
            "risky": sum(1 for r in results if r["status"] == "role"),
            "disposable": sum(1 for r in results if r["status"] == "disposable"),
        }
        output = {"summary": summary, "results": results}

        if args.output:
            Path(args.output).write_text(json.dumps(output, indent=2))
            print(f"Results saved to {args.output}")
        else:
            print(json.dumps(output, indent=2))

    elif args.command == "domain":
        result = verify_domain(args.domain)
        print(json.dumps(result, indent=2))

    elif args.command == "sender":
        result = verify_sender(args.email)
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
