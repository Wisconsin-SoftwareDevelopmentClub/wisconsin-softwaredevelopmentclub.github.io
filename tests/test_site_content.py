"""Protect the config-to-HTML workflow, including future board updates."""

import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location("update_site", ROOT / "scripts/update_site.py")
SITE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SITE)


class SiteContentTests(unittest.TestCase):
    def setUp(self):
        self.config = json.loads((ROOT / "config.json").read_text())

    def regions(self, config=None):
        return SITE.render_regions(config or self.config, "info.html", "About")

    def test_checked_in_pages_are_synchronized_and_idempotent(self):
        for filename, label in SITE.PAGES:
            with self.subTest(page=filename):
                source = (ROOT / filename).read_text()
                regions = SITE.render_regions(self.config, filename, label)
                self.assertEqual(source, SITE.sync_page(source, regions))
                self.assertEqual(source, SITE.sync_page(SITE.sync_page(source, regions), regions))

    def test_no_unconfirmed_roster_or_schedule_is_rendered(self):
        config = copy.deepcopy(self.config)
        config.update(board=[], meeting=None, announcement=None)
        regions = self.regions(config)
        self.assertEqual(regions["board"], "")
        self.assertEqual(regions["announcement"], "")
        self.assertIn("current meeting times", regions["meeting"])

    def test_current_roster_and_public_contact_are_optional(self):
        config = copy.deepcopy(self.config)
        config["board"] = [
            {"name": "Test Member", "title": "President", "email": "member@example.com", "isContact": True},
            {"name": "Another Member", "title": "Engineering", "email": "private@example.com", "isContact": False},
        ]
        board = self.regions(config)["board"]
        self.assertIn("Test Member", board)
        self.assertIn("mailto:member@example.com", board)
        self.assertNotIn("private@example.com", board)
        self.assertNotIn("<img", board)

    def test_content_is_text_and_links_use_https(self):
        config = copy.deepcopy(self.config)
        config["announcement"] = '<script>alert("hello")</script>'
        config["meeting"] = "Room A & B"
        regions = self.regions(config)
        self.assertNotIn("<script>", regions["announcement"])
        self.assertIn("&lt;script&gt;", regions["announcement"])
        self.assertIn("Room A &amp; B", regions["meeting"])
        config["discordLink"] = "javascript:alert(1)"
        with self.assertRaises(ValueError):
            self.regions(config)

    def test_changed_community_links_reach_every_page(self):
        config = copy.deepcopy(self.config)
        config["discordLink"] = "https://discord.gg/example-new-invite"
        for filename, label in SITE.PAGES:
            with self.subTest(page=filename):
                source = (ROOT / filename).read_text()
                updated = SITE.sync_page(source, SITE.render_regions(config, filename, label))
                self.assertNotIn(self.config["discordLink"], updated)
                self.assertIn(config["discordLink"], updated)

    def test_missing_region_fails_instead_of_silently_keeping_stale_content(self):
        source = (ROOT / "info.html").read_text()
        source = source.replace("<!-- /config:header -->", "")
        with self.assertRaisesRegex(ValueError, "header"):
            SITE.sync_page(source, self.regions())


if __name__ == "__main__":
    unittest.main()
