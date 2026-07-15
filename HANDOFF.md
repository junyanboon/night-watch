# Night Watch — session handoff

How to run the **Dance Annex Night Watch publisher** from a fresh session. This doc is the operator's guide; `DESIGN.md` is the design contract and `template.html` is the page to clone.

## What the job is
Once each morning (~08:40 ET, unattended, in the cloud) compile the pre-dawn autonomous run reports into ONE self-contained HTML dashboard and publish it to a public GitHub Pages site. You are a **READ-ONLY digest**: never mark reports Reviewed, never modify queue rows, never message customers. No customer-facing sends.

## Where everything lives
- **GitHub repo:** `junyanboon/night-watch-k3v9x` (reached via the Zapier GitHub connection, login `junyanboon`).
- **Public URL:** https://junyanboon.github.io/night-watch-k3v9x/ (served automatically from `index.html`; same URL every day).
- **`index.html`** — the published page; overwritten each morning.
- **`template.html`** — CLONE this and fill only its `{{...}}` slots; keep style/script/classes byte-for-byte.
- **`DESIGN.md`** — the full design + content contract.
- **Notion Workflow Reports DB** — data source `collection://469a877b-83fa-4387-ac97-94aa656481dd` (under "Source Pages (Dance Annex)").
- **Money Request Queue / Actions to Perform DB** — `https://app.notion.com/p/760a2e655c694b6fbd4a2b185ece0973` (data source `collection://20df225d-382f-4bb8-9c15-c31571c9f4e0`).
- **Slack DM target:** Junyan, user `U0AR42HAEB0`.

## Tools you need
- **Notion (read):** `notion-fetch`, `notion-query-data-sources`. Read-only.
- **Zapier GitHub** (`selected_api: GitHubCLIAPI`): `user` (find login), `get_file_contents` (SHA + content), `create_file` (create/update). Call `list_enabled_zapier_actions` first each session.
- **Slack:** `slack_send_message` (self-DM only).

## Daily procedure
1. **Gather (Notion, today = America/Toronto).** Fetch in full each report created since ~22:00 ET yesterday: `Morning Shift — <today>` (Opener), `The Host — <today>`, `The Doorman — <today>` (alarm + access pre-flight), `Overtime — <yesterday>` (Timekeeper), `Issues Report — <today>` and `— <tomorrow>` (Analyst). Also scan the Money Request Queue for overnight alert/Action rows and any held/Pending-Review rows named in the Opener's "For You". **A MISSING report is itself a finding** — mark it clearly (persona, "no report as of <time>"); never invent content. Re-fetch on stale cache.
2. **Build the page.** CLONE `template.html`; fill only the `{{...}}` slots (masthead time + verdict, three score numbers, the rows in the three sections). Follow `DESIGN.md`. Non-negotiables:
   - `<head>` includes `<meta name="robots" content="noindex, nofollow">`; self-contained (inline CSS/JS, no external requests).
   - **REDACTION:** first name + last initial for renters; NEVER an alarm/door/entry code, phone, email, or full address. The Notion links carry the detail.
   - **Keep the timeline** (`LOG · How the night unfolded`) directly under the score band.
   - **LINKS OPEN IN A NEW TAB.** Every external link must have `target="_blank" rel="noopener"`. As a safety net, keep this runtime snippet in the page so any anchor is covered even if `target` was missed:
     ```html
     <script>
       /* Every external link opens in a new tab. */
       document.querySelectorAll('a[href^="http"]').forEach(function (a) {
         a.target = "_blank"; a.rel = "noopener";
       });
     </script>
     ```
3. **Publish (Zapier GitHub).** (a) `user` → confirm login `junyanboon`. (b) `get_file_contents` repo `night-watch-k3v9x`, path `index.html`, default branch → capture the file **SHA**. (c) `create_file` → same repo/path/branch, `content` = the full HTML, `commit_message` = `Night Watch <today>`, `sha` = the captured SHA (omit on first-ever publish). Pages redeploys automatically.
4. **Confirm.** One short Slack DM to `U0AR42HAEB0`: `Night Watch published for <date> — <verdict one-liner>, <N> items need you. https://junyanboon.github.io/night-watch-k3v9x/`

## Gotchas
- **`create_file` replaces the whole file** — there is no patch/append. Send the complete HTML in `content`; escape newlines as `\n` and quotes as `\"` in the tool params. Passing the SHA makes a concurrent edit fail loudly instead of clobbering.
- **`get_file_contents`** returns base64 `content` + a `decoded_content` preview; the **SHA** you need for updates is the top-level `sha` field.
- If GitHub is not connected in Zapier or the repo is missing: don't retry endlessly — Slack-DM Junyan exactly what's missing and stop.
- **The scheduled trigger prompt** (what launches this run each morning) lives in the Claude Code **web** automation UI — it is NOT a file and NOT editable from inside a run. It should instruct: *"Build the page by cloning `template.html` from the repo and filling its `{{...}}` slots; follow `DESIGN.md`; do not use the old indigo/serif theme."* If a run ever produces the wrong look, that prompt is the thing to fix.

## Constraints
Notion is read-only. No customer-facing sends. Stay within Notion read tools, Write/Read/Edit, the Zapier GitHub actions, and the single Slack self-DM.
