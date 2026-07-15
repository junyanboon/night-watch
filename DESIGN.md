# The Night Watch — design contract

**How to build the page each morning: CLONE [`template.html`](./template.html) and fill only its `{{...}}` content slots** — keep the `<style>`, `<script>`, palette, fonts, and layout classes byte-for-byte. `template.html` carries the full skeleton plus inline instructions and reference rows; `index.html` is the current published edition (also a valid reference). Do NOT revert to the old dark-indigo "pre-dawn" theme. This doc explains the contract; the template enforces it.

## Hard rules
- `<head>` MUST include `<meta name="robots" content="noindex, nofollow">`. Public-by-URL, never indexed.
- Self-contained: inline CSS/JS only, no external requests.
- PUBLIC REDACTION: never print alarm/door/entry codes, phone numbers, emails, or full addresses. First name + last initial for renters. The Notion links carry the detail.
- Read-only digest: never mark reports Reviewed, never modify queue rows, never message customers.
- Keep the self-refresh script (reloads a visible stale tab every ~10 min).

## Visual system (Day Sheet) — all baked into template.html
- **Palette:** warm paper `#f5f4f0`, ink `#191715`, mute `#716c64`, hair `#dedbd3`, brand purple `#5b2fd4`. State colors: act `#b06c00` (amber), wait `#51617e` (slate), hot `#c23a2b` (red), done `#2c7a4e` (green), each with a `-soft` tint. Full dark-mode overrides via `prefers-color-scheme`.
- **Type:** `Avenir Next Condensed`/`Arial Narrow` for the big uppercase masthead, score numerals, and section headers; `Avenir Next` sans for names/pills; `Seravek` for body text. Tabular numerals.
- **Masthead:** small-caps kicker + hairline, giant uppercase `THE NIGHT WATCH` wordmark (second word in brand purple), one-sentence honest verdict line.
- **Score band:** 3-column band, big colored tabular numerals — Runs completed / Overtime flags / Waiting on you. Amber (`act-n`) when the review count > 0.
- **Sections** use `LOG / ACT I / ACT II` colored number badges + condensed uppercase `<h2>` + right-aligned note. Hairline `.row`s: `name↗` link · uppercase `.ctx` context · one colored `.pill` (act/wait/hot/done) stating the next step · one `.line` summary a human reads in two seconds.
- **State-color vocabulary** for dots, status words, and pills: `ok`=green (clean/pass), `warn`=amber (needs attention/late/held), `hot`=red (urgent/missing report), `info`=slate (informational/in progress).

## Keep the timeline
The **`LOG · How the night unfolded`** section is required and sits directly under the score band. It is a single vertical component at every width: right-aligned mono time · a dot centred on a continuous 2px vertical rail carrying a brand→amber gradient (night at top → morning at bottom) · bold persona, a short plain clause, and a small uppercase status word. One `.beat` per run in chronological order (evening close → dawn). Flagged runs get a warn dot; a missing report gets a hot dot + `no report`. Long quiet stretches collapse into a dot-less italic `.quiet` gap row (e.g. "a quiet night — nothing stirred for 6 h 37 m").

## Content contract
- Gather the pre-dawn reports (Opener, Host, Doorman, Timekeeper, Analyst) + overnight Money Request Queue rows. A MISSING report is itself a finding — mark it clearly (persona, "no report as of <time>"), never invent content.
- **Waiting on you** (ACT I) = the human-action items (held nudges, decisions, access, premises). Lead with the amount when there is one; say plainly when no money moved.
- **The ledger** (ACT II) = one row per persona/run with a status pill and a one-line takeaway. The Doorman row uses `<span class="plain">` when there's no report to link, and renders renters as chips (solid = today, dashed = tomorrow).
- Title `Dance Annex — The Night Watch`. Footer: sources + "the daytime desk reports separately."

## Publish
Zapier GitHub: `get_file_contents` index.html for the SHA → `create_file` (repo `night-watch-k3v9x`, path `index.html`, message `Night Watch <date>`, sha). Then Slack self-DM to Junyan (U0AR42HAEB0).
