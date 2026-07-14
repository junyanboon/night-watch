# The Night Watch — design contract

The published `index.html` is the source of truth for the look; this file states the rules so every morning's rebuild stays consistent. As of **2026-07-14** the Night Watch adopts the **Day Sheet editorial system** (matching https://junyanboon.github.io/day-sheet/). Do NOT revert to the old dark-indigo "pre-dawn" theme.

## Hard rules
- `<head>` MUST include `<meta name="robots" content="noindex, nofollow">`. Public-by-URL, never indexed.
- Self-contained: inline CSS/JS only, no external requests.
- PUBLIC REDACTION: never print alarm/door/entry codes, phone numbers, emails, or full addresses. First name + last initial for renters. The Notion links carry the detail.
- Read-only digest: never mark reports Reviewed, never modify queue rows, never message customers.
- Keep the self-refresh script (reloads a visible stale tab every ~10 min).

## Visual system (Day Sheet)
- **Palette:** warm paper `#f5f4f0`, ink `#191715`, mute `#716c64`, hair `#dedbd3`, brand purple `#5b2fd4`. State colors: act `#b06c00` (amber), wait `#51617e` (slate), hot `#c23a2b` (red), done `#2c7a4e` (green), each with a `-soft` tint. Full dark-mode overrides via `prefers-color-scheme`.
- **Type:** `Avenir Next Condensed`/`Arial Narrow` for the big uppercase masthead, score numerals, and section headers; `Avenir Next` sans for names/pills; `Seravek` for body text. Tabular numerals.
- **Masthead:** small-caps kicker + hairline, giant uppercase `THE NIGHT WATCH` wordmark (second word in brand purple), one-sentence honest verdict line.
- **Score band:** 3-column band, big colored tabular numerals — Runs completed / Overtime flags / Waiting on you. Amber when the review count > 0.
- **Sections** use `ACT I / ACT II / CURTAIN`-style colored number badges + condensed uppercase `<h2>` + right-aligned note. Hairline `.row`s: `name↗` link · uppercase `.ctx` context · one colored `.pill` (act/wait/hot/done) stating the next step · one `.line` summary a human reads in two seconds.

## Keep the timeline
The **`LOG · How the night unfolded`** section is required and sits directly under the score band. It is a single vertical component at every width: right-aligned mono time · a dot centred on a continuous 2px vertical rail carrying a brand→amber gradient (night at top → morning at bottom) · bold persona, a short plain clause, and a small uppercase status word coloured ok/warn/hot/info. One row per run in chronological order (evening close → dawn). Flagged runs get a warn/hot dot; a missing report gets a hot dot + `no report`. Long quiet stretches collapse into a dot-less italic gap row (e.g. "a quiet night — nothing stirred for 6 h 37 m").

## Content contract (unchanged)
- Gather the pre-dawn reports (Opener, Host, Doorman, Timekeeper, Analyst) + overnight Money Request Queue rows. A MISSING report is itself a finding — mark it clearly, never invent content.
- "Waiting on you" = the human-action items (held nudges, decisions, access, premises). Lead with the amount when there is one; say plainly when no money moved.
- Ledger = one row per persona/run with a status pill and a one-line takeaway. Doorman renters as chips (solid = today, dashed = tomorrow).
- Title `Dance Annex — The Night Watch`. Footer: sources + compiled note + "the daytime desk reports separately."

## Publish
Zapier GitHub: `get_file_contents` index.html for the SHA → `create_file` (repo `night-watch-k3v9x`, path `index.html`, message `Night Watch <date>`, sha). Then Slack self-DM to Junyan (U0AR42HAEB0).