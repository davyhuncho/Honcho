"""Assemble dashboard data and render it into index.html plus the Home Screen app files."""

from __future__ import annotations

import json
import shutil
from datetime import date, datetime, timezone
from pathlib import Path

from . import fatf as fatf_mod
from . import sanctions as sanctions_mod
from .feeds import fetch_sections

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
TEMPLATE = Path(__file__).resolve().parent / "template.html"
STATIC = Path(__file__).resolve().parent / "static"


def _load(name: str) -> dict:
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def build_data(cache: dict, offline: bool = False) -> dict:
    today = date.today()
    fatf = _load("fatf_lists.json")
    sources = _load("sources.json")

    for c in fatf["grey_list"]:
        c["months_listed"] = fatf_mod.months_listed(c.get("listed_since", ""), today)

    if offline:
        fatf_status = {"checked": False, "newer": [], "error": "offline mode",
                       "plenary_passed": fatf_mod.plenary_passed(fatf, today)}
        sections = []
        sanctions = []
    else:
        fatf_status = fatf_mod.check_for_update(fatf)
        sections = fetch_sections(sources, cache.setdefault("feeds", {}))
        sanctions = sanctions_mod.update_all(cache)

    return {
        "generated": datetime.now(timezone.utc).isoformat(),
        "today": today.isoformat(),
        "fatf": fatf,
        "fatf_status": fatf_status,
        "sections": sections,
        "sanctions": sanctions,
        "resources": sources.get("resources", []),
        "calendar": _load("calendar.json")["events"],
        "checklist": _load("checklist.json")["items"],
    }


def render(data: dict) -> str:
    # Escape "</" so feed text can never close the <script> tag early.
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    return TEMPLATE.read_text(encoding="utf-8").replace("/*__DATA__*/null", payload)


def copy_static(out_dir: Path) -> None:
    """Copy the Home Screen app files (manifest, icons, service worker) next to index.html."""
    for f in STATIC.iterdir():
        if f.is_file():
            shutil.copyfile(f, out_dir / f.name)
