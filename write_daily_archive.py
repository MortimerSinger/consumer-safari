#!/usr/bin/env python3
"""
write_daily_archive.py

Extracts DATA from index.html and writes daily-archive/YYYY-MM-DD.md.
Then regenerates daily-archive/INDEX.md and trims files older than 90 days
unless their filename is listed in daily-archive/KEEP.md.

Called by the 4am ET cron after DATA is updated, and usable manually.

Usage:
  python3 write_daily_archive.py                # uses today (ET)
  python3 write_daily_archive.py --date 2026-04-22
  python3 write_daily_archive.py --from-html index.html --date 2026-04-22
"""
import re
import json
import os
import sys
import argparse
from datetime import datetime, timedelta, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR
ARCHIVE_DIR = REPO_ROOT / "daily-archive"
KEEP_FILE = ARCHIVE_DIR / "KEEP.md"
INDEX_FILE = ARCHIVE_DIR / "INDEX.md"
ET = timezone(timedelta(hours=-4))  # EDT; close enough for daily filename


def extract_data(html: str) -> dict:
    m = re.search(r"const DATA = (\{.*?\});\s*\n", html, re.DOTALL)
    if not m:
        raise ValueError("Could not find DATA object in index.html")
    return json.loads(m.group(1))


def flatten_stories(groups):
    """Given [{category, stories:[...]}, ...] return list of story dicts with category."""
    out = []
    if not isinstance(groups, list):
        return out
    for g in groups:
        if not isinstance(g, dict):
            continue
        cat = g.get("category", "")
        for s in g.get("stories", []) or []:
            if isinstance(s, dict):
                s = dict(s)
                s["_category"] = cat
                out.append(s)
    return out


def render_story_line(s: dict) -> str:
    headline = (s.get("headline") or s.get("title") or "").strip()
    source = (s.get("source") or "").strip()
    url = (s.get("url") or "").strip()
    blurb = (s.get("blurb") or s.get("summary") or "").strip()
    tag = (s.get("tag") or "").strip()
    # Keep blurb to one line
    blurb = re.sub(r"\s+", " ", blurb)[:260]
    bits = [f"**{headline}**"]
    if source:
        bits.append(f"({source})")
    if blurb:
        bits.append(f"— {blurb}")
    if url:
        bits.append(f"[link]({url})")
    if tag:
        bits.append(f"`{tag}`")
    return "- " + " ".join(bits)


def render_deal_line(d: dict) -> str:
    date = d.get("date", "")
    acq = d.get("acquirer", "")
    tgt = d.get("target", "")
    price = d.get("price", "")
    sector = d.get("sector", "")
    status = d.get("status", "")
    src = d.get("source", "")
    url = d.get("url", "")
    head = f"{acq} → {tgt}" if acq and tgt else (acq or tgt or "Deal")
    bits = [f"**{head}**"]
    meta = " · ".join(x for x in [date, price, sector, status] if x)
    if meta:
        bits.append(f"({meta})")
    if src:
        bits.append(f"— {src}")
    if url:
        bits.append(f"[link]({url})")
    return "- " + " ".join(bits)


def render_voice_line(v: dict) -> str:
    author = v.get("author", "")
    handle = v.get("handle", "")
    platform = v.get("platform", "")
    title = v.get("title", "")
    url = v.get("url", "")
    date = v.get("date", "")
    feed = v.get("feedType", "")
    head = f"{author}" + (f" {handle}" if handle else "")
    bits = [f"**{head}**"]
    if platform or date:
        meta = " · ".join(x for x in [platform, date] if x)
        bits.append(f"({meta})")
    if title:
        bits.append(f"— {title}")
    if url:
        bits.append(f"[link]({url})")
    if feed:
        bits.append(f"`{feed}`")
    return "- " + " ".join(bits)


def build_archive_md(data: dict, date_str: str) -> str:
    lines = [f"# Consumer Safari — {date_str}", ""]

    header_date = data.get("date", "")
    if header_date:
        lines.append(f"_Brief dated: {header_date}_")
        lines.append("")

    # Consumer
    consumer = flatten_stories(data.get("todayNews") or [])
    lines.append("## Consumer")
    if consumer:
        for s in consumer:
            lines.append(render_story_line(s))
    else:
        lines.append("_No consumer stories in today's brief._")
    lines.append("")

    # AI
    ai = flatten_stories(data.get("aiTodayNews") or [])
    lines.append("## AI")
    if ai:
        for s in ai:
            lines.append(render_story_line(s))
    else:
        lines.append("_No AI stories in today's brief._")
    lines.append("")

    # Deep Read
    deep = (data.get("deepRead") or []) + (data.get("aiDeepRead") or [])
    if deep:
        lines.append("## Deep Read")
        for r in deep:
            title = (r.get("title") or "").strip()
            source = (r.get("source") or "").strip()
            url = (r.get("url") or "").strip()
            summary = re.sub(r"\s+", " ", (r.get("summary") or r.get("takeaway") or ""))[:260]
            bits = [f"**{title}**"]
            if source:
                bits.append(f"({source})")
            if summary:
                bits.append(f"— {summary}")
            if url:
                bits.append(f"[link]({url})")
            lines.append("- " + " ".join(bits))
        lines.append("")

    # Deals
    deals = data.get("dealTracker") or []
    lines.append("## Deals (from dealTracker)")
    if deals:
        for d in deals:
            lines.append(render_deal_line(d))
    else:
        lines.append("_No deals in tracker._")
    lines.append("")

    # Voices added today (approximated: top 5 most recently added by position in the
    # curated list, since newest voices are prepended to the roster)
    voices = data.get("voices") or []
    lines.append("## Voices added today")
    if voices:
        for v in voices[:5]:
            lines.append(render_voice_line(v))
    else:
        lines.append("_No voices._")
    lines.append("")

    return "\n".join(lines) + "\n"


def load_keep() -> set:
    if not KEEP_FILE.exists():
        return set()
    out = set()
    for ln in KEEP_FILE.read_text().splitlines():
        ln = ln.strip()
        if not ln or ln.startswith("#"):
            continue
        # Accept "2026-04-22" or "2026-04-22.md"
        if ln.endswith(".md"):
            out.add(ln)
        elif re.match(r"^\d{4}-\d{2}-\d{2}$", ln):
            out.add(ln + ".md")
    return out


def regenerate_index():
    files = sorted(
        [p for p in ARCHIVE_DIR.glob("*.md") if re.match(r"^\d{4}-\d{2}-\d{2}\.md$", p.name)],
        reverse=True,
    )
    lines = ["# Consumer Safari — Daily Archive Index", "", f"Total days: **{len(files)}**", "", "| Date | Stories | File |", "|------|---------|------|"]
    for p in files:
        txt = p.read_text()
        consumer_count = len(re.findall(r"^- ", _section(txt, "## Consumer"), flags=re.MULTILINE))
        ai_count = len(re.findall(r"^- ", _section(txt, "## AI"), flags=re.MULTILINE))
        date = p.stem
        lines.append(f"| {date} | {consumer_count} consumer · {ai_count} AI | [{p.name}]({p.name}) |")
    INDEX_FILE.write_text("\n".join(lines) + "\n")


def _section(md: str, header: str) -> str:
    """Return the body lines of a specific section header until the next '## '."""
    m = re.search(re.escape(header) + r"\n(.*?)(?=\n## |\Z)", md, flags=re.DOTALL)
    return m.group(1) if m else ""


def trim_old(max_age_days: int = 90):
    keep = load_keep()
    cutoff = datetime.now(ET).date() - timedelta(days=max_age_days)
    removed = []
    for p in ARCHIVE_DIR.glob("*.md"):
        if p.name in ("INDEX.md", "KEEP.md", "README.md"):
            continue
        m = re.match(r"^(\d{4})-(\d{2})-(\d{2})\.md$", p.name)
        if not m:
            continue
        d = datetime(int(m.group(1)), int(m.group(2)), int(m.group(3))).date()
        if d < cutoff and p.name not in keep:
            removed.append(p.name)
            p.unlink()
    return removed


def ensure_scaffold():
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    if not KEEP_FILE.exists():
        KEEP_FILE.write_text(
            "# KEEP — allowlist for daily archive files that should NEVER be trimmed.\n"
            "# One filename per line. Accepts '2026-04-22' or '2026-04-22.md'.\n"
            "# Morty maintains this file.\n"
        )


def write_for_html(html: str, date_str: str) -> Path:
    ensure_scaffold()
    data = extract_data(html)
    md = build_archive_md(data, date_str)
    out_path = ARCHIVE_DIR / f"{date_str}.md"
    out_path.write_text(md)
    return out_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", help="YYYY-MM-DD (default: today ET)")
    ap.add_argument("--from-html", default=str(REPO_ROOT / "index.html"))
    ap.add_argument("--skip-trim", action="store_true")
    args = ap.parse_args()

    date_str = args.date or datetime.now(ET).strftime("%Y-%m-%d")
    html_path = Path(args.from_html)
    if not html_path.exists():
        print(f"ERROR: {html_path} not found", file=sys.stderr)
        sys.exit(1)

    html = html_path.read_text()
    out_path = write_for_html(html, date_str)
    print(f"Wrote {out_path}")

    if not args.skip_trim:
        removed = trim_old()
        if removed:
            print(f"Trimmed {len(removed)} old files: {removed}")

    regenerate_index()
    print(f"Regenerated {INDEX_FILE}")


if __name__ == "__main__":
    main()
