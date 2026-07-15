# Night Watch — session handoff

How to run the **Dance Annex Night Watch publisher** from a fresh session. This doc is the operator's guide; `DESIGN.md` is the design contract and `template.html` is the page to clone.

## What the job is
Once each morning (~08:40 ET, unattended, in the cloud) compile the pre-dawn autonomous run reports into ONE self-contained HTML dashboard and publish it to a public GitHub Pages site. You are a **READ-ONLY digest**: never mark reports Reviewed, never modify queue rows, never message customers. No customer-facing sends.

## Where everything lives
- **GitHub repo:** `junyanboon/night-watch-k3v9x` (login `junyanboon`).
- **Public URL:** https://junyanboon.github.io/night-watch-k3v9x/ (served automatically from `index.html`; same URL every day).
- **`index.html`** — the published page; overwritten each morning. Optionally copy the outgoing edition into `archive/<date>.html`.
- **`template.html`** — CLONE this and fill only its `{{...}}` slots; keep style/script/classes byte-for-byte.
- **`DESIGN.md`** — the full design + content contract.
- **Notion Workflow Reports DB** — data source `collection://469a877b-83fa-4387-ac97-94aa656481dd` (under "Source Pages (Dance Annex)").
- **Money Request Queue / Actions to Perform DB** — `https://app.notion.com/p/760a2e655c694b6fbd4a2b185ece0973` (data source `collection://20df225d-382f-4bb8-9c15-c31571c9f4e0`).
- **Slack DM target:** Junyan, user `U0AR42HAEB0`.

## Tools
- **Notion (read):** `notion-fetch`, `notion-query-data-sources`. Read-only.
- **Publish to GitHub:** see the publish step. **Working write path today = the Zapier GitHub action** (`selected_api: GitHubCLIAPI`): `user`, `get_file_contents`, `create_file`; call `list_enabled_zapier_actions` first each session. `git` is installed and can READ the repo through `$HTTPS_PROXY`, but the environment tokens are **read-only**, so `git push` is denied — prefer git ONLY once a write-scoped token is added (see below). The claude.ai GitHub connector is NOT exposed as tools to agent/Claude Code sessions.
- **Slack:** `slack_send_message` (self-DM only).

## Daily procedure
1. **Gather (Notion, today = America/Toronto).** Fetch in full each report created since ~22:00 ET yesterday: `Morning Shift — <today>` (Opener), `The Host — <today>`, `The Doorman — <today>` (alarm + access pre-flight), `Overtime — <yesterday>` (Timekeeper), `Issues Report — <today>` and `— <tomorrow>` (Analyst). Also scan the Money Request Queue for overnight alert/Action rows and any held/Pending-Review rows named in the Opener's "For You". **A MISSING report is itself a finding** — mark it clearly (persona, "no report as of <time>"); never invent content. Re-fetch on stale cache.
2. **Build the page.** CLONE `template.html`; fill only the `{{...}}` slots (masthead time + verdict, three score numbers, the rows in the three sections). Follow `DESIGN.md`. Non-negotiables:
   - `<head>` includes `<meta name="robots" content="noindex, nofollow">`; self-contained (inline CSS/JS, no external requests).
   - **REDACTION:** first name + last initial for renters; NEVER an alarm/door/entry code, phone, email, or full address. The Notion links carry the detail.
   - **Keep the timeline** (`LOG · How the night unfolded`) directly under the score band.
   - **LINKS OPEN IN A NEW TAB.** Every external link must have `target="_blank" rel="noopener"`. Keep the runtime safety snippet from `DESIGN.md` as a backstop.
3. **Publish to GitHub.**
   - **Working path — Zapier.** (a) `user` → confirm login `junyanboon`. (b) `get_file_contents` repo `night-watch-k3v9x`, path `index.html`, default branch → capture the file **SHA** (top-level `sha` field). (c) `create_file` → same repo/path/branch, `content` = the full HTML, `commit_message` = `Night Watch <today>`, `sha` = the captured SHA (omit on first-ever publish). Pages redeploys automatically.
   - **Preferred once a write-scoped token exists (no inline HTML, easy archiving).** The env has `git` + proxy `$HTTPS_PROXY`; if `$GITHUB_TOKEN` (or another named secret) has **Contents: write**:
     ```bash
     git -c http.proxy="$HTTPS_PROXY" clone "https://x-access-token:${GITHUB_TOKEN}@github.com/junyanboon/night-watch-k3v9x" nw
     cd nw && git config http.proxy "$HTTPS_PROXY"
     git config user.name junyanboon && git config user.email junyan.boon@gmail.com
     # write index.html (and optionally cp the previous edition to archive/<date>.html)
     git add -A && git commit -m "Night Watch <today>"
     git -c http.proxy="$HTTPS_PROXY" push
     ```
     NOTE: as of now the environment tokens are **read-only** and this push is rejected ("Password authentication is not supported" = insufficient scope). Use the Zapier path until a Contents:write token is provisioned.
4. **Confirm.** One short Slack DM to `U0AR42HAEB0`: `Night Watch published for <date> — <verdict one-liner>, <N> items need you. https://junyanboon.github.io/night-watch-k3v9x/`

## Gotchas
- **Zapier `create_file` replaces the whole file** — no patch/append. Send the complete HTML in `content`; escape newlines as `\n` and quotes as `\"`. Passing the SHA makes a concurrent edit fail loudly instead of clobbering. (git avoids all of this once a write token exists.)
- **`get_file_contents`** returns base64 `content` + a `decoded_content` preview; the SHA you need is the top-level `sha`.
- **git read works, git push does not** (read-only env token); the **GitHub connector is not callable** from agent sessions — only Notion, Slack, and Zapier tools are.
- If no GitHub write path is available or the repo is missing: don't retry endlessly — Slack-DM Junyan exactly what's missing and stop.
- **The scheduled trigger prompt** (what launches this run each morning) lives in the Claude Code **web** automation UI — it is NOT a file and NOT editable from inside a run. It should instruct: *"Read HANDOFF.md + DESIGN.md + template.html from the repo and follow them; clone template.html and fill its `{{...}}` slots; do not use the old indigo/serif theme."* If a run ever produces the wrong look, that prompt is the thing to fix.

## Constraints
Notion is read-only. No customer-facing sends. Stay within Notion read tools, Write/Read/Edit + git (read), the Zapier GitHub actions, and the single Slack self-DM.
