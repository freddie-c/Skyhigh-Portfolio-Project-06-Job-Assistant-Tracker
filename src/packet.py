from datetime import datetime
from pathlib import Path
import re
from src.models import Listing
from src.tailor import tailor, TailorError

PACKET_DIR = Path("packets")

def _slug(text: str) -> str:
    """Filesystem-safe name fragment from arbitrary listing text."""
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower())     # strip anything path-unsafe
    return re.sub(r"-+", "-", text).strip("-")[:60]        # collapse dashes, cap length

def render(listing: Listing, result: dict) -> str:
    """Build the full packet as a string. No disk writes here."""
    lines = [
        "# DRAFT — FOR HUMAN REVIEW",
        "",
        "> Nothing here has been submitted anywhere. Review, edit, and send it yourself.",
        "",
        f"*Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}*",
        "",
        "---",
        "",
        f"## {listing.title}",
        f"**{listing.company}** — {listing.location or 'Location not stated'}",
        "",
        f"[View the original posting]({listing.url})",
        "",
        "## Suggested bullets",
        "",
        "Each bullet names what in your resume it draws from. Check that the claim",
        "is one you can defend in an interview before using it.",
        "",
    ]

    for i, bullet in enumerate(result.get("bullets", []), 1):
        lines += [
            f"**{i}.** {bullet.get('text', '')}",
            "",
            f"*Drawn from:* {bullet.get('source', 'unattributed')}",
            "",
        ]

    lines += ["## Keyword gaps", ""]
    gaps = result.get("gaps", [])
    if gaps:
        lines.append("What this listing asks for that your resume does not currently support:")
        lines.append("")
        for gap in gaps:
            lines.append(f"- **{gap.get('keyword', '')}** — {gap.get('note', '')}")
    else:
        lines.append("No gaps identified.")
    lines.append("")

    matched = result.get("matched_keywords", [])
    if matched:
        lines += ["## Already covered", "", ", ".join(matched), ""]

    flags = result.get("flags", [])
    if flags:                                              # surface anything odd in the listing
        lines += ["## ⚠️ Flags on this listing", ""]
        lines += [f"- {flag}" for flag in flags]
        lines.append("")

    lines += [
        "---",
        "",
        "## Next step",
        "",
        "This tool stops here, by design. Edit these bullets into your resume,",
        "apply through the company's own site, then mark the listing Applied.",
        "",
    ]
    return "\n".join(lines)

def generate(listing: Listing) -> Path:
    """Tailor, render, and write. Raises TailorError without touching disk."""
    result = tailor(listing)                               # may raise — nothing written yet
    content = render(listing, result)                      # built fully in memory

    PACKET_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M")
    path = PACKET_DIR / f"{_slug(listing.company)}-{_slug(listing.title)}-{stamp}.md"
    path.write_text(content)                               # single write, only on success
    return path