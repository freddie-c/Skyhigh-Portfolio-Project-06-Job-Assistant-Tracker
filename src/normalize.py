import html                                          # for unescaping &lt; &amp; etc.
import re                                            # for stripping tags
from datetime import datetime
from src.models import Listing

TAG_RE = re.compile(r"<[^>]+>")                      # matches any HTML tag

def _clean_html(raw: str) -> str:
    """Unescape entities, strip tags, collapse whitespace."""
    if not raw:
        return ""
    text = html.unescape(raw)                        # &lt;p&gt; -> <p>
    text = TAG_RE.sub(" ", text)                     # <p> -> space
    text = html.unescape(text)                       # catch double-encoded entities
    return re.sub(r"\s+", " ", text).strip()         # collapse runs of whitespace

def _parse_date(value: str | None) -> datetime | None:
    """Greenhouse gives ISO 8601 with a Z suffix; return None if absent or odd."""
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))   # Z isn't valid ISO for Python
    except ValueError:
        return None                                  # a bad date is not worth crashing over

def from_greenhouse(job: dict, company: str) -> Listing:
    """Map one raw Greenhouse job dict onto the common schema."""
    location = job.get("location") or {}             # may be missing or null
    return Listing(
        title=job.get("title", "").strip(),
        company=job.get("company_name") or company,  # fall back to the config name
        location=location.get("name", "").strip(),   # the nested field, safely
        url=job.get("absolute_url", ""),
        description=_clean_html(job.get("content", "")),
        posted_date=_parse_date(job.get("first_published")),
        sources=["greenhouse"],
    )