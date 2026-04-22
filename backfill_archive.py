#!/usr/bin/env python3
"""
backfill_archive.py

Walks the last N days of commits to index.html on main, extracts DATA,
and emits one daily-archive/YYYY-MM-DD.md per day.

Strategy: for each unique date in commit history (ET date of the
'Daily refresh' commit or the last commit of that day touching index.html),
take the latest commit for that date, extract DATA, and write the archive file.
If the archive file already exists, skip (don't overwrite).

Usage:
  python3 backfill_archive.py --days 30
"""
import re
import json
import os
import sys
import argparse
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR

# Reuse the writer
sys.path.insert(0, str(SCRIPT_DIR))
from write_daily_archive import (
    extract_data,
    build_archive_md,
    ARCHIVE_DIR,
    ensure_scaffold,
    regenerate_index,
    ET,
)


def run(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd or REPO_ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"cmd failed {cmd}: {r.stderr[:500]}")
    return r.stdout


def list_commits_for_file(path: str, since_date: str):
    """Return list of (sha, iso_date, subject) sorted chronologically (oldest first)."""
    out = run([
        "git", "log",
        f"--since={since_date}",
        "--pretty=format:%H\t%cI\t%s",
        "--",
        path,
    ])
    rows = []
    for line in out.strip().split("\n"):
        if not line:
            continue
        sha, iso, subject = line.split("\t", 2)
        rows.append((sha, iso, subject))
    rows.reverse()  # oldest first
    return rows


def pick_one_commit_per_day(rows):
    """Return dict: date (YYYY-MM-DD ET) -> sha (latest of that ET day)."""
    out = {}
    for sha, iso, _subj in rows:
        dt = datetime.fromisoformat(iso)
        et_date = dt.astimezone(ET).strftime("%Y-%m-%d")
        out[et_date] = sha  # last one wins (latest)
    return out


def load_data_from_commit(sha: str) -> dict | None:
    try:
        html = run(["git", "show", f"{sha}:index.html"])
    except Exception as e:
        print(f"  warn: could not read index.html at {sha[:8]}: {e}", file=sys.stderr)
        return None
    try:
        return extract_data(html)
    except Exception as e:
        print(f"  warn: could not parse DATA at {sha[:8]}: {e}", file=sys.stderr)
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--overwrite", action="store_true", help="Overwrite existing archive files")
    args = ap.parse_args()

    ensure_scaffold()

    since = (datetime.now(ET) - timedelta(days=args.days + 2)).strftime("%Y-%m-%d")
    print(f"Walking commits since {since} for index.html")

    rows = list_commits_for_file("index.html", since)
    print(f"  {len(rows)} commits touching index.html")

    by_day = pick_one_commit_per_day(rows)
    print(f"  {len(by_day)} distinct ET days")

    # Only keep last N days
    cutoff = datetime.now(ET).date() - timedelta(days=args.days)
    kept = {d: sha for d, sha in by_day.items() if datetime.strptime(d, "%Y-%m-%d").date() >= cutoff}
    print(f"  {len(kept)} days within the last {args.days} days")

    written = 0
    skipped = 0
    failed = 0
    for date_str in sorted(kept.keys()):
        out_path = ARCHIVE_DIR / f"{date_str}.md"
        if out_path.exists() and not args.overwrite:
            skipped += 1
            continue
        sha = kept[date_str]
        data = load_data_from_commit(sha)
        if data is None:
            failed += 1
            continue
        md = build_archive_md(data, date_str)
        out_path.write_text(md)
        written += 1
        print(f"  wrote {out_path.name}  (from {sha[:8]})")

    print(f"\nSummary: wrote={written} skipped={skipped} failed={failed}")
    regenerate_index()
    print(f"Regenerated {ARCHIVE_DIR/'INDEX.md'}")


if __name__ == "__main__":
    main()
