#!/usr/bin/env python3
"""MLRO Morning Brief: build the compliance dashboard.

    python run.py              build output/index.html and open it in your browser
    python run.py --no-open    build only (for scheduled jobs)
    python run.py --serve      serve on http://localhost:8765 and rebuild every hour
    python run.py --offline    build without network access (FATF lists only)
    python run.py --notify     also send a push notification (topic in data/notify.json, see README)
"""

from __future__ import annotations

import argparse
import functools
import http.server
import json
import os
import sys
import threading
import time
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from dashboard import notify  # noqa: E402
from dashboard.render import build_data, copy_static, render  # noqa: E402

CACHE = ROOT / "cache" / "feeds.json"


def build(out_dir: Path, offline: bool = False, send_notification: bool = False) -> Path:
    try:
        cache = json.loads(CACHE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        cache = {}
    data = build_data(cache, offline=offline)
    if send_notification and not offline:
        _notify(data, cache)
    if not offline:
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        CACHE.write_text(json.dumps(cache), encoding="utf-8")

    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "index.html"
    out.write_text(render(data), encoding="utf-8")
    copy_static(out_dir)

    feeds = [f for s in data["sections"] for f in s["feeds"]]
    failed = [f["name"] for f in feeds if f["error"]]
    stories = sum(len(f["items"]) for f in feeds)
    print(f"Built {out}  ({stories} stories from {len(feeds) - len(failed)}/{len(feeds)} feeds)")
    for name in failed:
        print(f"  ! could not fetch: {name}")
    st = data["fatf_status"]
    if st["newer"]:
        print("  ! NEW FATF statement published since", data["fatf"]["as_of"], "- update data/fatf_lists.json:")
        for p in st["newer"]:
            print("    ", p["url"])
    elif st["error"] and not offline:
        print("  ! could not check fatf-gafi.org for new statements:", st["error"])
    return out


def _notify(data: dict, cache: dict) -> None:
    try:
        config = json.loads((ROOT / "data" / "notify.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        config = {}
    topic = os.environ.get("NTFY_TOPIC", "").strip() or config.get("topic", "")
    if not topic:
        print("  ! --notify given but no ntfy topic set (NTFY_TOPIC or data/notify.json); skipping")
        return
    message = notify.compose(data, cache)
    try:
        notify.send(message, topic,
                    click_url=os.environ.get("DASHBOARD_URL") or config.get("dashboard_url") or None,
                    server=os.environ.get("NTFY_SERVER") or config.get("server") or "https://ntfy.sh",
                    token=os.environ.get("NTFY_TOKEN") or None)
        print("  notification sent:", message["body"].splitlines()[0])
    except Exception as exc:
        print("  ! notification failed:", exc)


def serve(out_dir: Path, port: int, every_minutes: int) -> None:
    def loop() -> None:
        while True:
            time.sleep(every_minutes * 60)
            try:
                build(out_dir)
            except Exception as exc:  # keep serving the last good build
                print("rebuild failed:", exc)

    threading.Thread(target=loop, daemon=True).start()
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(out_dir))
    with http.server.ThreadingHTTPServer(("127.0.0.1", port), handler) as httpd:
        url = f"http://localhost:{port}/"
        print(f"Serving {url}  (rebuilding every {every_minutes} min, Ctrl+C to stop)")
        webbrowser.open(url)
        httpd.serve_forever()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=str(ROOT / "output"), help="output directory (default: ./output)")
    ap.add_argument("--no-open", action="store_true", help="do not open the browser")
    ap.add_argument("--offline", action="store_true", help="skip all network requests")
    ap.add_argument("--serve", action="store_true", help="run a local server that rebuilds periodically")
    ap.add_argument("--notify", action="store_true", help="send a push notification via ntfy (needs NTFY_TOPIC)")
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--every", type=int, default=60, help="rebuild interval in minutes when serving")
    args = ap.parse_args()

    out_dir = Path(args.out)
    out = build(out_dir, offline=args.offline, send_notification=args.notify)
    if args.serve:
        serve(out_dir, args.port, args.every)
    elif not args.no_open:
        webbrowser.open(out.resolve().as_uri())


if __name__ == "__main__":
    main()
