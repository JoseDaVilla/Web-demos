"""Inline SVG icons from two libraries, vendored in build/icons/.

- brands/: Simple Icons (CC0), the official brand marks (WhatsApp,
  Instagram...). Filled shapes, drawn with currentColor.
- lucide/: Lucide (ISC), general line icons (phone, stethoscope...).

To add an icon, copy its SVG from the npm packages `simple-icons` or
`lucide-static` into the matching folder.
"""
import re
from pathlib import Path

DIR = Path(__file__).resolve().parent / "icons"


def icon(name, cls="ico"):
    """Return an inline <svg> for `name` ("brands/whatsapp" or "lucide/phone")."""
    svg = (DIR / f"{name}.svg").read_text(encoding="utf-8")
    svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S)
    svg = re.sub(r"<title>.*?</title>", "", svg, flags=re.S)
    svg = re.sub(r'\s(class|width|height|role)="[^"]*"', "", svg)
    svg = re.sub(r"\s+", " ", svg).strip()
    extra = f'class="{cls}" aria-hidden="true" focusable="false"'
    if name.startswith("brands/"):
        extra += ' fill="currentColor"'
    return svg.replace("<svg", f"<svg {extra}", 1)
