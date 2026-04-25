# YouTube Trusted Channels Allowlist

This file gates which YouTube channels can be auto-included in the daily briefing's
`toListen` and `aiListen` sections without escalation to Morty.

**Rule for the cron:**

1. If a video is from a channel in this allowlist → ship it.
2. If a video is from a channel NOT in this list → escalate to Morty with:
   - Channel name and handle
   - Subscriber count
   - View count of the specific video
   - One-line "why I want to include this"
3. Morty replies yes/no. If yes, add the channel to this list. If no, drop it.

**Quality floor (apply even to allowlisted channels):**
- Never use a `youtube.com/results?search_query=...` or `youtube.com/search?...` URL — that is a search results page, not a video.
- Specific video URLs only (`/watch?v=...`).
- If a specific video on an allowlisted channel feels low-quality, use judgment to skip without bothering Morty.

---

## Trusted channels (Morty's roster)

_(awaiting Morty's list — current state: empty)_

Format when populated:
- **Channel name** (channel handle / URL) — focus area

---

## Recently rejected (for cron memory, don't re-pitch)

- (none yet)
