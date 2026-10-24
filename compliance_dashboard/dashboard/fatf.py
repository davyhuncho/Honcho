"""FATF black / grey list data plus a live check for newer FATF statements."""

from __future__ import annotations

import re
from datetime import date

from .feeds import fetch_url

MONTHS = {m: i for i, m in enumerate(
    ["january", "february", "march", "april", "may", "june", "july",
     "august", "september", "october", "november", "december"], start=1)}

# e.g. /en/publications/High-risk-and-other-monitored-jurisdictions/increased-monitoring-october-2026.html
_PUB_RE = re.compile(
    r'href="([^"]*High-risk-and-other-monitored-jurisdictions/'
    r'(increased-monitoring|call-for-action)-([a-z]+)-(\d{4})[^"]*)"',
    re.IGNORECASE,
)


def find_publications(page_html: str) -> list[dict]:
    """Extract FATF list publications (kind, year, month, url) from a FATF page."""
    pubs = {}
    for href, kind, month, year in _PUB_RE.findall(page_html):
        m = MONTHS.get(month.lower())
        if not m:
            continue
        url = href if href.startswith("http") else "https://www.fatf-gafi.org" + href
        pubs[(kind.lower(), int(year), m)] = {
            "kind": kind.lower(), "year": int(year), "month": m, "url": url,
        }
    return sorted(pubs.values(), key=lambda p: (p["year"], p["month"]), reverse=True)


def plenary_passed(fatf: dict, today: date | None = None) -> bool:
    """True once the next plenary listed in the baseline has ended.

    FATF publishes updated statements on the last day of every plenary, so after
    that date the local lists are out of date even if fatf-gafi.org can't be
    reached (it blocks some automated requests).
    """
    np = fatf.get("next_plenary") or {}
    end = np.get("end") or np.get("start")
    return bool(end) and (today or date.today()) > date.fromisoformat(end)


def check_for_update(fatf: dict, today: date | None = None) -> dict:
    """Compare the newest statement on fatf-gafi.org with the local baseline."""
    as_of = date.fromisoformat(fatf["as_of"])
    status = {"checked": False, "newer": [], "error": None, "plenary_passed": plenary_passed(fatf, today)}
    try:
        page = fetch_url(fatf["sources"]["topic_page"]).decode("utf-8", "replace")
    except Exception as exc:
        status["error"] = f"{type(exc).__name__}: {exc}"[:200]
        return status
    status["checked"] = True
    status["newer"] = [
        p for p in find_publications(page)
        if (p["year"], p["month"]) > (as_of.year, as_of.month)
    ]
    return status


def months_listed(since: str, today: date) -> int | None:
    try:
        y, m = (int(x) for x in since.split("-")[:2])
    except (ValueError, AttributeError):
        return None
    return (today.year - y) * 12 + today.month - m
