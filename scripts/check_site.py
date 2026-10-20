#!/usr/bin/env python3
"""Dependency-free checks for static pages, links, and shared content."""

from html.parser import HTMLParser
from pathlib import Path
import sys
from urllib.parse import unquote, urlsplit

from update_site import PAGES, ROOT, main as sync_main


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.ids = set()
        self.anchors = []
        self.assets = []
        self.errors = []
        self.h1_count = 0
        self.main_count = 0
        self.has_viewport = False
        self.has_description = False
        self.has_lang = False
        self.active_pages = []
        self.heading_level = 0
        self.feed(path.read_text())

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        element_id = attrs.get("id")
        if element_id:
            if element_id in self.ids:
                self.errors.append(f"Duplicate ID: {element_id}")
            self.ids.add(element_id)
        if tag == "html":
            self.has_lang = bool(attrs.get("lang"))
        if tag == "meta":
            if attrs.get("name") == "viewport":
                self.has_viewport = "width=device-width" in attrs.get("content", "")
            if attrs.get("name") == "description":
                self.has_description = bool(attrs.get("content"))
        if tag == "main":
            self.main_count += 1
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            level = int(tag[1])
            if level > self.heading_level + 1:
                self.errors.append(f"Heading level jumps from h{self.heading_level} to {tag}")
            self.heading_level = level
            if tag == "h1":
                self.h1_count += 1
        if tag == "a":
            self.anchors.append(attrs.get("href", ""))
            if attrs.get("aria-current") == "page":
                self.active_pages.append(attrs.get("href"))
        if tag == "img":
            if "alt" not in attrs:
                self.errors.append(f"Image is missing alt text: {attrs.get('src')}")
            self.assets.append(attrs.get("src", ""))
        if tag == "link" and attrs.get("rel") in {"stylesheet", "icon"}:
            self.assets.append(attrs.get("href", ""))

    def check(self, pages):
        for present, message in (
            (self.h1_count == 1, "Expected one h1"),
            (self.main_count == 1, "Expected one main landmark"),
            (self.has_lang, "Missing document language"),
            (self.has_viewport, "Missing responsive viewport"),
            (self.has_description, "Missing page description"),
            (self.active_pages == [self.path.name], "Active navigation does not match page"),
            ("#main" in self.anchors, "Missing skip link"),
        ):
            if not present:
                self.errors.append(message)
        for reference in self.anchors + self.assets:
            if not reference:
                self.errors.append("Empty link or asset URL")
                continue
            parsed = urlsplit(reference)
            if parsed.scheme or parsed.netloc:
                if parsed.scheme not in {"https", "mailto"}:
                    self.errors.append(f"Unexpected URL scheme: {reference}")
                continue
            target = (self.path.parent / unquote(parsed.path)).resolve() if parsed.path else self.path
            if not target.is_file():
                self.errors.append(f"Missing link or asset: {reference}")
            elif parsed.fragment:
                target_page = pages.get(target.name)
                if target_page and unquote(parsed.fragment) not in target_page.ids:
                    self.errors.append(f"Missing anchor: {reference}")
        return self.errors


def main():
    # Reuse the CLI's non-mutating synchronization check.
    sys.argv = [sys.argv[0], "--check"]
    if sync_main():
        return 1
    pages = {filename: Page(ROOT / filename) for filename, _ in PAGES}
    errors = []
    for filename, page in pages.items():
        errors.extend(f"{filename}: {error}" for error in page.check(pages))
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"Checked {len(pages)} pages: local links, assets, landmarks, headings, and metadata pass.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
