#!/usr/bin/env python3
"""
Operations Manager Script
System health checks, log management, backups, and rate limiter resets.

Usage:
  python ops_manager.py status           # Health check
  python ops_manager.py logs --tail 20   # View recent logs
  python ops_manager.py cleanup --days 30 # Clean old files
  python ops_manager.py backup --output output/backups/
  python ops_manager.py reset            # Reset rate limiters
"""

import argparse
import json
import os
import shutil
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path


def check_status() -> dict:
    """Run full system health check."""
    checks = {}

    # Python
    checks["python"] = {"ok": True, "version": sys.version.split()[0]}

    # Node.js
    node_ok = os.system("node --version > /dev/null 2>&1") == 0 or os.system("node --version >nul 2>&1") == 0
    checks["node"] = {"ok": node_ok}

    # Canvas
    canvas_deps = Path("tldraw-canvas/node_modules").exists()
    checks["canvas"] = {"ok": canvas_deps, "note": "Run: cd tldraw-canvas && npm install" if not canvas_deps else "Ready"}

    # Gmail OAuth
    creds = Path(".claude/credentials.json").exists() or Path("credentials.json").exists()
    token = Path(".claude/token.json").exists() or Path("token.json").exists()
    checks["gmail_oauth"] = {"ok": creds, "credentials": creds, "token": token}

    # Exa API key
    exa_key = bool(os.environ.get("EXA_API_KEY"))
    if not exa_key:
        for env_file in [".env", ".env.local"]:
            if Path(env_file).exists():
                content = Path(env_file).read_text()
                if "EXA_API_KEY=" in content:
                    exa_key = True
                    break
    checks["exa_api"] = {"ok": exa_key}

    # Output directories
    output_dirs = ["output/workflows", "output/logs", "output/discovery", "output/reports"]
    missing = [d for d in output_dirs if not Path(d).exists()]
    checks["output_dirs"] = {"ok": len(missing) == 0, "missing": missing}

    # Rate limiter
    rate_file = Path("output/rate_limits.json")
    checks["rate_limiter"] = {"ok": rate_file.exists()}

    # Team config
    team_file = Path("output/team.json") if Path("output/team.json").exists() else Path(".claude/team.json")
    checks["team_config"] = {"ok": team_file.exists()}

    # Overall
    all_ok = all(c.get("ok", False) for c in checks.values())
    return {"healthy": all_ok, "checks": checks, "timestamp": datetime.now().isoformat()}


def view_logs(tail: int = 20, campaign: str = None, platform: str = None, level: str = None) -> list:
    """Read recent activity logs."""
    log_dir = Path("output/logs")
    if not log_dir.exists():
        return []

    entries = []
    for log_file in sorted(log_dir.glob("**/*.json"), key=lambda p: p.stat().st_mtime, reverse=True):
        try:
            data = json.loads(log_file.read_text())
            if isinstance(data, list):
                entries.extend(data)
            elif isinstance(data, dict):
                entries.append(data)
        except (json.JSONDecodeError, Exception):
            continue

    # Apply filters
    if campaign:
        entries = [e for e in entries if campaign.lower() in str(e.get("campaign", "")).lower()]
    if platform:
        entries = [e for e in entries if platform.lower() in str(e.get("platform", "")).lower()]
    if level:
        entries = [e for e in entries if e.get("level", "").lower() == level.lower()]

    # Sort by timestamp descending
    entries.sort(key=lambda e: e.get("timestamp", ""), reverse=True)
    return entries[:tail]


def cleanup(days: int = 30) -> dict:
    """Remove old logs and temporary files."""
    cutoff = datetime.now() - timedelta(days=days)
    removed = {"files": 0, "bytes": 0}

    for directory in ["output/logs", "output/reports"]:
        dir_path = Path(directory)
        if not dir_path.exists():
            continue
        for f in dir_path.rglob("*"):
            if f.is_file() and datetime.fromtimestamp(f.stat().st_mtime) < cutoff:
                size = f.stat().st_size
                f.unlink()
                removed["files"] += 1
                removed["bytes"] += size

    return {"removed": removed, "cutoff_date": cutoff.isoformat()}


def backup(output_dir: str = "output/backups") -> dict:
    """Create a timestamped backup of all data."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    backup_name = f"backup-{timestamp}"
    backup_path = Path(output_dir) / backup_name

    items_to_backup = [
        "output/discovery",
        "output/workflows",
        ".claude/templates",
        "output/team.json",
        ".claude/team.json",
        "output/rate_limits.json",
    ]

    backup_path.mkdir(parents=True, exist_ok=True)
    copied = 0
    for item in items_to_backup:
        src = Path(item)
        if src.exists():
            dst = backup_path / item
            dst.parent.mkdir(parents=True, exist_ok=True)
            if src.is_dir():
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)
            copied += 1

    # Create zip
    zip_path = shutil.make_archive(str(backup_path), 'zip', str(backup_path))
    shutil.rmtree(backup_path)

    return {"backup": zip_path, "items_backed_up": copied, "timestamp": timestamp}


def reset_rate_limits(platform: str = None) -> dict:
    """Reset rate limiter state."""
    rate_file = Path("output/rate_limits.json")
    if not rate_file.exists():
        return {"reset": False, "error": "No rate_limits.json found"}

    if platform:
        data = json.loads(rate_file.read_text())
        if platform in data:
            data[platform] = {}
            rate_file.write_text(json.dumps(data, indent=2))
            return {"reset": True, "platform": platform}
        return {"reset": False, "error": f"Platform '{platform}' not found"}

    # Reset all
    rate_file.write_text(json.dumps({}, indent=2))
    return {"reset": True, "platform": "all"}


def main():
    parser = argparse.ArgumentParser(description="Operations Manager")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("status", help="System health check")

    sp = subparsers.add_parser("logs", help="View activity logs")
    sp.add_argument("--tail", type=int, default=20)
    sp.add_argument("--campaign", help="Filter by campaign name")
    sp.add_argument("--platform", help="Filter by platform")
    sp.add_argument("--level", help="Filter by level (info/error/warn)")

    sp = subparsers.add_parser("cleanup", help="Clean old files")
    sp.add_argument("--days", type=int, default=30)

    sp = subparsers.add_parser("backup", help="Backup all data")
    sp.add_argument("--output", default="output/backups")

    sp = subparsers.add_parser("reset", help="Reset rate limiters")
    sp.add_argument("--platform", help="Reset specific platform only")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "status":
        print(json.dumps(check_status(), indent=2))
    elif args.command == "logs":
        entries = view_logs(args.tail, args.campaign, args.platform, args.level)
        print(json.dumps(entries, indent=2))
    elif args.command == "cleanup":
        result = cleanup(args.days)
        print(json.dumps(result, indent=2))
    elif args.command == "backup":
        result = backup(args.output)
        print(json.dumps(result, indent=2))
    elif args.command == "reset":
        result = reset_rate_limits(args.platform)
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
