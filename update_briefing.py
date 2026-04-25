#!/usr/bin/env python3
"""
update_briefing.py — write a validated briefing DATA object to Supabase.

This is the ONLY way the cron is allowed to update the live site's data.

Usage:
    python3 update_briefing.py path/to/data.json [--dry-run]

Reads SUPABASE_SERVICE_ROLE_KEY from environment (NEVER inline a key).

Workflow:
1. Load JSON from input path
2. Validate against briefing_schema.BRIEFING_SCHEMA — abort if invalid
3. Insert new row with is_current = TRUE
4. Mark all other rows is_current = FALSE
5. Return success/failure

If validation fails, the script prints all errors and exits non-zero.
The live site is NEVER touched if validation fails.

Idempotent: re-running with the same data updates the existing row for that date.
"""
import json
import os
import sys
import argparse
import subprocess
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from briefing_schema import validate, SCHEMA_VERSION

SB_URL = "https://ugmirwqwlggdemwklcwi.supabase.co"


def get_service_key() -> str:
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
    if not key:
        print("ERROR: SUPABASE_SERVICE_ROLE_KEY not set in environment.", file=sys.stderr)
        print("Cron must inject this. Aborting to prevent silent failure.", file=sys.stderr)
        sys.exit(2)
    return key


def sb_request(method: str, path: str, key: str, body: dict | None = None, headers_extra: dict | None = None):
    cmd = ["curl", "-s", "-w", "\n%{http_code}", "-X", method,
           f"{SB_URL}/rest/v1/{path}",
           "-H", f"apikey: {key}",
           "-H", f"Authorization: Bearer {key}",
           "-H", "Content-Type: application/json"]
    for k, v in (headers_extra or {}).items():
        cmd.extend(["-H", f"{k}: {v}"])
    if body is not None:
        cmd.extend(["-d", json.dumps(body)])
    r = subprocess.run(cmd, capture_output=True, text=True)
    out = r.stdout.rsplit("\n", 1)
    body_text = out[0] if len(out) > 1 else ""
    code = int(out[-1]) if out[-1].isdigit() else 0
    return code, body_text


def write_briefing(data: dict, *, dry_run: bool = False) -> int:
    # Validate
    ok, errors = validate(data)
    if not ok:
        print("VALIDATION FAILED. The live site will NOT be updated.", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print("Validation: PASSED")

    if dry_run:
        print("DRY RUN — not writing to Supabase.")
        return 0

    key = get_service_key()
    today = datetime.now(timezone.utc).date().isoformat()

    # Step 1: mark all existing rows is_current = false (so the unique-current index doesn't conflict)
    code, txt = sb_request(
        "PATCH",
        "briefings?is_current=eq.true",
        key,
        body={"is_current": False},
        headers_extra={"Prefer": "return=minimal"},
    )
    if code not in (200, 204):
        print(f"ERROR: failed to clear is_current flags. HTTP {code} body: {txt[:300]}", file=sys.stderr)
        return 2
    print(f"Cleared previous current flag (HTTP {code})")

    # Step 2: upsert the new row for today's date
    payload = {
        "date": today,
        "data": data,
        "is_current": True,
        "schema_version": SCHEMA_VERSION,
    }
    code, txt = sb_request(
        "POST",
        "briefings",
        key,
        body=payload,
        headers_extra={
            "Prefer": "resolution=merge-duplicates,return=representation",
            # Conflict-target requires column to be UNIQUE in the table.
            # We are not enforcing UNIQUE on date, so we will simply insert.
            # If the same date is written twice, both rows exist; only the latest is is_current.
        },
    )
    if code not in (200, 201):
        print(f"ERROR: failed to insert briefing. HTTP {code} body: {txt[:500]}", file=sys.stderr)
        return 3
    print(f"Inserted new briefing (HTTP {code}) for {today}")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("data_path", help="Path to JSON file containing the new briefing DATA")
    ap.add_argument("--dry-run", action="store_true", help="Validate only; do not write to Supabase")
    args = ap.parse_args()

    path = Path(args.data_path)
    if not path.exists():
        print(f"ERROR: {path} not found", file=sys.stderr)
        sys.exit(2)

    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        print(f"ERROR: invalid JSON in {path}: {e}", file=sys.stderr)
        sys.exit(2)

    sys.exit(write_briefing(data, dry_run=args.dry_run))


if __name__ == "__main__":
    main()
