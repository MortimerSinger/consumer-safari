#!/usr/bin/env python3
"""
build_email_template.py — PINNED Consumer Safari email template.

This is the ONE email rendering script that all daily cron runs MUST use.
The cron task spec references this file by exact path. Do not improvise.

USAGE
-----
1. Compose your day's content as a Python dict matching the schema below.
2. Save it to /home/user/workspace/morning-briefing/email_data_YYYY-MM-DD.json.
3. Call:  python3 build_email_template.py YYYY-MM-DD
4. The script reads the JSON, renders HTML, validates, queries Supabase
   for subscribers, and sends via Resend.

SECURITY
--------
Resend API key is read from the RESEND_API_KEY environment variable.
NEVER paste it inline. NEVER commit it to git.

Set it before running:
   export RESEND_API_KEY=re_xxxxxxxxxxxxxxx

Supabase service-role key is also read from SUPABASE_SERVICE_ROLE_KEY env var.

CONTENT SCHEMA (email_data_YYYY-MM-DD.json)
-------------------------------------------
{
  "date": "Saturday, April 25, 2026",
  "subject": "Consumer Safari Daily Brief — April 25, 2026",
  "brief": "One paragraph...",
  "key_numbers": [
    {"label": "...", "value": "...", "change": "...", "direction": "up|down"},
    ...up to 4
  ],
  "consumer_stories": [
    {"cat": "🥫 CPG & Food", "items": [
      {"h": "...", "s": "...", "u": "https://...", "b": "..."},
      ...
    ]},
    ...
  ],
  "ai_stories": [
    {"cat": "🤖 AI & Labor", "items": [...]},
    ...
  ],
  "banner": null  // optional: {"kind": "warning|info", "title": "...", "body": "..."}
}

VALIDATION
----------
Before sending, the script scans rendered HTML for tell-tale debug strings
('{\\'headline\\'', '{\\'category\\'', '\\'stories\\':') and aborts the send
if any are present. This catches the dict-stringification bug observed
on 2026-04-25.
"""

import json
import os
import sys
import subprocess
import time
from pathlib import Path

WORKSPACE = Path("/home/user/workspace/morning-briefing")


def render_key_number(kn):
    arrow = "↑" if kn["direction"] == "up" else "↓"
    color = "#059669" if kn["direction"] == "up" else "#DC2626"
    return f'''
<td width="50%" style="padding:10px;vertical-align:top;">
  <div style="background:#F9FAFB;border-radius:10px;padding:14px 16px;border:1px solid #E5E7EB;">
    <div style="font-size:11px;font-weight:600;color:#6B7280;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px;">{kn["label"]}</div>
    <div style="font-size:24px;font-weight:800;color:#111827;line-height:1.1;">{kn["value"]} <span style="color:{color};font-size:18px;">{arrow}</span></div>
    <div style="font-size:13px;color:#6B7280;margin-top:4px;">{kn["change"]}</div>
  </div>
</td>'''


def render_story(item):
    return f'''
<div style="margin-bottom:18px;">
  <a href="{item['u']}" style="text-decoration:none;color:#111827;">
    <div style="font-size:19px;font-weight:700;color:#111827;line-height:1.25;margin-bottom:6px;">{item['h']}</div>
  </a>
  <div style="font-size:13px;color:#6D28D9;font-weight:600;margin-bottom:6px;">{item['s']}</div>
  <div style="font-size:17px;color:#374151;line-height:1.5;">{item['b']}</div>
</div>'''


def render_category(group):
    """group MUST be a dict with 'cat' (string) and 'items' (list of story dicts).
    Iterating items inline below; we never f-string a dict directly."""
    if not isinstance(group, dict) or "cat" not in group or "items" not in group:
        raise ValueError(f"Bad category group: {group!r}")
    if not isinstance(group["cat"], str):
        raise ValueError(f"cat must be a string, got {type(group['cat'])}: {group['cat']!r}")
    stories_html = "".join(render_story(i) for i in group["items"])
    return f'''
<div style="margin-bottom:28px;">
  <div style="font-size:14px;font-weight:700;color:#6D28D9;text-transform:uppercase;letter-spacing:1px;margin-bottom:14px;padding-bottom:8px;border-bottom:2px solid #EDE9FE;">{group["cat"]}</div>
  {stories_html}
</div>'''


def render_banner(banner):
    if not banner:
        return ""
    kind = banner.get("kind", "info")
    bg, border, label_color, body_color = {
        "warning": ("#FEF3C7", "#D97706", "#92400E", "#78350F"),
        "info":    ("#F5F3FF", "#6D28D9", "#6D28D9", "#1F2937"),
    }.get(kind, ("#F5F3FF", "#6D28D9", "#6D28D9", "#1F2937"))
    title = banner.get("title", "")
    body = banner.get("body", "")
    return f'''
<div style="background:{bg};border-left:4px solid {border};padding:14px 18px;margin:0 0 20px 0;border-radius:4px;">
  <div style="font-size:12px;font-weight:700;color:{label_color};text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">{title}</div>
  <div style="font-size:15px;color:{body_color};line-height:1.5;">{body}</div>
</div>'''


def build_email(data):
    # Validate top-level
    for k in ("date", "subject", "brief", "key_numbers", "consumer_stories", "ai_stories"):
        if k not in data:
            raise ValueError(f"Missing required key: {k}")

    # Render key numbers in 2x2 grid
    key_pairs = []
    for i in range(0, len(data["key_numbers"]), 2):
        row = "".join(render_key_number(kn) for kn in data["key_numbers"][i:i+2])
        key_pairs.append(f'<tr>{row}</tr>')
    key_numbers_html = (
        f'<table width="100%" cellpadding="0" cellspacing="0" '
        f'style="border-collapse:separate;margin:8px -10px 18px;">'
        f'{"".join(key_pairs)}</table>'
    )

    consumer_html = "".join(render_category(g) for g in data["consumer_stories"])
    ai_html = "".join(render_category(g) for g in data["ai_stories"])
    banner_html = render_banner(data.get("banner"))

    html = f'''<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#F9FAFB;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;">
<div style="max-width:600px;margin:0 auto;background:#FFFFFF;padding:28px;">

  <div style="text-align:center;padding-bottom:20px;border-bottom:1px solid #E5E7EB;">
    <div style="font-size:28px;font-weight:900;color:#6D28D9;letter-spacing:2px;">CONSUMER SAFARI</div>
    <div style="font-size:12px;font-weight:600;color:#6B7280;letter-spacing:2px;margin-top:4px;">THE MORNING BRIEFING</div>
    <div style="font-size:14px;color:#6B7280;margin-top:12px;">{data["date"]}</div>
    <div style="font-size:14px;margin-top:8px;"><a href="https://www.consumersafari.com" style="color:#6D28D9;text-decoration:underline;font-weight:600;">To save articles and more, go to ConsumerSafari.com</a></div>
  </div>

  {banner_html}

  <div style="background:#F5F3FF;border-left:4px solid #6D28D9;padding:18px 20px;margin:0 0 20px 0;border-radius:4px;">
    <div style="font-size:12px;font-weight:700;color:#6D28D9;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:10px;">Your Brief</div>
    <div style="font-size:18px;color:#1F2937;line-height:1.55;">{data["brief"]}</div>
  </div>

  {key_numbers_html}

  {consumer_html}

  <hr style="border:none;border-top:1px solid #E5E7EB;margin:32px 0;">
  <div style="font-size:16px;font-weight:700;color:#6D28D9;text-transform:uppercase;letter-spacing:1.5px;text-align:center;margin-bottom:24px;">AI &amp; TECHNOLOGY</div>

  {ai_html}

  <div style="text-align:center;margin-top:32px;padding:20px 0;">
    <a href="https://www.consumersafari.com" style="display:inline-block;background:#6D28D9;color:#FFFFFF;text-decoration:none;font-weight:700;padding:14px 32px;border-radius:8px;font-size:15px;">Read Full Briefing</a>
  </div>

  <div style="text-align:center;margin-top:28px;padding-top:20px;border-top:1px solid #E5E7EB;font-size:11px;color:#9CA3AF;letter-spacing:1px;text-transform:uppercase;">Powered by TCP Intelligence</div>

</div>
</body>
</html>'''
    return html


def sanity_check(html):
    """Abort if rendered HTML contains telltale Python-dict debug fragments.
    Catches the 2026-04-25 bug where a dict was stringified into a header."""
    forbidden = [
        "{'headline'",
        "{'category'",
        "'stories':",
        "'tag': '",
        "'blurb':",
        "{\"headline\"",
        "{\"category\"",
        "\"stories\":",
    ]
    for needle in forbidden:
        if needle in html:
            raise RuntimeError(
                f"SANITY CHECK FAILED: rendered HTML contains debug string {needle!r}. "
                f"Aborting send. Inspect /tmp/render_dump.html to debug."
            )


def get_subscribers():
    sb_url = "https://ugmirwqwlggdemwklcwi.supabase.co"
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
    if not key:
        raise RuntimeError(
            "SUPABASE_SERVICE_ROLE_KEY not set in environment. "
            "Cannot fetch subscriber list."
        )
    result = subprocess.run(
        ["curl", "-s",
         f"{sb_url}/rest/v1/email_preferences?daily_digest=eq.true&select=email",
         "-H", f"apikey: {key}",
         "-H", f"Authorization: Bearer {key}"],
        capture_output=True, text=True, check=True
    )
    return json.loads(result.stdout)


def send_email(to_email, subject, html):
    api_key = os.environ.get("RESEND_API_KEY")
    if not api_key:
        raise RuntimeError(
            "RESEND_API_KEY not set in environment. "
            "Set it with: export RESEND_API_KEY=re_xxxxx before running."
        )
    payload = {
        "from": "Consumer Safari <briefing@consumersafari.com>",
        "to": [to_email],
        "subject": subject,
        "html": html,
    }
    result = subprocess.run(
        ["curl", "-s", "-X", "POST", "https://api.resend.com/emails",
         "-H", f"Authorization: Bearer {api_key}",
         "-H", "Content-Type: application/json",
         "-d", json.dumps(payload)],
        capture_output=True, text=True
    )
    try:
        resp = json.loads(result.stdout)
        return resp.get("id"), result.stdout
    except Exception:
        return None, result.stdout


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 build_email_template.py YYYY-MM-DD [--dry-run]")
        sys.exit(1)
    date_str = sys.argv[1]
    dry_run = "--dry-run" in sys.argv

    data_path = WORKSPACE / f"email_data_{date_str}.json"
    if not data_path.exists():
        print(f"ERROR: {data_path} not found. Create it with the schema documented at top of this file.")
        sys.exit(1)

    data = json.loads(data_path.read_text())
    html = build_email(data)

    # Always dump for inspection
    dump_path = Path("/tmp/render_dump.html")
    dump_path.write_text(html)
    out_path = WORKSPACE / f"email_{date_str}.html"
    out_path.write_text(html)
    print(f"Rendered: {out_path} ({len(html)} chars)")

    # Mandatory sanity check
    sanity_check(html)
    print("Sanity check: PASSED")

    if dry_run:
        print("Dry run — not sending.")
        return

    subs = get_subscribers()
    print(f"{len(subs)} subscribers")
    ok = 0; fail = 0
    for i, r in enumerate(subs, 1):
        email = r["email"]
        msg_id, raw = send_email(email, data["subject"], html)
        if msg_id:
            ok += 1
        else:
            fail += 1
            print(f"FAIL {email}: {raw[:200]}")
        if i % 10 == 0:
            print(f"{i}/{len(subs)} sent — ok={ok} fail={fail}")
        time.sleep(0.5)
    print(f"\nFinal: ok={ok} fail={fail} of {len(subs)}")


if __name__ == "__main__":
    main()
