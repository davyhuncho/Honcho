"""Morning push notification via ntfy (https://ntfy.sh): free, no account needed.

Install the ntfy app on your phone, subscribe to your private topic name, and set
NTFY_TOPIC (and optionally DASHBOARD_URL) when running the build.
"""

from __future__ import annotations

import urllib.request
from datetime import date

from .feeds import USER_AGENT

MAX_SEEN = 3000


def _all_items(data: dict) -> list[dict]:
    return [i for s in data["sections"] for f in s["feeds"] for i in f["items"]]


def compose(data: dict, cache: dict, today: date | None = None) -> dict:
    """Build the notification and record which stories have now been announced.

    Returns {"title", "body", "priority", "tags"}. Stories count as new if their
    link was not in a previous notification.
    """
    today = today or date.today()
    seen = set(cache.get("notified", []))
    items = [i for i in _all_items(data) if i.get("link")]
    new = [i for i in items if i["link"] not in seen]
    watch_new = [i for i in new if i.get("watch")]

    lines, priority, tags = [], 3, ["briefcase"]
    fatf = data["fatf"]
    newer = data["fatf_status"].get("newer") or []
    if newer:
        priority, tags = 4, ["warning"]
        lines.append("New FATF statement published. Check the grey/black list changes and update the dashboard.")
    elif data["fatf_status"].get("plenary_passed"):
        priority, tags = 4, ["warning"]
        lines.append("FATF plenary has ended: new grey/black lists are out. The dashboard lists need updating.")

    np = fatf.get("next_plenary") or {}
    if np.get("start"):
        to_start = (date.fromisoformat(np["start"]) - today).days
        to_end = (date.fromisoformat(np.get("end") or np["start"]) - today).days
        if 0 < to_start <= 14:
            lines.append(f"FATF plenary in {to_start} day{'s' if to_start != 1 else ''}.")
        elif to_start <= 0 <= to_end:
            lines.append("FATF plenary in session" + (" - outcomes today." if to_end == 0 else "."))

    if watch_new:
        lines.append(f"{len(watch_new)} new on your watch list (TCI, Caribbean, BVI...):")
        lines += [f"- {i['title']}" for i in watch_new[:3]]
    other = len(new) - len(watch_new)
    if other > 0:
        lines.append(f"{other} other new AML / sanctions stories.")
    if not lines:
        lines.append("No new stories since yesterday.")

    current = [i["link"] for i in items]
    current_set = set(current)
    cache["notified"] = (current + [l for l in cache.get("notified", []) if l not in current_set])[:MAX_SEEN]
    return {
        "title": f"MLRO Brief - {today.strftime('%a %d %b')}",
        "body": "\n".join(lines),
        "priority": priority,
        "tags": tags,
    }


def send(message: dict, topic: str, click_url: str | None = None,
         server: str = "https://ntfy.sh", token: str | None = None) -> None:
    headers = {
        "Title": message["title"],
        "Priority": str(message["priority"]),
        "Tags": ",".join(message["tags"]),
        "User-Agent": USER_AGENT,
    }
    if click_url:
        headers["Click"] = click_url
        headers["Actions"] = f"view, Open brief, {click_url}"
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(f"{server.rstrip('/')}/{topic}", data=message["body"].encode("utf-8"),
                                 headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=20) as resp:
        resp.read()
