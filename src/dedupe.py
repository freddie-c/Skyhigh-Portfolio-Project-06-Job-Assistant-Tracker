import re
from src.models import Listing

def _key(listing: Listing) -> tuple[str, str, str]:
    """Identity of a job, independent of which source it came from."""
    def norm(value: str) -> str:
        value = value.lower().strip()
        value = re.sub(r"[^a-z0-9 ]", " ", value)     # drop punctuation, commas, dashes
        return re.sub(r"\s+", " ", value).strip()     # collapse whitespace
    return (norm(listing.company), norm(listing.title), norm(listing.location))

def dedupe(listings: list[Listing]) -> list[Listing]:
    """Keep the first occurrence; merge the sources of later copies into it."""
    seen: dict[tuple[str, str, str], Listing] = {}
    for listing in listings:
        key = _key(listing)
        if key not in seen:
            seen[key] = listing                        # first one wins
            continue
        kept = seen[key]
        for source in listing.sources:                 # don't lose where the copy came from
            if source not in kept.sources:
                kept.sources.append(source)
    return list(seen.values())
