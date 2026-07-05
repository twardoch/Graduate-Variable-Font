#!/usr/bin/env -S uv run -s
# /// script
# dependencies = ["fonttools>=4.50"]
# ///
# this_file: tools/validate_font.py
"""Sanity-check the built Graduate variable font.

Every release ships one binary: a variable TTF with twelve design axes. If that
file will not parse, or an axis has gone missing, or a named instance points
outside its own axis range, the font is broken before anyone installs it. This
script is the gate. It parses each TTF passed on the command line (defaulting to
the two tracked copies), confirms the expected axes are present and ordered
sanely, and checks that every named instance sits inside the axis box.

Run it locally or in CI:

    python tools/validate_font.py
    python tools/validate_font.py fonts/variable/GRADUATE.ttf
"""

from __future__ import annotations

import sys
from pathlib import Path

from fontTools.ttLib import TTFont

# The twelve axes the Graduate variable font is designed to carry. If a build
# drops one or renames a tag, that is a regression we want to hear about loudly.
EXPECTED_AXES: frozenset[str] = frozenset(
    {
        "XOPQ",  # horizontal opaque — stem thickness (weight)
        "XTRA",  # horizontal transparent — counter width (width)
        "OPSZ",  # optical size
        "GRAD",  # grade
        "YTRA",  # vertical transparent
        "CNTR",  # contrast
        "YOPQ",  # vertical opaque
        "SERF",  # serif presence
        "YTAS",  # ascender height
        "YTLC",  # lowercase height
        "YTDE",  # descender depth
        "SELE",  # serif length ("Largo Serif")
    }
)

DEFAULT_FONTS: tuple[str, ...] = (
    "fonts/variable/GRADUATE.ttf",
    "docs/fonts/GRADUATE.ttf",
)


def validate(path: Path) -> list[str]:
    """Return a list of problems found in one font file. Empty means clean."""
    problems: list[str] = []
    try:
        font = TTFont(path)
    except Exception as exc:  # noqa: BLE001 — surface any parse failure verbatim
        return [f"cannot parse {path}: {exc}"]

    if "fvar" not in font:
        return [f"{path}: no fvar table — this is not a variable font"]

    fvar = font["fvar"]
    axes = {a.axisTag: a for a in fvar.axes}

    missing = EXPECTED_AXES - axes.keys()
    if missing:
        problems.append(f"{path}: missing axes {sorted(missing)}")
    extra = axes.keys() - EXPECTED_AXES
    if extra:
        problems.append(f"{path}: unexpected axes {sorted(extra)}")

    for tag, axis in axes.items():
        if not axis.minValue <= axis.defaultValue <= axis.maxValue:
            problems.append(
                f"{path}: axis {tag} default {axis.defaultValue} outside "
                f"[{axis.minValue}, {axis.maxValue}]"
            )

    for inst in fvar.instances:
        for tag, value in inst.coordinates.items():
            axis = axes.get(tag)
            if axis is None:
                problems.append(f"{path}: instance uses unknown axis {tag}")
            elif not axis.minValue <= value <= axis.maxValue:
                problems.append(
                    f"{path}: instance coordinate {tag}={value} outside "
                    f"[{axis.minValue}, {axis.maxValue}]"
                )

    if not problems:
        print(
            f"OK  {path}  {len(axes)} axes, "
            f"{len(fvar.instances)} named instances, "
            f"{font['maxp'].numGlyphs} glyphs"
        )
    return problems


def main(argv: list[str]) -> int:
    targets = argv[1:] or [p for p in DEFAULT_FONTS if Path(p).exists()]
    if not targets:
        print("no font files found to validate", file=sys.stderr)
        return 1

    problems: list[str] = []
    for target in targets:
        problems.extend(validate(Path(target)))

    if problems:
        print("\nFONT VALIDATION FAILED:", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 1

    print(f"\nAll {len(targets)} font file(s) valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
