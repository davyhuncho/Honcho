import sys
import unittest
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dashboard import fatf, feeds, render  # noqa: E402

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


if __name__ == "__main__":
    unittest.main()
