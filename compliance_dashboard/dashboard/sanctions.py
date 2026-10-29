"""Daily diff of the UK Sanctions List and the OFAC SDN list.

Each run downloads the full official lists, compares them with the snapshot
saved by the previous run, and records additions, removals and (UK only)
amendments. The first run only records a baseline.
"""

from __future__ import annotations

import csv
import io
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

from .feeds import fetch_url

UK_URL = "https://sanctionslist.fcdo.gov.uk/docs/UK-Sanctions-List.xml"
UK_SEARCH = "https://www.gov.uk/government/publications/the-uk-sanctions-list"
OFAC_URL = "https://sanctionslistservice.ofac.treas.gov/api/PublicationPreview/exports/SDN.CSV"
OFAC_SEARCH = "https://sanctionssearch.ofac.treas.gov/"
KEEP_DAYS = 30
MAX_NAMES = 200  # per change event, to keep the page small


def _t(el: ET.Element | None, tag: str) -> str:
    c = el.find(tag) if el is not None else None
    return (c.text or "").strip() if c is not None else ""


def parse_uk(data: bytes) -> tuple[dict, str]:
    """Return ({unique_id: entry}, date_generated) from the FCDO XML file."""
    root = ET.fromstring(data)
    out = {}
    for d in root.iter("Designation"):
        uid = _t(d, "UniqueID")
        if not uid:
            continue
        names = d.findall("Names/Name")
        primary = next((n for n in names if _t(n, "NameType") == "Primary Name"), names[0] if names else None)
        parts = [_t(primary, f"Name{i}") for i in range(1, 7)]
        out[uid] = {
            "name": " ".join(p for p in parts if p),
            "type": _t(d, "IndividualEntityShip"),
            # "The Russia (Sanctions) (EU Exit) Regulations 2019" -> "Russia"
            "regime": re.sub(r"^The\s+|\s*\(Sanctions\).*$", "", _t(d, "RegimeName")),
            "updated": _t(d, "LastUpdated"),
        }
    return out, _t(root, "DateGenerated")


def parse_ofac(data: bytes) -> dict:
    """Return {ent_num: entry} from OFAC's SDN.CSV (no header row; '-0-' means empty)."""
    text = data.decode("utf-8", "replace").replace("\x1a", "")
    out = {}
    for row in csv.reader(io.StringIO(text)):
        if len(row) < 4 or not row[0].strip().isdigit():
            continue
        clean = [c.strip() if c.strip() != "-0-" else "" for c in row]
        out[clean[0]] = {
            "name": clean[1],
            "type": clean[2].title() if clean[2] else "Entity",
            "regime": clean[3],
        }
    return out


def diff(old: dict, new: dict, track_updates: bool = False) -> dict:
    added = [dict(new[k], id=k) for k in new.keys() - old.keys()]
    removed = [dict(old[k], id=k) for k in old.keys() - new.keys()]
    amended = 0
    if track_updates:
        amended = sum(1 for k in new.keys() & old.keys() if new[k].get("updated") != old[k].get("updated"))
    added.sort(key=lambda e: e["name"])
    removed.sort(key=lambda e: e["name"])
    return {"added": added, "removed": removed, "amended": amended}


def _update(key: str, label: str, fetch, cache: dict, now: datetime) -> dict:
    store = cache.setdefault(key, {"snapshot": None, "events": []})
    result = {"label": label, "error": None, "count": None, "list_date": None, "baseline": False}
    try:
        entries, list_date = fetch()
    except Exception as exc:
        result["error"] = f"{type(exc).__name__}: {exc}"[:200]
    else:
        if len(entries) < 100:  # a truncated or error download; don't record it as mass removals
            result["error"] = f"download looked incomplete ({len(entries)} entries)"
        else:
            result["count"], result["list_date"] = len(entries), list_date
            if store["snapshot"] is None:
                result["baseline"] = True
            else:
                d = diff(store["snapshot"], entries, track_updates=(key == "uk"))
                if d["added"] or d["removed"] or d["amended"]:
                    store["events"].insert(0, {
                        "seen": now.isoformat(),
                        "list_date": list_date,
                        "added_count": len(d["added"]),
                        "removed_count": len(d["removed"]),
                        "amended": d["amended"],
                        "added": d["added"][:MAX_NAMES],
                        "removed": d["removed"][:MAX_NAMES],
                    })
            store["snapshot"] = entries
            store["checked"] = now.isoformat()
    cutoff = (now - timedelta(days=KEEP_DAYS)).isoformat()
    store["events"] = [e for e in store["events"] if e["seen"] >= cutoff]
    result["events"] = store["events"]
    result["checked"] = store.get("checked")
    return result


def update_all(cache: dict, now: datetime | None = None) -> list[dict]:
    now = now or datetime.now(timezone.utc)
    sc = cache.setdefault("sanctions", {})
    uk = _update("uk", "UK Sanctions List", lambda: parse_uk(fetch_url(UK_URL, timeout=90)), sc, now)
    uk.update(source=UK_URL, search=UK_SEARCH,
              note="UK sanctions apply in the Turks and Caicos Islands. Re-screen customers when designations are added.")
    ofac = _update("ofac", "OFAC SDN List", lambda: (parse_ofac(fetch_url(OFAC_URL, timeout=90)), ""), sc, now)
    ofac.update(source=OFAC_URL, search=OFAC_SEARCH,
                note="Relevant to US-dollar business and correspondent banking.")
    return [uk, ofac]


def events_since(lists: list[dict], since_iso: str | None) -> list[tuple[dict, dict]]:
    """(list, event) pairs recorded after `since_iso` (all of them if None)."""
    return [(l, e) for l in lists for e in l.get("events", []) if not since_iso or e["seen"] > since_iso]
