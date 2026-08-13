# Night Watch — session handoff

How to run the Dance Annex Night Watch publisher. `DESIGN.md` is the product contract and `template.html` is the page to clone.

## What the job is

Once each morning at approximately 08:40 Toronto, publish a self-contained **exception console**. The Concierge’s first morning pass owns all verification, ticket work, safe fixes, and reconciliation. Night Watch runs afterward and displays only the remaining human-only gates.

The publisher is read-only: never update a ticket or Action row, never send a customer message, never settle money, and never change configuration. It also never converts unprocessed Concierge work into an Ops Lead task.

## Sources

- GitHub repo: `junyanboon/night-watch`
- Public URL: https://junyanboon.github.io/night-watch/
- `template.html`: visual and structural source of truth
- `DESIGN.md`: exception qualification and content contract
- `ACCEPTANCE.md`: July 26 regression fixture and expected ownership
- Workflow Reports data source. **Retired runs are not findings:** The Opener / `Morning Shift` report was retired 2026-07-23 (ticket 007, dissolved-never-restore). Its absence is expected — never render it as a missing report, a ledger row, or a system exception.
- Actions to Perform data source
- Message Queue: read only when a residual action is a human-reviewed outbound
- Fixer Report: https://junyanboon.github.io/fixer-report/
- Configured Junyan self-DM target

## Daily procedure

### 1. Verify the Concierge handoff

Fetch today’s `The Concierge — Rolling Daily YYYY-MM-DD` report in full. Require a fresh exact marker:

`NW-HANDOFF-V1 checked=<N> completed=<N> parked=<N> needs_ops=<N> system_exceptions=<N>`

Re-fetch if the Notion response is stale.

- Fresh marker, zero system exceptions: continue.
- Missing, stale, malformed, internally inconsistent marker, unknown residual class, or any system exception: render one hot **Concierge handoff incomplete** system row and carry its evidence. Do not list every raw overnight report item as work for the Ops Lead.

### 2. Re-read the residual human queue

Read only the Action URLs named on `RESIDUAL` lines beneath the marker. For every candidate, fetch the complete row and linked ticket. Include it only when its present state is still open, the requested outcome remains unmet, and its class is one of `money`, `physical`, `access-config`, `policy`, or `message-review`.

JOB 34's classification is canonical. The publisher does not search the whole Ops Lead queue or independently reroute work; it verifies the named residuals against fresh source state. A pending row alone is insufficient: exclude machine-readable work already completed, Concierge-owned admin/ticket work, future artist-facing time gates, duplicates, obsolete rows, and policy-excluded noise. Live verification and fact-driven advancement are never deferred by `Revisit After`.

Open `For = Junyan`, `Type = Review`, `Raised by = The Custodian` rows contribute only to the Fixer Report pointer count.

### 2b. Read the live open surface directly

Independent of the marker — run these every publish, and run them even when the handshake failed:

- Customer Care tickets `collection://047caea0-3da0-4434-a924-319efa8237cb` — group by `Position`, exclude `Done`.
- Sales tickets `collection://b4bd4ed7-0ae8-44bb-aed0-adf78b7848b0` — group by `Position`, exclude `Won` and `Lost`.
- Actions to Perform `collection://20df225d-382f-4bb8-9c15-c31571c9f4e0` — open rows (`Status` not `Processed`/`Cancelled`), split by `For`.

Take the oldest `Created time` across the open set for the age figure. These feed the truth band and ACT II. They are counts and pointers only — never a basis for the publisher to act, reclassify, or advance anything.

Compare `needs_ops` against the live open surface. On a material disagreement, write the `.gap` line naming both numbers, plus the reason when the rolling report gives one (skipped jobs, partial pass, budget exhaustion).

### 3. Build the page

Clone `template.html` and fill the content slots:

- masthead date/time and honest verdict;
- score counts as `checked`, `completed + parked`, and the freshly verified residual count;
- truth band: the five direct-read counts, plus the gap line when they disagree with the marker;
- ACT I human-only rows, or the all-clear card at zero;
- ACT II queue groups, ordered `Gate: Staff` → `Review` → rest by age, max five named tickets per group; omit the section at zero;
- ACT III compact automatic audit from JOB 34;
- optional system exception and Fixer pointer.

Keep the established design. Never add worksheet controls or a chat handoff.

### 4. Validate

Before publishing, check:

- exactly three score cells;
- `Needs you` count equals the rendered human-action rows;
- a zero count renders the all-clear card;
- missing handoff never renders all clear;
- the truth band rendered, with all five numbers filled, even on a failed handshake;
- ACT II queue-group counts sum to the truth band's ticket totals, or the section is absent because both are zero;
- every displayed action links to its live Notion row;
- no codes, phone numbers, emails, or full addresses;
- renter names are first name + last initial;
- all external links open in a new tab;
- HTML contains no unresolved `{{...}}` placeholders.

### 5. Publish and confirm

Read the current `index.html` SHA, replace the full file on the default branch, and use commit message `Night Watch <YYYY-MM-DD> — exception console`. GitHub Pages redeploys automatically.

Then send one Slack self-DM:

`Night Watch published for <date> — <all clear | N items need you | Concierge handoff incomplete>; <N> open across the queue. https://junyanboon.github.io/night-watch/`

## Trigger boundary

The scheduled publisher trigger lives outside this repo. Its prompt should say:

> Read HANDOFF.md, DESIGN.md, and template.html from `junyanboon/night-watch`. Verify the fresh Concierge JOB 34 `NW-HANDOFF-V1` marker first. Publish only its freshly verified `RESIDUAL` Actions; raw overnight findings are Concierge work, not Ops Lead work.

Changing, enabling, or disabling the trigger remains a human-controlled configuration action.
