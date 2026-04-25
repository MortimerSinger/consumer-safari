# YouTube Trusted Channels Allowlist

This file gates which YouTube channels can be auto-included in the daily briefing's
`toListen` and `aiListen` sections without escalation to Morty.

## Rule for the cron

1. If a video is from a channel in this allowlist → ship it.
2. If a video is from a channel NOT in this list → escalate to Morty with:
   - Channel name and handle
   - Subscriber count
   - View count of the specific video
   - One-line "why I want to include this"
3. Morty replies yes/no. If yes, add the channel to this list. If no, drop it (and add to "Recently rejected" so we don't re-pitch).

## Quality floor (apply even to allowlisted channels)

- Never use a `youtube.com/results?search_query=...` or `youtube.com/search?...` URL — that is a search results page, not a video.
- Specific video URLs only (`/watch?v=...`).
- If a specific video on an allowlisted channel feels low-quality (off-topic, clickbait, recycled), use judgment to skip without bothering Morty.

---

## Trusted channels (Morty's roster, as of 2026-04-25)

Match channel names case-insensitively and tolerate minor variations
(e.g., "All-In" / "All-In Podcast" / "All In Pod" all map to All-In Podcast).

- **Lex Fridman** — long-form interviews on AI, technology, science, business
- **All-In Podcast** — Chamath, Sacks, Friedberg, Calacanis on tech/markets/policy
- **Acquired** — long-form company history and strategy deep dives
- **Bg2 Pod** — Bill Gurley + Brad Gerstner on tech investing and macro
- **Dwarkesh Patel** — Dwarkesh's interview podcast on AI, science, history
- **Bloomberg Technology** — daily Bloomberg TV tech coverage
- **a16z** — Andreessen Horowitz portfolio and thesis content
- **CNBC** — daily business news and interviews
- **WSJ** — Wall Street Journal video journalism
- **The Diary of a CEO** — Steven Bartlett interviews
- **Coleman Hughes** — Conversations with Coleman, long-form interviews on culture, politics, AI, race
- **Sam Harris** — Making Sense, long-form on AI, ethics, geopolitics, neuroscience
- **The Prof G Pod** — Scott Galloway on tech, brand, business, culture (also Prof G Markets)
- **Pivot** — Kara Swisher + Scott Galloway on tech, business, politics
- **AI in Context** — AI commentary and analysis (verify channel handle on first match)
- **EO Global** — Entrepreneurs' Organization, founder and operator interviews
- **Go9x** — Morty's pick (verify channel handle on first match)
- **Paul J. Lipsky** — Morty's pick (verify channel handle on first match)
- **Casey Neistat** — Filmmaker / vlogger; commentary on tech, creator economy, NYC, business
- **Figure** — Figure AI, humanoid robotics company channel (firsthand product/demo content)
- **Peter Diamandis / Moonshots** — Peter Diamandis's channel and Moonshots podcast (same source); exponential tech, AI, longevity, future of work
- **Myicor** — Morty's pick (verify channel handle on first match)
- **Silicon Valley Girl** — Marina Mogilko, tech/startup/lifestyle commentary
- **KatGPT / CatGPT** — AI explainers and interviews (e.g., Mustafa Suleyman “Beyond the Bio” series); confirm exact handle on first match
- **Google Labs** — Google's experimental product channel (firsthand demos, model launches, Gemini features)
- **The Master Investor Podcast** — long-form investor and operator interviews (verify channel handle on first match)
- **Fareed Zakaria GPS** — CNN's Fareed Zakaria, geopolitics, macro, foreign policy
- **TED** — TED Talks main channel (also covers TEDx, TED Conferences)
- **GaryVee** — Gary Vaynerchuk, marketing, brand, creator economy, business commentary
- **WSJ Events** — Wall Street Journal conferences and event sessions (CEO Council, Tech Live, Global Food Forum, etc.)
- **Wharton School** — Wharton's official channel; faculty research, business education, exec interviews
- **Baker Institute** — Rice University's Baker Institute for Public Policy; energy, geopolitics, economics, public policy
- **Parsons** — Parsons School of Design (The New School); design, fashion, creative practice (verify on first match if Morty meant a different Parsons)
- **Gromek Institute** — Jay & Patty Baker Gromek Institute at FIT; retail, fashion business, omnichannel research
- **Forward Party** — Andrew Yang's political party channel; policy, AI, future of work, governance reform
- **Andrew Yang** — Andrew Yang's personal channel / Forward Podcast; AI policy, UBI, future of work, politics
- **The Interview** — likely NYT's The Interview podcast (David Marchese / Lulu Garcia-Navarro); long-form cultural and business interviews (verify exact handle on first match)
- **Big Think** — expert interviews on science, philosophy, business, AI, longform ideas
- **The Free Press** — Bari Weiss's outlet; Honestly podcast, longform interviews on culture, politics, tech
- **Mo Gawdat** — former Google X CBO; AI, happiness, future of work, ethics
- **AI Upload** — Morty's pick (verify channel handle on first match)
- **The Institute of Art and Ideas** — IAI / iai.tv; philosophy, science, AI, ideas debates and lectures

---

## Recently rejected (cron memory, do not re-pitch)

- (none yet)

---

## Maintenance

- Morty adds or removes channels by telling Kit. Kit edits this file directly.
- The cron reads this file on every run. No restart, no deploy needed.
- This file is committed to git so changes are auditable in history.
