"""Fetch and parse RSS / Atom feeds using only the Python standard library."""

from __future__ import annotations

import html
import re
import ssl
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36 ComplianceDashboard/1.0"
)
TIMEOUT = 20

_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"\s+")


def fetch_url(url: str, timeout: int = TIMEOUT) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
        return resp.read()


def _local(tag: str) -> str:
    """Strip an XML namespace: '{http://www.w3.org/2005/Atom}entry' -> 'entry'."""
    return tag.rsplit("}", 1)[-1]


def _child(el: ET.Element, name: str) -> ET.Element | None:
    for c in el:
        if _local(c.tag) == name:
            return c
    return None


def _text(el: ET.Element, name: str) -> str:
    c = _child(el, name)
    return (c.text or "").strip() if c is not None else ""


def clean_text(s: str, limit: int = 280) -> str:
    s = html.unescape(_TAG_RE.sub(" ", html.unescape(s or "")))
    s = _WS_RE.sub(" ", s).strip()
    return s if len(s) <= limit else s[: limit - 1].rsplit(" ", 1)[0] + "…"


def parse_date(s: str) -> datetime | None:
    s = (s or "").strip()
    if not s:
        return None
    try:
        d = parsedate_to_datetime(s)
    except (TypeError, ValueError, IndexError):
        try:
            d = datetime.fromisoformat(s.replace("Z", "+00:00"))
        except ValueError:
            return None
    if d.tzinfo is None:
        d = d.replace(tzinfo=timezone.utc)
    return d.astimezone(timezone.utc)


def parse_feed(data: bytes) -> list[dict]:
    """Parse RSS 2.0, RSS 1.0 (RDF) or Atom into a list of item dicts."""
    root = ET.fromstring(data)
    items: list[dict] = []
    for el in root.iter():
        kind = _local(el.tag)
        if kind == "item":
            link = _text(el, "link") or _text(el, "guid")
            date = parse_date(_text(el, "pubDate") or _text(el, "date"))
            summary = _text(el, "description")
            src = _child(el, "source")
            source = (src.text or "").strip() if src is not None else ""
        elif kind == "entry":
            link = ""
            for c in el:
                if _local(c.tag) == "link" and c.get("rel", "alternate") == "alternate":
                    link = c.get("href", "")
                    break
            date = parse_date(_text(el, "updated") or _text(el, "published"))
            summary = _text(el, "summary") or _text(el, "content")
            source = ""
        else:
            continue
        title = clean_text(_text(el, "title"), 300)
        # Google News appends " - Publisher" to titles; split it out.
        if source and title.endswith(" - " + source):
            title = title[: -len(source) - 3]
        if not title:
            continue
        summary = clean_text(summary)
        if summary.startswith(title):
            summary = ""
        items.append({
            "title": title,
            "link": link.strip(),
            "date": date.isoformat() if date else None,
            "source": source,
            "summary": summary,
        })
    return items


def _norm_title(t: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", t.lower()).strip()[:90]


def fetch_feed(feed: dict, max_items: int, max_age_days: int) -> dict:
    result = {"name": feed["name"], "url": feed["url"], "items": [], "error": None}
    try:
        items = parse_feed(fetch_url(feed["url"]))
    except Exception as exc:  # network errors, bad XML, HTTP errors
        result["error"] = f"{type(exc).__name__}: {exc}"[:200]
        return result
    cutoff = datetime.now(timezone.utc) - timedelta(days=max_age_days)
    fresh = [i for i in items if not i["date"] or datetime.fromisoformat(i["date"]) >= cutoff]
    fresh.sort(key=lambda i: i["date"] or "", reverse=True)
    result["items"] = fresh[:max_items]
    return result


def fetch_sections(sources: dict, cache: dict) -> list[dict]:
    """Fetch every enabled feed in parallel. Falls back to cached items on failure."""
    max_items = sources.get("max_items_per_feed", 12)
    max_age = sources.get("max_age_days", 21)
    watch = [(w, re.compile(r"\b" + re.escape(w.lower()))) for w in sources.get("watch_terms", [])]

    jobs = [(s, f) for s in sources["sections"] for f in s["feeds"] if f.get("enabled", True)]
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(lambda sf: fetch_feed(sf[1], max_items, max_age), jobs))

    sections: dict[str, dict] = {}
    for (section, _), res in zip(jobs, results):
        key = res["url"]
        if res["error"] and cache.get(key):
            res["items"] = cache[key]["items"]
            res["stale_since"] = cache[key]["fetched"]
        elif not res["error"]:
            cache[key] = {"items": res["items"], "fetched": datetime.now(timezone.utc).isoformat()}
        for item in res["items"]:
            hay = (item["title"] + " " + item["summary"]).lower()
            item["watch"] = [w for w, rx in watch if rx.search(hay)]
        out = sections.setdefault(section["id"], {"id": section["id"], "title": section["title"], "feeds": []})
        out["feeds"].append(res)

    # Remove duplicate stories that appear in more than one feed of a section.
    for sec in sections.values():
        seen: set[str] = set()
        for feed in sec["feeds"]:
            unique = []
            for item in feed["items"]:
                k = _norm_title(item["title"])
                if k not in seen:
                    seen.add(k)
                    unique.append(item)
            feed["items"] = unique
    return list(sections.values())
