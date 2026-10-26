"""Keep university references out of the club's name prefix."""

from pathlib import Path
import sys
import unittest
from unittest.mock import Mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from check_site import Page


class ClubNamingTests(unittest.TestCase):
    def naming_errors(self, source):
        path = Mock()
        path.read_text.return_value = source
        return [error for error in Page(path).errors if error.startswith("University prefix")]

    def test_university_prefixes_are_rejected(self):
        for university in (
            "UW", "UW-Madison", "UW–Madison", "UW‑Madison", "UW—Madison",
            "uw madison", "University of Wisconsin–Madison",
        ):
            for club in ("Software Development Club", "Wisconsin Software Development Club", "SDC", "Wisconsin SDC"):
                with self.subTest(university=university, club=club):
                    self.assertTrue(self.naming_errors(f"<h1>{university} {club}</h1>"))

    def test_metadata_and_accessibility_text_are_checked(self):
        for source in (
            "<title>About | UW-Madison Software Development Club</title>",
            '<meta name="description" content="Join UW SDC.">',
            '<meta property="og:title" content="UW-Madison Software Development Club">',
            '<img alt="UW–Madison SDC logo">',
            '<a aria-label="UW Software Development Club home"></a>',
            '<a title="UW-Madison Wisconsin SDC"></a>',
        ):
            with self.subTest(source=source):
                self.assertTrue(self.naming_errors(source))

    def test_inline_markup_entities_and_line_breaks_do_not_hide_prefixes(self):
        for source in (
            "<h1>UW–<span>Madison</span> <strong>Software Development Club</strong></h1>",
            "<h1>UW&ndash;Madison&nbsp;SDC</h1>",
            "<h1>UW-Madison<br>Software Development Club</h1>",
            "<h1>UW-Madison\n Software Development Club</h1>",
        ):
            with self.subTest(source=source):
                self.assertTrue(self.naming_errors(source))

    def test_club_names_and_following_university_references_are_allowed(self):
        for source in (
            "<title>Wisconsin SDC | Build software. Find your people.</title>",
            "<h1>Wisconsin Software Development Club</h1>",
            "<p>Software Development Club at UW–Madison</p>",
            "<span>Software Development Club · UW–Madison</span>",
            '<meta name="description" content="Meet Wisconsin SDC, a UW–Madison community.">',
            "<p>University of Wisconsin–Madison</p><h1>Software Development Club</h1>",
            '<img alt="UW–Madison campus"><span>Software Development Club</span>',
            "<!-- UW Software Development Club -->",
        ):
            with self.subTest(source=source):
                self.assertEqual([], self.naming_errors(source))


if __name__ == "__main__":
    unittest.main()
