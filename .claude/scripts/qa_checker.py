#!/usr/bin/env python3
"""
QA Checker — Compliance, quality scoring, brand voice, and spam detection.

Usage:
  python qa_checker.py review "message text"
  python qa_checker.py spam-score "subject" "body"
  python qa_checker.py compliance --type canspam --message "text"
  python qa_checker.py brand-voice "text to check"
  python qa_checker.py audit --days 7
  python qa_checker.py report
  python qa_checker.py blocklist [--add "word"] [--remove "word"]

Data: output/qa/
"""

import argparse
import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List

DATA_DIR = Path("output/qa")
REVIEWS_FILE = DATA_DIR / "reviews.json"
BLOCKLIST_FILE = DATA_DIR / "blocklist.json"
BRAND_VOICE_FILE = Path("output/brand_voice.json")

# Spam trigger words (common email spam indicators)
SPAM_TRIGGERS = [
    "act now", "buy now", "click here", "congratulations", "dear friend",
    "double your", "earn money", "free", "guaranteed", "incredible deal",
    "limited time", "make money", "no obligation", "offer expires",
    "order now", "risk free", "special promotion", "urgent", "winner",
    "100% free", "cash bonus", "credit card", "discount", "lowest price",
    "million dollars", "no cost", "prize", "save big", "while supplies last",
]

# CAN-SPAM required elements
CANSPAM_CHECKS = [
    ("unsubscribe", "Must include unsubscribe mechanism"),
    ("address", "Must include physical mailing address"),
]

DEFAULT_BRAND_VOICE = {
    "tone": "professional but friendly",
    "avoid": ["synergy", "circle back", "touch base", "leverage", "paradigm", "disrupt"],
    "prefer": ["collaborate", "follow up", "connect", "help", "share"],
    "max_exclamation_marks": 1,
    "emoji_allowed": False,
    "max_caps_words": 2,
}


def _ensure_dirs():
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def _load_brand_voice() -> Dict:
    if BRAND_VOICE_FILE.exists():
        return json.loads(BRAND_VOICE_FILE.read_text())
    return DEFAULT_BRAND_VOICE


def _load_blocklist() -> List[str]:
    if BLOCKLIST_FILE.exists():
        return json.loads(BLOCKLIST_FILE.read_text())
    return []


def _save_review(review: Dict):
    _ensure_dirs()
    reviews = []
    if REVIEWS_FILE.exists():
        reviews = json.loads(REVIEWS_FILE.read_text())
    reviews.append(review)
    REVIEWS_FILE.write_text(json.dumps(reviews, indent=2))


# ─── Quality Scoring ─────────────────────────────────────────────────────────

def review_message(message: str) -> Dict:
    """Full quality review of a message."""
    score = 100
    issues = []
    warnings = []

    text_lower = message.lower()
    blocklist = _load_blocklist()

    # Spam trigger check (-5 per trigger, max -30)
    spam_found = [w for w in SPAM_TRIGGERS if w in text_lower]
    penalty = min(len(spam_found) * 5, 30)
    score -= penalty
    if spam_found:
        issues.append(f"Spam triggers found: {', '.join(spam_found[:5])}")

    # Blocklist check (-10 per word)
    blocked_found = [w for w in blocklist if w.lower() in text_lower]
    score -= len(blocked_found) * 10
    if blocked_found:
        issues.append(f"Blocked words found: {', '.join(blocked_found)}")

    # Length check
    word_count = len(message.split())
    if word_count < 20:
        warnings.append("Message is very short (under 20 words)")
        score -= 5
    if word_count > 500:
        warnings.append("Message is very long (over 500 words)")
        score -= 5

    # ALL CAPS check
    caps_words = [w for w in message.split() if w.isupper() and len(w) > 2]
    if len(caps_words) > 3:
        score -= 10
        issues.append(f"Excessive ALL CAPS words: {len(caps_words)}")

    # Exclamation marks
    excl_count = message.count('!')
    if excl_count > 3:
        score -= 5
        warnings.append(f"Too many exclamation marks: {excl_count}")

    # Personalization indicators
    has_personalization = any(marker in message for marker in ["{{", "{%", "Hi ", "Dear "])
    if not has_personalization:
        score -= 10
        warnings.append("No personalization detected (no name/variable references)")

    # CTA check
    cta_words = ["reply", "click", "visit", "schedule", "book", "call", "sign up", "try", "start"]
    has_cta = any(w in text_lower for w in cta_words)
    if not has_cta:
        score -= 5
        warnings.append("No clear call-to-action detected")

    score = max(0, min(100, score))

    rating = "excellent" if score >= 90 else "good" if score >= 70 else "fair" if score >= 50 else "poor"

    review = {
        "score": score,
        "rating": rating,
        "issues": issues,
        "warnings": warnings,
        "spam_triggers": spam_found,
        "word_count": word_count,
        "has_personalization": has_personalization,
        "has_cta": has_cta,
        "reviewed_at": datetime.now().isoformat(),
    }

    _save_review(review)
    return review


# ─── Spam Score ──────────────────────────────────────────────────────────────

def spam_score(subject: str, body: str) -> Dict:
    """Calculate spam score for an email."""
    score = 0  # 0 = clean, 100 = definitely spam
    flags = []

    combined = f"{subject} {body}".lower()

    # Subject checks
    if subject.isupper():
        score += 20
        flags.append("Subject is ALL CAPS")
    if subject.count('!') > 1:
        score += 10
        flags.append("Multiple exclamation marks in subject")
    if re.search(r'RE:|FW:', subject) and "reply" not in combined:
        score += 15
        flags.append("Fake RE:/FW: prefix")

    # Trigger words
    triggers = [w for w in SPAM_TRIGGERS if w in combined]
    score += min(len(triggers) * 5, 40)
    if triggers:
        flags.append(f"Spam words: {', '.join(triggers[:5])}")

    # ALL CAPS in body
    caps_ratio = sum(1 for c in body if c.isupper()) / max(len(body), 1)
    if caps_ratio > 0.3:
        score += 15
        flags.append("High CAPS ratio in body")

    # URL density
    urls = re.findall(r'https?://\S+', body)
    if len(urls) > 3:
        score += 10
        flags.append(f"Too many URLs: {len(urls)}")

    score = min(100, score)
    rating = "clean" if score < 20 else "low risk" if score < 40 else "medium risk" if score < 60 else "high risk" if score < 80 else "spam"

    return {"score": score, "rating": rating, "flags": flags}


# ─── Compliance ──────────────────────────────────────────────────────────────

def check_compliance(message: str, compliance_type: str = "canspam") -> Dict:
    """Check message for legal compliance."""
    text_lower = message.lower()
    passed = []
    failed = []

    if compliance_type == "canspam":
        # Unsubscribe
        if any(w in text_lower for w in ["unsubscribe", "opt out", "opt-out", "remove me"]):
            passed.append("Unsubscribe mechanism present")
        else:
            failed.append("Missing unsubscribe mechanism (CAN-SPAM required)")

        # Physical address
        address_pattern = r'\d+\s+\w+\s+(street|st|avenue|ave|road|rd|boulevard|blvd|drive|dr|lane|ln|way|suite|ste)'
        if re.search(address_pattern, text_lower):
            passed.append("Physical address present")
        else:
            failed.append("Missing physical mailing address (CAN-SPAM required)")

        # Honest subject (can't fully verify, flag if empty)
        if len(message.strip()) < 10:
            failed.append("Message too short to contain required elements")

    elif compliance_type == "gdpr":
        if any(w in text_lower for w in ["data", "privacy", "consent", "legitimate interest"]):
            passed.append("Data processing reference found")
        else:
            failed.append("No data processing disclosure (GDPR recommended)")

        if any(w in text_lower for w in ["unsubscribe", "opt out", "remove", "delete my data"]):
            passed.append("Right to erasure/opt-out mentioned")
        else:
            failed.append("No right to erasure mention (GDPR recommended)")

    compliant = len(failed) == 0

    return {
        "compliant": compliant,
        "type": compliance_type,
        "passed": passed,
        "failed": failed,
        "checked_at": datetime.now().isoformat(),
    }


# ─── Brand Voice ─────────────────────────────────────────────────────────────

def check_brand_voice(text: str) -> Dict:
    """Check text against brand voice guidelines."""
    voice = _load_brand_voice()
    text_lower = text.lower()
    issues = []

    # Avoided words
    avoided_found = [w for w in voice.get("avoid", []) if w.lower() in text_lower]
    if avoided_found:
        issues.append(f"Avoided words used: {', '.join(avoided_found)}")

    # Exclamation marks
    max_excl = voice.get("max_exclamation_marks", 1)
    if text.count('!') > max_excl:
        issues.append(f"Too many exclamation marks ({text.count('!')} > {max_excl})")

    # Emoji check
    if not voice.get("emoji_allowed", False):
        emoji_pattern = re.compile(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]')
        if emoji_pattern.search(text):
            issues.append("Emojis used but not allowed by brand voice")

    # ALL CAPS
    max_caps = voice.get("max_caps_words", 2)
    caps_words = [w for w in text.split() if w.isupper() and len(w) > 2]
    if len(caps_words) > max_caps:
        issues.append(f"Too many ALL CAPS words ({len(caps_words)} > {max_caps})")

    consistent = len(issues) == 0

    return {
        "consistent": consistent,
        "tone": voice.get("tone", ""),
        "issues": issues,
        "suggestions": voice.get("prefer", []),
    }


# ─── Blocklist ───────────────────────────────────────────────────────────────

def manage_blocklist(add: str = None, remove: str = None) -> List[str]:
    blocklist = _load_blocklist()
    if add:
        if add not in blocklist:
            blocklist.append(add)
    if remove:
        blocklist = [w for w in blocklist if w != remove]
    _ensure_dirs()
    BLOCKLIST_FILE.write_text(json.dumps(blocklist, indent=2))
    return blocklist


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="QA Checker — Compliance & Quality")
    subparsers = parser.add_subparsers(dest="command")

    sp = subparsers.add_parser("review", help="Review message quality")
    sp.add_argument("message")

    sp = subparsers.add_parser("spam-score", help="Check spam score")
    sp.add_argument("subject")
    sp.add_argument("body")

    sp = subparsers.add_parser("compliance", help="Check legal compliance")
    sp.add_argument("--type", default="canspam", choices=["canspam", "gdpr"])
    sp.add_argument("--message", required=True)

    sp = subparsers.add_parser("brand-voice", help="Check brand voice")
    sp.add_argument("text")

    sp = subparsers.add_parser("blocklist", help="Manage blocked words")
    sp.add_argument("--add")
    sp.add_argument("--remove")

    sp = subparsers.add_parser("audit", help="Audit recent reviews")
    sp.add_argument("--days", type=int, default=7)

    subparsers.add_parser("report", help="QA summary report")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "review":
        print(json.dumps(review_message(args.message), indent=2))
    elif args.command == "spam-score":
        print(json.dumps(spam_score(args.subject, args.body), indent=2))
    elif args.command == "compliance":
        print(json.dumps(check_compliance(args.message, args.type), indent=2))
    elif args.command == "brand-voice":
        print(json.dumps(check_brand_voice(args.text), indent=2))
    elif args.command == "blocklist":
        result = manage_blocklist(args.add, args.remove)
        print(json.dumps(result, indent=2))
    elif args.command == "audit":
        if REVIEWS_FILE.exists():
            reviews = json.loads(REVIEWS_FILE.read_text())
            cutoff = (datetime.now() - timedelta(days=args.days)).isoformat()
            recent = [r for r in reviews if r.get("reviewed_at", "") >= cutoff]
            print(json.dumps({"period_days": args.days, "reviews": len(recent), "results": recent}, indent=2))
        else:
            print(json.dumps({"reviews": 0, "results": []}, indent=2))
    elif args.command == "report":
        if REVIEWS_FILE.exists():
            reviews = json.loads(REVIEWS_FILE.read_text())
            scores = [r["score"] for r in reviews if "score" in r]
            print(json.dumps({
                "total_reviews": len(reviews),
                "avg_score": round(sum(scores) / len(scores)) if scores else 0,
                "excellent": sum(1 for s in scores if s >= 90),
                "good": sum(1 for s in scores if 70 <= s < 90),
                "fair": sum(1 for s in scores if 50 <= s < 70),
                "poor": sum(1 for s in scores if s < 50),
            }, indent=2))
        else:
            print(json.dumps({"total_reviews": 0}, indent=2))


if __name__ == "__main__":
    main()
