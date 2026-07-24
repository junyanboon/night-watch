# The Night Watch — design contract

**How to build the page each morning: CLONE [`template.html`](./template.html) and fill only its `{{...}}` content slots** — keep the `<style>`, `<script>`, palette, fonts, and layout classes byte-for-byte. `template.html` carries the full skeleton plus inline instructions and reference rows; `index.html` is the current published edition (also a valid reference). Do NOT revert to the old dark-indigo "pre-dawn" theme. This doc explains the contract; the template enforces it.

## Hard rules
- `<head>` MUST include `<meta name="robots" content="noindex, nofollow">`. Public-by-URL, never indexed.
- Self-contained: inline CSS/JS only, no external requests.
- **LINKS OPEN IN A NEW TAB.** Every external link (`href` starting `http`) MUST carry `target="_blank" rel="noopener"` so it opens in a new tab, not the current page. Also include the runtime safety snippet in `## Links` below so any anchor is covered even if a per-link `target` was missed.
- PUBLIC REDACTION: never print alarm/door/entry codes, phone numbers, emails, or full addresses. First name + last initial for renters. The Notion links carry the detail.
- Read-only digest: never mark reports Reviewed, never modify queue rows, never message customers.
- Keep the self-refresh script (reloads a visible stale tab every ~10 min).
- ACT I check-off / tick feature **removed 2026-07-23, owner request — do not re-add**; completed items are closed in Notion, and an edition may use static struck-through rows for owner cross-offs.

## Links
Every external link opens in a new tab. Put `target="_blank" rel="noopener"` on each anchor, AND keep this runtime safety net in the page (it upgrades any external anchor at load, and leaves in-page `#anchor` links alone):
```html
<script>
  /* Every external link opens in a new tab. */
  document.querySelectorAll('a[href^="http"]').forEach(function (a) {
    a.target = "_blank"; a.rel = "noopener";
  });
</script>
```

## Visual system (Day Sheet) — all baked into template.html
- **Palette:** warm paper `#f5f4f0`, ink `#191715`, mute `#716c64`, hair `#dedbd3`, brand purple `#5b2fd4`. State colors: act `#b06c00` (amber), wait `#51617e` (slate), hot `#c23a2b` (red), done `#2c7a4e` (green), each with a `-soft` tint. Full dark-mode overrides via `prefers-color-scheme`.
- **Type:** `Avenir Next Condensed`/`Arial Narrow` for the big uppercase masthead, score numerals, and section headers; `Avenir Next` sans for names/pills; `Seravek` for body text. Tabular numerals.
- **Masthead:** small-caps kicker + hairline, giant uppercase `THE NIGHT WATCH` wordmark (second word in brand purple), one-sentence honest verdict line.
- **Score band:** big colored tabular numerals — Runs completed / Warnings / Waiting on you (always exactly 3 cells; amber `act-n` when a count needs attention). **No "Fix these" cell** — Fix items live on The Fixer Report (2026-07-21).
- **Sections (restructured 2026-07-23, owner directive)** use `ACT I / ACT II` colored number badges + condensed uppercase `<h2>` + right-aligned note. TWO sections only: **ACT I `How the night unfolded`** (the merged timeline+ledger) and **ACT II `Waiting on you`** (hairline `.row`s: `name↗` link · uppercase `.ctx` context · one `.pill` · one `.line` summary).
- **State-color vocabulary — THREE STATES ONLY (owner directive 2026-07-23)** for dots AND pills alike: `ok`=green "All good" (clean/pass) · `warn`=amber warning (needs attention/flags/held) · `hot`=red urgent (missing report/time pressure/emergency). No other pill classes; the old act/wait/done/info pills are retired.

## Keep the timeline — ACT I is the merged timeline+ledger (2026-07-23)
The **`ACT I · How the night unfolded`** section is required and sits directly under the score band. It MERGES the former LOG timeline and ACT II ledger into one component: right-aligned mono time · a dot centred on a continuous 2px vertical rail carrying a brand→amber gradient (night at top → morning at bottom) · the persona **linked to its Notion report** (`a.who`) · uppercase `.ctx` context · a right-aligned **3-state pill** (`ok` "All good" / `warn` / `hot`) · and a **bullet list (`ul.bl`)** of what that agent concretely did and found — counts, amounts, flags, filings. The reader must be able to understand each agent's night from the bullets alone. One `.beat` per run in chronological order (evening close → dawn). A missing report gets a hot dot + pill `no report`. Long quiet stretches collapse into a dot-less italic `.quiet` gap row (e.g. "a quiet night — nothing stirred for 6 h 37 m"). The Doorman beat may carry renter chips (solid = today, dashed = tomorrow); codes never on the page. There is NO separate ledger section anymore.

## Content contract
- Gather the pre-dawn reports (Custodian **`Fixer Report — <date>`**, Opener, Host, Doorman, Timekeeper, Analyst) + overnight Money Request Queue rows. The Fixer Report is the Custodian's 02:35 night pass — it carries the full-day QA + day-in-review and is the source of the "Fix these — you" (`For = Junyan`) items. A MISSING report is itself a finding — mark it clearly (persona, "no report as of <time>"), never invent content.
- **Waiting on you** (ACT II) = the **Ops-lead** staff-gate items — open Actions `For = Ops Lead` (held nudges, decisions, access, premises). Lead with the amount when there is one; say plainly when no money moved. Pills here use the same three states (`warn` for a normal next step, `hot` for genuine urgency).
- **Fix these — you (MOVED, 2026-07-21):** agent mistakes only **Junyan** can correct (open Actions `For = Junyan`, `Type = Review`, `Raised by = The Custodian`) belong to **The Fixer Report** (https://junyanboon.github.io/fixer-report/) — the Night Watch never renders a `#fixme` section or score cell. The audiences differ: the Night Watch briefs the Ops lead (staff gates only); the Fixer Report briefs Junyan (agent corrections). On the Night Watch, when ≥1 such row is open, render only the one-line `.fixnote` pointer after ACT II (`FIX · N agent mistakes for Junyan → The Fixer Report ↗`); omit it entirely at zero.
- **The ledger (RETIRED 2026-07-23, owner directive):** the separate per-run ledger section is gone — its content (per-agent outcomes, counts, the Doorman chips) now lives in ACT I's bullets.
- Title `Dance Annex — The Night Watch`. Footer: sources + "the daytime desk reports separately."

## Publish
GitHub MCP connector (no Zapier): read `index.html` for the SHA → create/update file contents (repo `night-watch`, path `index.html`, message `Night Watch <date>`, sha). `git` push with a Contents:write token is the equivalent CLI path. Then Slack self-DM to Junyan (U0AR42HAEB0). See `HANDOFF.md` for the full operator guide.
