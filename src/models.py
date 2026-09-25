from dataclasses import dataclass, field    # dataclass = struct with less boilerplate
from datetime import datetime

@dataclass
class Listing:
    title: str                              # job title as posted
    company: str                            # company name
    location: str                           # city/region, or "" if unstated
    url: str                                # link to the posting
    description: str                        # plain text, HTML already stripped
    posted_date: datetime | None            # None when a source omits it
    sources: list[str] = field(default_factory=list)   # every source this appeared in