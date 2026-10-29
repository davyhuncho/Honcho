import sys
import unittest
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dashboard import fatf, feeds, notify, render, sanctions  # noqa: E402

NOW = datetime.now(timezone.utc)
RSS = f"""<?xml version="1.0"?>
<rss version="2.0"><channel><title>t</title>
<item><title>TCI regulator issues AML advisory - Turks and Caicos Weekly News</title>
<link>https://example.com/a</link><pubDate>{NOW.strftime('%a, %d %b %Y %H:%M:%S GMT')}</pubDate>
<description>&lt;a href="x"&gt;TCI regulator issues AML advisory&lt;/a&gt;</description>
<source url="https://tcweeklynews.com">Turks and Caicos Weekly News</source></item>
<item><title>Old story</title><link>https://example.com/old</link>
<pubDate>{(NOW - timedelta(days=90)).strftime('%a, %d %b %Y %H:%M:%S GMT')}</pubDate></item>
</channel></rss>""".encode()

ATOM = f"""<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom"><title>OFSI</title>
<entry><title>Financial sanctions notice: Russia</title>
<link rel="alternate" type="text/html" href="https://www.gov.uk/notice"/>
<updated>{NOW.isoformat().replace('+00:00', 'Z')}</updated>
<summary>Asset freeze targets added.</summary></entry>
</feed>""".encode()


class FeedTests(unittest.TestCase):
    def test_rss_google_news_style(self):
        items = feeds.parse_feed(RSS)
        self.assertEqual(items[0]["title"], "TCI regulator issues AML advisory")
        self.assertEqual(items[0]["source"], "Turks and Caicos Weekly News")
        self.assertEqual(items[0]["summary"], "")  # summary duplicating the title is dropped
        self.assertTrue(items[0]["date"])

    def test_atom(self):
        (item,) = feeds.parse_feed(ATOM)
        self.assertEqual(item["link"], "https://www.gov.uk/notice")
        self.assertEqual(item["summary"], "Asset freeze targets added.")

    def test_fetch_filters_old_and_flags_watch_terms(self):
        sources = {"watch_terms": ["TCI"], "sections": [
            {"id": "a", "title": "A", "feeds": [{"name": "f1", "url": "u1"}, {"name": "f2", "url": "u2"}]}]}
        with mock.patch.object(feeds, "fetch_url", return_value=RSS):
            (sec,) = feeds.fetch_sections(sources, {})
        f1, f2 = sec["feeds"]
        self.assertEqual([i["title"] for i in f1["items"]], ["TCI regulator issues AML advisory"])
        self.assertEqual(f1["items"][0]["watch"], ["TCI"])
        self.assertEqual(f2["items"], [])  # duplicate story removed

    def test_failed_feed_uses_cache(self):
        sources = {"sections": [{"id": "a", "title": "A", "feeds": [{"name": "f", "url": "u"}]}]}
        cache = {"u": {"items": [{"title": "cached", "summary": "", "link": "", "date": None, "source": ""}],
                       "fetched": "2026-10-23T08:00:00+00:00"}}
        with mock.patch.object(feeds, "fetch_url", side_effect=OSError("down")):
            (sec,) = feeds.fetch_sections(sources, cache)
        self.assertEqual(sec["feeds"][0]["items"][0]["title"], "cached")
        self.assertEqual(sec["feeds"][0]["stale_since"], "2026-10-23T08:00:00+00:00")


class FatfTests(unittest.TestCase):
    PAGE = """
      <a href="/en/publications/High-risk-and-other-monitored-jurisdictions/increased-monitoring-october-2026.html">x</a>
      <a href="https://www.fatf-gafi.org/en/publications/High-risk-and-other-monitored-jurisdictions/call-for-action-june-2026.html">y</a>
    """

    def test_detects_newer_statement(self):
        data = {"as_of": "2026-06-19", "sources": {"topic_page": "x"}}
        with mock.patch.object(fatf, "fetch_url", return_value=self.PAGE.encode()):
            st = fatf.check_for_update(data)
        self.assertEqual(len(st["newer"]), 1)
        self.assertEqual(st["newer"][0]["kind"], "increased-monitoring")
        self.assertTrue(st["newer"][0]["url"].startswith("https://www.fatf-gafi.org/en/"))

    def test_plenary_passed_when_site_blocked(self):
        data = {"as_of": "2026-06-19", "sources": {"topic_page": "x"},
                "next_plenary": {"start": "2026-10-28", "end": "2026-10-30"}}
        with mock.patch.object(fatf, "fetch_url", side_effect=OSError("403")):
            self.assertFalse(fatf.check_for_update(data, today=date(2026, 10, 30))["plenary_passed"])
            self.assertTrue(fatf.check_for_update(data, today=date(2026, 10, 31))["plenary_passed"])

    def test_months_listed(self):
        self.assertEqual(fatf.months_listed("2025-06", date(2026, 10, 24)), 16)
        self.assertIsNone(fatf.months_listed("", date(2026, 10, 24)))

    def test_baseline_is_consistent(self):
        data = render._load("fatf_lists.json")
        grey = {c["country"] for c in data["grey_list"]}
        latest = data["history"][0]
        self.assertTrue(set(latest["added"]) <= grey)
        self.assertFalse(set(latest["removed"]) & grey)


class RenderTests(unittest.TestCase):
    def test_render_escapes_script_close(self):
        out = render.render({"x": "</script><b>"})
        self.assertNotIn("</script><b>", out)
        self.assertIn("<\\/script>", out)

    def test_offline_build(self):
        html = render.render(render.build_data({}, offline=True))
        self.assertIn("MLRO Morning Brief", html)
        self.assertNotIn("/*__DATA__*/null", html)


class NotifyTests(unittest.TestCase):
    def _data(self, items, newer=()):
        return {
            "fatf": {"next_plenary": {"start": "2026-10-28", "end": "2026-10-30"}},
            "fatf_status": {"newer": list(newer)},
            "sections": [{"feeds": [{"items": items}]}],
        }

    def test_compose_counts_new_and_watch_stories_once(self):
        items = [
            {"title": "TCI story", "link": "https://a", "watch": ["TCI"]},
            {"title": "Other story", "link": "https://b", "watch": []},
        ]
        cache = {}
        msg = notify.compose(self._data(items), cache, today=date(2026, 10, 24))
        self.assertIn("FATF plenary in 4 days.", msg["body"])
        self.assertIn("1 new on your watch list", msg["body"])
        self.assertIn("- TCI story", msg["body"])
        self.assertIn("1 other new", msg["body"])
        self.assertEqual(msg["priority"], 3)
        # Second run with the same stories announces nothing new.
        msg2 = notify.compose(self._data(items), cache, today=date(2026, 11, 20))
        self.assertEqual(msg2["body"], "No new stories since yesterday.")

    def test_new_fatf_statement_is_high_priority(self):
        msg = notify.compose(self._data([], newer=[{"url": "x"}]), {}, today=date(2026, 10, 30))
        self.assertEqual(msg["priority"], 4)
        self.assertTrue(msg["body"].startswith("New FATF statement published"))
        self.assertIn("outcomes today", msg["body"])

    def test_plenary_passed_is_high_priority(self):
        data = self._data([])
        data["fatf_status"]["plenary_passed"] = True
        msg = notify.compose(data, {}, today=date(2026, 11, 2))
        self.assertEqual(msg["priority"], 4)
        self.assertIn("new grey/black lists are out", msg["body"])

    def test_send_posts_to_ntfy(self):
        captured = {}

        class Resp:
            def __enter__(self): return self
            def __exit__(self, *a): return False
            def read(self): return b"{}"

        def fake_urlopen(req, timeout):
            captured["req"] = req
            return Resp()

        with mock.patch.object(notify.urllib.request, "urlopen", fake_urlopen):
            notify.send({"title": "T", "body": "B ü", "priority": 4, "tags": ["warning"]},
                        "my-topic", click_url="https://example.github.io/Honcho/")
        req = captured["req"]
        self.assertEqual(req.full_url, "https://ntfy.sh/my-topic")
        self.assertEqual(req.get_header("Click"), "https://example.github.io/Honcho/")
        self.assertEqual(req.get_header("Priority"), "4")
        self.assertEqual(req.data, "B ü".encode())


UK_XML = b"""<?xml version="1.0" encoding="utf-8"?>
<Designations><DateGenerated>29/10/2026</DateGenerated>
<Designation><LastUpdated>04/08/2026</LastUpdated><UniqueID>AFG0001</UniqueID>
<Names><Name><Name6>HAJI KHAIRULLAH MONEY EXCHANGE</Name6><NameType>Primary Name</NameType></Name>
<Name><Name6>Haji Alim Hawala</Name6><NameType>Alias</NameType></Name></Names>
<RegimeName>The Afghanistan (Sanctions) (EU Exit) Regulations 2020</RegimeName>
<IndividualEntityShip>Entity</IndividualEntityShip></Designation>
<Designation><LastUpdated>01/10/2026</LastUpdated><UniqueID>RUS0002</UniqueID>
<Names><Name><Name1>Ivan</Name1><Name6>PETROV</Name6><NameType>Primary Name</NameType></Name></Names>
<RegimeName>The Russia (Sanctions) (EU Exit) Regulations 2019</RegimeName>
<IndividualEntityShip>Individual</IndividualEntityShip></Designation>
</Designations>"""

OFAC_CSV = (b'36,"AEROCARIBBEAN AIRLINES",-0- ,"CUBA",-0- ,-0- ,-0- ,-0- ,-0- ,-0- ,-0- ,-0- \r\n'
            b'306,"BANCO NACIONAL DE CUBA",-0- ,"CUBA",-0- ,-0- ,-0- ,-0- ,-0- ,-0- ,-0- ,"a.k.a. \'BNC\'."\r\n'
            b'7157,"SMITH, John",individual,"SDGT",-0- ,-0- ,-0- ,-0- ,-0- ,-0- ,-0- ,-0- \r\n\x1a')


class SanctionsTests(unittest.TestCase):
    def test_parse_uk(self):
        entries, generated = sanctions.parse_uk(UK_XML)
        self.assertEqual(generated, "29/10/2026")
        self.assertEqual(entries["AFG0001"]["name"], "HAJI KHAIRULLAH MONEY EXCHANGE")
        self.assertEqual(entries["AFG0001"]["regime"], "Afghanistan")
        self.assertEqual(entries["RUS0002"]["name"], "Ivan PETROV")
        self.assertEqual(entries["RUS0002"]["type"], "Individual")

    def test_parse_ofac(self):
        entries = sanctions.parse_ofac(OFAC_CSV)
        self.assertEqual(set(entries), {"36", "306", "7157"})
        self.assertEqual(entries["7157"], {"name": "SMITH, John", "type": "Individual", "regime": "SDGT"})
        self.assertEqual(entries["36"]["type"], "Entity")

    def test_diff(self):
        old = {"A": {"name": "a", "updated": "1"}, "B": {"name": "b", "updated": "1"}}
        new = {"B": {"name": "b", "updated": "2"}, "C": {"name": "c", "updated": "1"}}
        d = sanctions.diff(old, new, track_updates=True)
        self.assertEqual([e["id"] for e in d["added"]], ["C"])
        self.assertEqual([e["id"] for e in d["removed"]], ["A"])
        self.assertEqual(d["amended"], 1)

    def test_update_baseline_then_change_and_guard(self):
        cache = {}
        big = {str(i): {"name": f"n{i}"} for i in range(150)}
        now = datetime(2026, 10, 29, 10, tzinfo=timezone.utc)
        r = sanctions._update("ofac", "OFAC SDN List", lambda: (big, ""), cache, now)
        self.assertTrue(r["baseline"])
        bigger = dict(big, x={"name": "New Person"})
        del bigger["0"]
        r = sanctions._update("ofac", "OFAC SDN List", lambda: (bigger, ""), cache, now + timedelta(days=1))
        (ev,) = r["events"]
        self.assertEqual((ev["added_count"], ev["removed_count"]), (1, 1))
        # A truncated download must not be recorded as mass removals.
        r = sanctions._update("ofac", "OFAC SDN List", lambda: ({"1": {"name": "x"}}, ""), cache, now + timedelta(days=2))
        self.assertIn("incomplete", r["error"])
        self.assertEqual(len(r["events"]), 1)
        self.assertEqual(len(cache["ofac"]["snapshot"]), 150)

    def test_notification_reports_changes_once(self):
        lists = [{"label": "UK Sanctions List", "events": [
            {"seen": "2026-10-29T10:00:00+00:00", "added_count": 3, "removed_count": 1, "amended": 2}]}]
        data = {"fatf": {}, "fatf_status": {}, "sections": [], "sanctions": lists}
        cache = {"notified_at": "2026-10-28T10:00:00+00:00"}
        msg = notify.compose(data, cache, today=date(2026, 10, 29))
        self.assertIn("Sanctions list changes: UK +3 -1 2 amended. Re-screen customers.", msg["body"])
        self.assertEqual(msg["priority"], 4)
        msg = notify.compose(data, cache, today=date(2026, 10, 30))
        self.assertNotIn("Sanctions", msg["body"])


if __name__ == "__main__":
    unittest.main()
