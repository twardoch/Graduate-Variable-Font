# TODO

Modernization pass (2026) — done items live in `CHANGELOG.md`.

## Done this pass
- [x] Git health verified (healthy, up to date with origin)
- [x] `.gitignore` hygiene (macOS + Node + Python patterns already present; `.DS_Store` ignored, not tracked)
- [x] Add `tools/validate_font.py` (fontTools parse + fvar axes + instance-range sanity)
- [x] Add CI `font-validation` job
- [x] Rewrite README with axis table, build + validate instructions, corrected links
- [x] Add `CHANGELOG.md` and `TODO.md`
- [x] Generate `docs/assets/icon.png` (< 500 KB)
- [x] First semver tag via `gitnextver`

## Bigger ideas (future)
- [ ] Add [fontbakery](https://github.com/fonttools/fontbakery) to CI for a full
      Open Font quality profile — catches interpolation errors, name-table
      issues, and metrics problems that the lightweight validator does not.
- [ ] Automate the font build. Today the TTF is exported by hand from FontLab;
      a headless build (e.g. via a FontLab CLI export, or a `fontmake`-based
      pipeline from a designspace/UFO round-trip) would let CI rebuild and diff
      the binary instead of trusting a committed artifact.
- [ ] Attach the built `GRADUATE.ttf` (and a zip with the OFL) to GitHub Releases
      so downstream users can grab a versioned binary without cloning.
- [ ] Reconcile with upstream `etunni/Graduate-Variable-Font` — document exactly
      what this fork changed, or open a PR upstream if the deltas are general.
- [ ] Regenerate `assets/GRADUATE-VARIABLE-MAP.pdf` from the current build so the
      specimen poster matches the shipped axes and instances.
- [ ] Consider a STAT-table audit — 27 named instances across weight×width should
      map cleanly onto STAT axis-value records for good menu grouping.
