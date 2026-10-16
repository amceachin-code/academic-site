# Lessons

## 2026-10-16: Check new heading levels in dark mode

- What happened: the tools page got new h3 sub-headings. They looked fine in a light-mode build but were invisible on the live site for visitors whose OS is in dark mode.
- Why: `custom.css` keeps the page white under `.dark`, but the theme's dark prose styles still recolor headings. Only h2 had a pinned color.
- Rule: when adding a heading level or prose element the site has not used before, check it with dark mode emulated, not just light mode.
