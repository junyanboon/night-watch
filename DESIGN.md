# The Night Watch — exception-console design contract

The Night Watch is the **post-Concierge exception display**, not a worksheet and not an operations queue. Each morning the Concierge first processes the overnight findings through its JOB 34 handoff. The publisher then clones [`template.html`](./template.html) and shows only what remains genuinely human-only.

`template.html` is the visual source of truth. Fill its `{{...}}` content slots; preserve the style system, layout classes, redaction rules, and scripts.

[`ACCEPTANCE.md`](./ACCEPTANCE.md) is the regression fixture for the July 26 cases. Any future change that makes those cases reappear as worksheet decisions violates this contract.

## Product contract

The Ops Lead should see one of two outcomes in ACT I:

1. **All clear** — the Concierge verified and completed every overnight finding; or
2. **Needs you** — a short list containing only actions that require human authority or hands.

Alongside that verdict the page always shows **what is actually open** — the truth band and, when non-empty, ACT II's ordered queue. ACT I answers "what did the handoff leave me"; the truth band and queue answer "what is really outstanding". Both are needed: the first is only trustworthy while the Concierge keeps up, and the second is what makes a bad morning legible instead of quiet.

The page never asks the Ops Lead to verify reports, classify work, update statuses, copy a handoff into chat, or confirm that an already-observable result happened. Those are Concierge responsibilities.

## Required morning handshake

Before rendering, fetch the current `The Concierge — Rolling Daily YYYY-MM-DD` report and find a fresh line matching:

`NW-HANDOFF-V1 checked=<N> completed=<N> parked=<N> needs_ops=<N> system_exceptions=<N>`

- The marker to use is the **last** one on the report, not the first. Passes file all day and each supersedes the one before it.
- A fresh marker proves the Concierge consumed the overnight reports.
- The Concierge lists every human-only candidate directly below it as `RESIDUAL class=<money|physical|access-config|policy|message-review> action=<Notion URL>`. That classification is canonical; the publisher verifies current state without rerouting raw findings.
- If the marker is missing, stale, malformed, internally inconsistent, names an unknown class, or reports one or more system exceptions, render one hot system exception: **Concierge handoff incomplete**. Do not promote the raw overnight findings into Ops Lead tasks.
- `Checked overnight` = marker `checked`.
- `Handled automatically` = marker `completed + parked`.
- `Needs you` = named residual rows that remain open after the publisher's fresh re-read. It must equal marker `needs_ops`; a mismatch is a system exception.

## The truth band — direct reads, not marker-derived

The handshake above describes what the Concierge *claims* it handed over. The truth band describes what is *actually open*, queried straight from the ticket and Actions data sources on every publish. It renders always — including when the handshake fails, when `Needs you` is zero, and when the all-clear card shows.

It carries five numbers: open Actions `For = Ops Lead`, open Actions `For = Junyan`, open Customer Care tickets, open Sales tickets, and the age in days of the oldest open item.

When the marker's `needs_ops` and the live open surface disagree materially, render the `.gap` line naming both numbers and, when the rolling report says so, the reason (skipped jobs, partial pass, budget exhaustion).

This band is a **gauge, never a task list.** It does not promote anything to Ops Lead work and it does not reclassify findings — it exists so the console can no longer report a calm number while a backlog sits unworked. *(2026-08-13: the console read `1 needs you` on a morning with 139 open Action rows and 48 open tickets, the oldest 19 days. The page was obeying its contract exactly; the contract assumed a Concierge that keeps up, and that assumption had stopped holding.)*

## ACT II — the queue

The open ticket surface, grouped by `Position`, oldest group first. It answers "what order do I work in", replacing a manual hunt through two boards.

- Order: `Gate: Staff` first (human-only by the gates.md self-serve test), then `Review`, then everything else by age.
- Each group: count, position name, age of the oldest ticket, one plain-language line on what that position means, and at most five named tickets plus a `+N more`.
- Omit the whole section when nothing is open.
- Rows are **pointers to work, not authority to act.** Every ticket is still walked with `process-studio-tickets`, which owns all ticket mechanics. The console does not advance a Position, clear a gate, or mark anything.
- The queue is independent of the handshake: it renders even when the marker is missing, because a broken handoff is exactly when knowing the real backlog matters most.

## What qualifies for “Needs you”

A row may appear only when all of these are true:

1. It is a live, open ✅ Actions to Perform row assigned to `For = Ops Lead` or `For = Owner`.
2. The Concierge’s fresh handoff re-read the source and left the row open.
3. The requested outcome is still unmet.
4. JOB 34 named it with one allowed `RESIDUAL class`: `money`, `physical`, `access-config`, `policy`, or `message-review`.
5. **The publisher read that row itself during this run and found it open.** The marker is a nomination, never a verdict — a residual named at 08:30 and closed at 10:35 is closed. Being unable to read the row is a system exception, not permission to render it from the marker's text. *(2026-08-13: five residuals were published as needing the Ops Lead; all five had been closed by a later Concierge pass before the page went out.)*

Never render:

- a retired run's absence as a missing report or system exception (HANDOFF.md carries the Retired runs table — check it before writing "never ran");
- machine-readable gates that already read true;
- ticket routing, correspondence capture, documentation, deduplication, or closure work;
- a future artist-facing `Gate: Time` outbound before its due date (live verification and fact-driven advancement still run every pass);
- ignored/policy-excluded report noise;
- a duplicate, cancelled, processed, or superseded Action row;
- `For = Junyan` defects—the Fixer Report owns those.

## Page structure

- **Masthead:** same warm-paper editorial visual; one honest outcome sentence.
- **Score band:** `Checked overnight` / `Handled automatically` / `Needs you` — exactly three cells, marker-derived.
- **Truth band:** five direct-read counts plus an optional gap line. Always rendered.
- **ACT I — Needs you:** first and prominent. At zero, show one green all-clear card. Otherwise show only the residual human actions, each with a direct Notion link, evidence, and one concrete next step.
- **ACT II — The queue:** open tickets grouped by `Position`, oldest first. Omitted at zero.
- **ACT III — Automatic audit:** a compact collapsed audit of what the Concierge completed or parked. It exists for trust and debugging, not as a checklist.
- **System exception:** a red row above human actions when the morning handshake or a required live source failed.
- **Fixer pointer:** when open `For = Junyan` verifier defects exist, show only the pointer to The Fixer Report.

There are no worksheet controls, status dropdowns, notes fields, selections, checkboxes, or chat handoff button.

## Visual system

Keep the established Day Sheet visual language:

- warm paper `#f5f4f0`, ink `#191715`, muted `#716c64`, hairline `#dedbd3`, brand purple `#5b2fd4`;
- amber for a normal human action, red for an urgent/system exception, green for verified clear;
- `Avenir Next Condensed`/`Arial Narrow` masthead and numerals; `Avenir Next`/`Seravek` body;
- first name + last initial for renters;
- dark-mode variables and reduced-motion behavior;
- three pill states only: `ok`, `warn`, `hot`.

## Hard rules

- `<meta name="robots" content="noindex,nofollow">`.
- Self-contained HTML: inline CSS/JS only, except the existing local favicon.
- External links always use `target="_blank" rel="noopener"`; retain the runtime safety script.
- Never publish an alarm/door/entry code, phone, email, or full address.
- The page is read-only. It never mutates Notion, sends messages, settles money, changes access/configuration, or triggers a workflow.
- Missing data is a system exception, never an “all clear.”
- The publisher sends Junyan one short summary only after publication.

## Publish

Use the GitHub contents write path or a normal git commit/push to replace `index.html`. The scheduled publisher remains read-only; the production work happens in the Concierge before this page is built.
