#!/usr/bin/env python3
"""
Account Manager — CRM-style contact and deal pipeline management.

Features:
  - Contact database (add, search, view, list, import, export)
  - Deal pipeline (lead → qualified → proposal → negotiation → closed_won/closed_lost)
  - Follow-up scheduler with overdue tracking
  - Interaction history per contact
  - CSV/JSON import and export

Usage:
  python account_manager.py dashboard
  python account_manager.py add "John Doe" --email john@co.com --company "Acme" --role "CTO"
  python account_manager.py list [--stage <stage>] [--tag <tag>] [--source <source>]
  python account_manager.py search <query>
  python account_manager.py view <id>
  python account_manager.py deal <id> --stage <stage> [--value <amount>]
  python account_manager.py followup <id> --date YYYY-MM-DD --note "text"
  python account_manager.py overdue
  python account_manager.py pipeline
  python account_manager.py import <file> [--format csv|json]
  python account_manager.py export [--format csv|json] [--output <file>]
  python account_manager.py interaction <id> --type <type> --note "text"

Data stored in: output/accounts/
"""

import argparse
import csv
import json
import os
import sys
import uuid
from datetime import datetime, date
from pathlib import Path
from typing import Dict, List, Optional

DATA_DIR = Path("output/accounts")
CONTACTS_FILE = DATA_DIR / "contacts.json"
FOLLOWUPS_FILE = DATA_DIR / "followups.json"

DEAL_STAGES = ["lead", "qualified", "proposal", "negotiation", "closed_won", "closed_lost"]


def _ensure_dirs():
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def _load(filepath: Path) -> list:
    if filepath.exists():
        return json.loads(filepath.read_text())
    return []


def _save(filepath: Path, data: list):
    _ensure_dirs()
    filepath.write_text(json.dumps(data, indent=2, default=str))


def _gen_id() -> str:
    return str(uuid.uuid4())[:8]


# ─── Contacts ────────────────────────────────────────────────────────────────

def add_contact(name: str, **kwargs) -> Dict:
    contacts = _load(CONTACTS_FILE)
    contact = {
        "id": _gen_id(),
        "name": name,
        "email": kwargs.get("email", ""),
        "company": kwargs.get("company", ""),
        "role": kwargs.get("role", ""),
        "phone": kwargs.get("phone", ""),
        "linkedin": kwargs.get("linkedin", ""),
        "twitter": kwargs.get("twitter", ""),
        "tags": [t.strip() for t in kwargs.get("tags", "").split(",") if t.strip()],
        "source": kwargs.get("source", "manual"),
        "deal_stage": "lead",
        "deal_value": 0,
        "notes": kwargs.get("notes", ""),
        "interactions": [],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
    }
    contacts.append(contact)
    _save(CONTACTS_FILE, contacts)
    return contact


def list_contacts(stage: str = None, tag: str = None, source: str = None) -> List[Dict]:
    contacts = _load(CONTACTS_FILE)
    if stage:
        contacts = [c for c in contacts if c.get("deal_stage") == stage]
    if tag:
        contacts = [c for c in contacts if tag in c.get("tags", [])]
    if source:
        contacts = [c for c in contacts if c.get("source") == source]
    return contacts


def search_contacts(query: str) -> List[Dict]:
    contacts = _load(CONTACTS_FILE)
    q = query.lower()
    return [c for c in contacts if q in c.get("name", "").lower()
            or q in c.get("company", "").lower()
            or q in c.get("email", "").lower()
            or q in c.get("role", "").lower()
            or any(q in t for t in c.get("tags", []))]


def view_contact(contact_id: str) -> Optional[Dict]:
    contacts = _load(CONTACTS_FILE)
    for c in contacts:
        if c["id"] == contact_id:
            return c
    return None


def update_deal(contact_id: str, stage: str, value: int = None) -> Optional[Dict]:
    contacts = _load(CONTACTS_FILE)
    for c in contacts:
        if c["id"] == contact_id:
            if stage not in DEAL_STAGES:
                print(f"Invalid stage. Must be one of: {', '.join(DEAL_STAGES)}", file=sys.stderr)
                return None
            c["deal_stage"] = stage
            if value is not None:
                c["deal_value"] = value
            c["updated_at"] = datetime.now().isoformat()
            _save(CONTACTS_FILE, contacts)
            return c
    print(f"Contact {contact_id} not found", file=sys.stderr)
    return None


def add_interaction(contact_id: str, interaction_type: str, note: str) -> Optional[Dict]:
    contacts = _load(CONTACTS_FILE)
    for c in contacts:
        if c["id"] == contact_id:
            interaction = {
                "type": interaction_type,
                "note": note,
                "timestamp": datetime.now().isoformat(),
            }
            c.setdefault("interactions", []).append(interaction)
            c["updated_at"] = datetime.now().isoformat()
            _save(CONTACTS_FILE, contacts)
            return c
    return None


# ─── Follow-ups ──────────────────────────────────────────────────────────────

def schedule_followup(contact_id: str, follow_date: str, note: str) -> Dict:
    followups = _load(FOLLOWUPS_FILE)
    contact = view_contact(contact_id)
    followup = {
        "id": _gen_id(),
        "contact_id": contact_id,
        "contact_name": contact["name"] if contact else "Unknown",
        "date": follow_date,
        "note": note,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
    }
    followups.append(followup)
    _save(FOLLOWUPS_FILE, followups)
    return followup


def get_overdue() -> List[Dict]:
    followups = _load(FOLLOWUPS_FILE)
    today = date.today().isoformat()
    return [f for f in followups if f["status"] == "pending" and f["date"] <= today]


# ─── Pipeline ────────────────────────────────────────────────────────────────

def get_pipeline() -> Dict:
    contacts = _load(CONTACTS_FILE)
    pipeline = {stage: [] for stage in DEAL_STAGES}
    for c in contacts:
        stage = c.get("deal_stage", "lead")
        pipeline.setdefault(stage, []).append({
            "id": c["id"],
            "name": c["name"],
            "company": c.get("company", ""),
            "value": c.get("deal_value", 0),
        })
    summary = {stage: {"count": len(items), "total_value": sum(i.get("value", 0) for i in items), "contacts": items}
               for stage, items in pipeline.items()}
    return summary


def dashboard() -> Dict:
    contacts = _load(CONTACTS_FILE)
    followups = _load(FOLLOWUPS_FILE)
    today = date.today().isoformat()
    overdue = [f for f in followups if f["status"] == "pending" and f["date"] <= today]
    upcoming = [f for f in followups if f["status"] == "pending" and f["date"] > today][:5]

    return {
        "total_contacts": len(contacts),
        "pipeline": {stage: sum(1 for c in contacts if c.get("deal_stage") == stage) for stage in DEAL_STAGES},
        "overdue_followups": len(overdue),
        "upcoming_followups": [{"contact": f["contact_name"], "date": f["date"], "note": f["note"]} for f in upcoming],
        "recent_contacts": [{"id": c["id"], "name": c["name"], "company": c.get("company")} for c in contacts[-5:]],
    }


# ─── Import / Export ─────────────────────────────────────────────────────────

def import_contacts(filepath: str, fmt: str = "csv") -> Dict:
    path = Path(filepath)
    if not path.exists():
        print(f"File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    imported = 0
    if fmt == "csv":
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row.get("name", row.get("Name", ""))
                if name:
                    add_contact(name, **{k.lower(): v for k, v in row.items() if k.lower() != "name"})
                    imported += 1
    elif fmt == "json":
        data = json.loads(path.read_text())
        for item in (data if isinstance(data, list) else [data]):
            name = item.pop("name", "Unknown")
            add_contact(name, **item)
            imported += 1

    return {"imported": imported, "file": filepath}


def export_contacts(fmt: str = "csv", output: str = None) -> str:
    contacts = _load(CONTACTS_FILE)
    if not output:
        output = f"output/contacts_export.{fmt}"

    Path(output).parent.mkdir(parents=True, exist_ok=True)

    if fmt == "csv":
        if contacts:
            keys = ["id", "name", "email", "company", "role", "phone", "linkedin", "twitter",
                     "deal_stage", "deal_value", "source", "created_at"]
            with open(output, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=keys, extrasaction='ignore')
                writer.writeheader()
                writer.writerows(contacts)
    elif fmt == "json":
        Path(output).write_text(json.dumps(contacts, indent=2, default=str))

    return output


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Account Manager — CRM for outreach")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("dashboard", help="Pipeline overview")

    sp = subparsers.add_parser("add", help="Add a contact")
    sp.add_argument("name")
    sp.add_argument("--email", default="")
    sp.add_argument("--company", default="")
    sp.add_argument("--role", default="")
    sp.add_argument("--phone", default="")
    sp.add_argument("--linkedin", default="")
    sp.add_argument("--twitter", default="")
    sp.add_argument("--tags", default="")
    sp.add_argument("--source", default="manual")
    sp.add_argument("--notes", default="")

    sp = subparsers.add_parser("list", help="List contacts")
    sp.add_argument("--stage")
    sp.add_argument("--tag")
    sp.add_argument("--source")

    sp = subparsers.add_parser("search", help="Search contacts")
    sp.add_argument("query")

    sp = subparsers.add_parser("view", help="View contact")
    sp.add_argument("id")

    sp = subparsers.add_parser("deal", help="Update deal stage")
    sp.add_argument("id")
    sp.add_argument("--stage", required=True, choices=DEAL_STAGES)
    sp.add_argument("--value", type=int)

    sp = subparsers.add_parser("followup", help="Schedule follow-up")
    sp.add_argument("id")
    sp.add_argument("--date", required=True)
    sp.add_argument("--note", required=True)

    subparsers.add_parser("overdue", help="Show overdue follow-ups")
    subparsers.add_parser("pipeline", help="Deal pipeline view")

    sp = subparsers.add_parser("import", help="Import contacts")
    sp.add_argument("file")
    sp.add_argument("--format", dest="fmt", default="csv", choices=["csv", "json"])

    sp = subparsers.add_parser("export", help="Export contacts")
    sp.add_argument("--format", dest="fmt", default="csv", choices=["csv", "json"])
    sp.add_argument("--output")

    sp = subparsers.add_parser("interaction", help="Log interaction")
    sp.add_argument("id")
    sp.add_argument("--type", required=True, choices=["email", "linkedin", "twitter", "instagram", "call", "meeting", "note"])
    sp.add_argument("--note", required=True)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "dashboard":
        print(json.dumps(dashboard(), indent=2))
    elif args.command == "add":
        result = add_contact(args.name, email=args.email, company=args.company, role=args.role,
                             phone=args.phone, linkedin=args.linkedin, twitter=args.twitter,
                             tags=args.tags, source=args.source, notes=args.notes)
        print(json.dumps(result, indent=2))
    elif args.command == "list":
        print(json.dumps(list_contacts(args.stage, args.tag, args.source), indent=2))
    elif args.command == "search":
        print(json.dumps(search_contacts(args.query), indent=2))
    elif args.command == "view":
        result = view_contact(args.id)
        print(json.dumps(result, indent=2) if result else "Contact not found")
    elif args.command == "deal":
        result = update_deal(args.id, args.stage, args.value)
        if result:
            print(json.dumps(result, indent=2))
    elif args.command == "followup":
        result = schedule_followup(args.id, args.date, args.note)
        print(json.dumps(result, indent=2))
    elif args.command == "overdue":
        print(json.dumps(get_overdue(), indent=2))
    elif args.command == "pipeline":
        print(json.dumps(get_pipeline(), indent=2))
    elif args.command == "import":
        result = import_contacts(args.file, args.fmt)
        print(json.dumps(result, indent=2))
    elif args.command == "export":
        output = export_contacts(args.fmt, args.output)
        print(f"Exported to: {output}")
    elif args.command == "interaction":
        result = add_interaction(args.id, args.type, args.note)
        if result:
            print(json.dumps(result, indent=2))
        else:
            print("Contact not found")


if __name__ == "__main__":
    main()
