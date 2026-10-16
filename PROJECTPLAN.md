# Plan: Students & Guardians tools on www.andrew-mceachin.com

Goal: serve the multiplication worksheet and the grade-inflation tool under www.andrew-mceachin.com, each still deployed from its own repo, and add a "Students & Guardians" tab to the academic site that links to them.

## Approach

Rename the `academic-site` repo to `amceachin-code.github.io`. That makes it the GitHub user site. A user site's custom domain is inherited by every project site, so each tool repo appears at `www.andrew-mceachin.com/<repo>/` with no DNS changes. Old `amceachin-code.github.io/<repo>/` links redirect.

Order matters: fix the chat allowlist before the rename, so the grade-inflation chat never breaks.

## Steps

1. **grade-inflation: chat allowlist** (`api/chat.ts`)
   - Add `https://www.andrew-mceachin.com` to `ALLOWED_ORIGINS`. Keep `https://amceachin-code.github.io` during the switch.
   - Update the CORS note in `CLAUDE.md`.
   - Commit and push to `main`. Vercel redeploys. Confirm with a preflight request from the new origin.
2. **grade-inflation: link previews** (`index.html`)
   - Point `og:url` and `og:image` at `https://www.andrew-mceachin.com/grade-inflation/`.
   - Update the live link in `README.md`.
3. **multiplication-worksheet: link previews** (`index.html`, `README.md`, `TODO.md`)
   - Same URL change. Update the repo's Website field.
4. **academic-site: new tab**
   - New hand-made page `site/content/tools/_index.md` (no `.generated` marker, so `sync_hugo.py` leaves it alone). A short intro, then one section per tool: what it does, who it is for, a link to the tool, and a link to its GitHub repo.
   - Add "Students & Guardians" to `site/config/_default/menus.yaml` at weight 40 (between Commentary & Media and Code).
   - Build locally with Hugo and check the page and menu in the browser.
   - Commit only these two files. Your existing uncommitted changes (README, CV PDF, `sync_hugo.py`, media, `.generated` markers) stay untouched and uncommitted.
5. **Rename the repo**
   - `gh repo rename amceachin-code.github.io` on `academic-site`.
   - Confirm the custom domain is still set, update the local remote URL, and re-run the deploy workflow if needed.
6. **Verify live**
   - www.andrew-mceachin.com (home), `/tools/`, `/multiplication-worksheet/`, `/grade-inflation/` all load.
   - The grade-inflation chat answers a message from the new domain.
   - Old `github.io` URLs redirect.

## Side effects to know

- `intervention-simulation` publishes a Pages site, which would appear at www.andrew-mceachin.com/intervention-simulation/. Decision: turn off its Pages site before the rename. Turning it back on later puts it under the personal domain; to keep it separate, host it elsewhere (e.g. Vercel).
- A future repo can't share a name with a site section (`code`, `media`, `publications`, `tools`).
- The local folder stays named `academic-site`. Only the GitHub name changes.

## Rollback

Rename the repo back to `academic-site`. The tool URLs return to `github.io`, and the chat still works because the old origin stays allowed.
