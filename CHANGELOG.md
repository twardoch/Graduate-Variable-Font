# Changelog

All notable changes to the Graduate Variable Font project are recorded here.

## [Unreleased] — 2026 modernization pass

### Added
- `tools/validate_font.py` — a self-contained `fontTools` check that parses the
  built variable font, confirms all twelve axes are present, and verifies every
  named instance sits inside its axis range. Runs locally (`uv run`) and in CI.
- `.github/workflows/ci.yml` — a `font-validation` job that runs the validator on
  every push and pull request.
- `CHANGELOG.md`, `TODO.md` — project history and forward-looking task list.

### Changed
- Rewrote `README.md`: replaced the upstream boilerplate with a ground-truth axis
  table (tags, ranges, defaults read from the binary), build and validation
  instructions, and corrected links to point at the `twardoch` fork rather than
  the upstream `etunni` repository. The older date-stamped history moved here.

### Notes
- No design changes. The font sources (`sources/GRADUATE-2019.vfc`) and the built
  `GRADUATE.ttf` binaries are untouched — the product itself is unchanged.
- Validation evidence: `python tools/validate_font.py` reports both tracked TTFs
  as valid — 12 axes, 27 named instances, 563 glyphs each.

## Design history (from upstream, pre-modernization)

- **10 Oct 2019** — Project website added at the GitHub Pages site.
- **26 Mar 2019** — Build reaches 12 axes; newest is "Largo Serif" (SELE),
  controlling serif length. Included in the Axis-Praxis specimen (thanks to
  Laurence Penney).
- **11 Oct 2018** — PDF poster of the current axis map added.
- **27 Sep 2018** — General improvements; fixed an issue in the letter "b".
- **26 Sep 2018** — Added the YTDD axis (descender diacritic distance). Removed
  the SLANT axis pending correct variation across all axes. Improved the
  relationship of contrast/weight/width variations.
- **17 Sep 2018** — Added the YTLC axis (lowercase height).
- **12 Sep 2018** — First commit (Eduardo Tunni). Initial 10 axes: Weight, Width,
  Optical Size, Grade, Slant (later removed), Contrast, Yopaque, Ytrans, Ytad,
  Ytlc, Ytdd.
