# The Night Watch — exception-console design contract

The Night Watch is the **post-Concierge exception display**, not a worksheet and not an operations queue. Each morning the Concierge first processes the overnight findings through its JOB 34 handoff. The publisher then clones [`template.html`](./template.html) and shows only what remains genuinely human-only.

`template.html` is the visual source of truth. Fill its `{{...}}` content slots; preserve the style system, layout classes, redaction rules, and scripts.

[`ACCEPTANCE.md`](./ACCEPTANCE.md) is the regression fixture for the July 26 cases. Any future change that makes those cases reappear as worksheet decisions violates this contract.

## Product contract

The Ops Lead should see one of two outcomes:

1. **All clear** — the Concierge verified and completed every overnight finding; or
2. **Needs you** — a short list containing only actions that require human authority or hands.

The page never asks the Ops Lead to verify reports, classify work, update statuses, copy a handoff into chat, or confirm that an already-observable result happened. Those are Concierge responsibilities.

## Required morning handshake

Before rendering, fetch the current `The Concierge — Rolling Daily YYYY-MM-DD` report and find a fresh line matching:

`NW-HANDOFF-V1 checked=<N> completed=<N> parked=<N> needs_ops=<N> system_exceptions=<N>`

- A fresh marker proves the Concierge consumed the overnight reports.
- The Concierge lists every human-only candidate directly below it as `RESIDUAL class=<money|physical|access-config|policy|message-review> action=<Notion URL>`. That classification is canonical; the publisher verifies current state without rerouting raw findings.
- If the marker is missing, stale, malformed, internally inconsistent, names an unknown class, or reports one or more system exceptions, render one hot system exception: **Concierge handoff incomplete**. Do not promote the raw overnight findings into Ops Lead tasks.
- `Checked overnight` = marker `checked`.
- `Handled automatically` = marker `completed + parked`.
- `Needs you` = named residual rows that remain open after the publisher's fresh re-read. It must equal marker `needs_ops`; a mismatch is a system exception.

## What qualifies for “Needs you”

A row may appear only when all of these are true:

1. It is a live, open ✅ Actions to Perform row assigned to `For = Ops Lead` or `For = Owner`.
2. The Concierge’s fresh handoff re-read the source and left the row open.
3. The requested outcome is still unmet.
4. JOB 34 named it with one allowed `RESIDUAL class`: `money`, `physical`, `access-config`, `policy`, or `message-review`.

Never render:

- machine-readable gates that already read true;
- ticket routing, correspondence capture, documentation, deduplication, or closure work;
- a future artist-facing `Gate: Time` outbound before its due date (live verification and fact-driven advancement still run every pass);
- ignored/policy-excluded report noise;
- a duplicate, cancelled, processed, or superseded Action row;
- `For = Junyan` defects—the Fixer Report owns those.

## Page structure

- **Masthead:** same warm-paper editorial visual; one honest outcome sentence.
- **Score band:** `Checked overnight` / `Handled automatically` / `Needs you`.
- **ACT I — Needs you:** first and prominent. At zero, show one green all-clear card. Otherwise show only the residual human actions, each with a direct Notion link, evidence, and one concrete next step.
- **ACT II — Automatic audit:** a compact collapsed audit of what the Concierge completed or parked. It exists for trust and debugging, not as a checklist.
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
