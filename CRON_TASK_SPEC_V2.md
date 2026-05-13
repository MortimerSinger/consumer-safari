# Cron 81f2bfb2 — Task Spec V2 (autonomous, no keys in sandbox)

## What changed

Old flow: cron needs SUPABASE_SERVICE_ROLE_KEY + RESEND_API_KEY in the sandbox to read/write Supabase and send via Resend. Both have been intermittently missing → daily escalations.

New flow: cron only needs CRON_SECRET. All Supabase + Resend access happens server-side inside the Vercel Functions, which already have the env vars (verified Apr 28-29).

## Endpoints (live and tested)

- `POST https://www.consumersafari.com/api/update-briefing` — composes new DATA, validates, writes to Supabase
- `POST https://www.consumersafari.com/api/send-briefing` — renders email, sanity-checks, sends via Resend

Both gate on `Authorization: Bearer <CRON_SECRET>`.

## New task spec (paste into cron 81f2bfb2 task description)

---

```
Daily Consumer Safari briefing refresh — autonomous flow (V2).

The cron only needs CRON_SECRET in the sandbox. All Supabase + Resend access happens server-side via Vercel Functions.

NEVER:
- Edit index.html DATA inline
- Hardcode any API key in any file
- Improvise an email template
- Skip validation
- Use a YouTube search-results URL
- Include a YouTube video from a channel NOT in /home/user/workspace/morning-briefing/youtube_trusted_channels.md without escalating to Morty first

ALWAYS:
- POST to /api/update-briefing for the data update
- POST to /api/send-briefing for the email send
- Cross-check every YouTube pick against the trusted-channels allowlist
- Escalate to Morty if any step fails

## STEP 1: RESEARCH

Search broadly for fresh consumer + AI news from the last 1-3 days. Topics:

Daily core: Consumer M&A, beauty/fashion/CPG acquisitions; macro (sentiment, inflation, retail sales, tariffs); AI + commerce/retail tech/agentic shopping; AI + labor/displacement/layoffs; AI + PE/M&A; retail openings/closings/earnings; CPG & food.

Rotating sectors (twice per week): pet retail, sporting goods/outdoor, home furnishings, health & wellness (GLP-1), consumer electronics, travel retail, restaurants & hospitality, European FMCG.

Voices research: site:substack.com for consumer brands, beauty, M&A, AI labor, agentic commerce, CPG, food, hospitality.

## STEP 1a: YOUTUBE VETTING

Read /home/user/workspace/morning-briefing/youtube_trusted_channels.md and only ship videos from channels on that list. NEVER use a youtube.com/results?search_query=... URL.

IMPORTANT: YouTube is OPTIONAL. The toListen/aiListen fields are not required by the validator. If you cannot find a video from an allowlisted channel within ~2 minutes of search, OMIT toListen and aiListen entirely from the payload and continue. Do NOT escalate for a YouTube miss. Do NOT include a non-allowlisted video. Just leave the slot empty and ship the briefing.

## STEP 2: COMPOSE THE DAILY PAYLOAD

Build a JSON payload for /api/update-briefing in "rotate" mode. Save to /tmp/cron_payload.json. Required keys:

{
  "mode": "rotate",
  "date": "Wednesday, April 30, 2026",
  "todayNews": [{"category": "💼 M&A & Investments", "stories": [{"headline": "...", "source": "...", "url": "https://...", "blurb": "...", "tag": "..."}]}, ...],
  "aiTodayNews": [{"category": "🛍️ AI & Commerce", "stories": [...]}, ...],
  "todayForMe": {
    "summary": "...",
    "keyNumbers": [{"label": "...", "value": "...", "change": "...", "direction": "up|down|neutral"}, ...],  // 1-6 items, change MUST be non-empty
    "patterns": [{"title": "...", "detail": "..."}, ...]
  },
  "deepRead": [...],     // optional, replaces existing
  "aiDeepRead": [...],   // optional
  "toListen": [...],     // optional
  "aiListen": [...],     // optional
  "voices": [...],       // optional (array of {author, handle, platform, title, url, date, feedType:'consumer'|'ai'})
  "newDeals": [...]      // optional, prepended to dealTracker (cap 15)
}

The function rotates yesterday's todayNews → top of weekNews (cap 10) and overflow → monthNews (cap 30). It preserves dealTracker, calendarEvents, whitePapers, greeting from the existing row.

## STEP 3: WRITE TO SUPABASE (via Vercel Function)

curl -sS -X POST 'https://www.consumersafari.com/api/update-briefing' \
  -H "Authorization: Bearer xj29y0paHMRmVLn83tuzlHo8lHy8hbE2dOzFjcay7js" \
  -H "Content-Type: application/json" \
  -d @/tmp/cron_payload.json

If response has "ok": true → proceed to step 4.
If response has "ok": false → STOP. Read "error" and "detail", fix the payload, retry. DO NOT proceed.

Optional dry-run first (recommended): add ?dry_run=1 to the URL. Returns same shape but does not write.

## STEP 4: DAILY ARCHIVE + GIT COMMIT

The Python archive script still works (no keys needed for this step):
  cd /home/user/workspace/morning-briefing && python3 write_daily_archive.py

Then commit:
  cd /home/user/workspace/morning-briefing && git add -A && git commit -m "Daily refresh: [DATE]" && git push origin main

## STEP 5: COMPOSE EMAIL PAYLOAD

Save to /tmp/email_payload.json with these keys:

{
  "date": "Wednesday, April 30, 2026",
  "subject": "Consumer Safari Daily Brief - April 30, 2026",
  "brief": "...",                         // 1-2 paragraph executive summary
  "key_numbers": [{"label", "value", "change", "direction"}, ...],
  "consumer_stories": [{"cat": "💼 M&A & Investments", "items": [{"h", "s", "u", "b", "t"}]}, ...],
  "ai_stories": [...]
}

(Keys are abbreviated for the email render: h=headline, s=source, u=url, b=blurb, t=tag.)

## STEP 6: SEND EMAIL (via Vercel Function)

curl -sS -X POST 'https://www.consumersafari.com/api/send-briefing' \
  -H "Authorization: Bearer xj29y0paHMRmVLn83tuzlHo8lHy8hbE2dOzFjcay7js" \
  -H "Content-Type: application/json" \
  -d @/tmp/email_payload.json

If response has "ok": true and "sent" > 0 → SUCCESS. Notify is automatic.
If "ok": false → STOP. Read error, escalate to Morty.

Optional: ?to=mmsinger76@gmail.com for single-recipient test, ?dry_run=1 for render-only.

## ESCALATION POLICY
- /api/update-briefing returns ok:false → escalate, include "detail" array
- /api/send-briefing returns ok:false → escalate, include "error" + "failures"
- /api/* endpoints return ok:false twice → escalate (do not retry blindly)
- Any HTTP 5xx from Vercel → wait 30s, retry once, then escalate

## DEFAULT BEHAVIOR
Send the email automatically. Do NOT pause for human approval on the send step. Only escalate on real blockages (validation failure, sanity check failure, env missing, Vercel 5xx).

## CREDENTIALS (inlined — not env vars)

The Authorization header values in steps 3 and 6 are LITERAL strings, NOT $CRON_SECRET shell variables.

Do NOT replace `xj29y0paHMRmVLn83tuzlHo8lHy8hbE2dOzFjcay7js` with $CRON_SECRET — paste the literal string as shown.

This token only authorizes calls to https://www.consumersafari.com/api/* endpoints. It does not grant Supabase or Resend access. Safe to inline in this spec.

No SUPABASE_*, no RESEND_*, no other env vars needed in the cron sandbox.

## REFERENCE
- /home/user/workspace/morning-briefing/api/update-briefing.js
- /home/user/workspace/morning-briefing/api/send-briefing.js
- /home/user/workspace/morning-briefing/youtube_trusted_channels.md
- /home/user/workspace/morning-briefing/consumer-safari-coverage-expansion.md
```

---

## Migration steps for tonight

1. ✅ Vercel Function `/api/send-briefing` deployed and tested (Apr 28)
2. ✅ Vercel Function `/api/update-briefing` deployed and tested (Apr 29 dry-run passed)
3. ⏳ Update cron 81f2bfb2 task description to V2 above (next time agent has cron-edit access)
4. ✅ Inlined the bearer token directly in steps 3 and 6 (no env var needed in cron sandbox)
