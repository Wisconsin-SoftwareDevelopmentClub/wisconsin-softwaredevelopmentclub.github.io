#!/usr/bin/env python3
"""Sync config-owned regions into plain HTML. No dependencies or hosting build."""

import argparse
from html import escape
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
PAGES = (
    ("index.html", "Home"),
    ("project.html", "Projects"),
    ("info.html", "About"),
)


def text(value):
    return escape(str(value), quote=True)


def https_url(value, label):
    if not isinstance(value, str):
        raise ValueError(f"{label} must be an https URL")
    parsed = urlsplit(value)
    if parsed.scheme != "https" or not parsed.netloc or any(c.isspace() for c in value):
        raise ValueError(f"{label} must be an https URL")
    return text(value)


def render_regions(config, filename, current_page):
    for field in ("semester", "announcement", "meeting"):
        value = config.get(field)
        if value is not None and not isinstance(value, str):
            raise ValueError(f"{field} must be text or null")
    if not isinstance(config.get("board", []), list):
        raise ValueError("board must be an array")
    discord = https_url(config["discordLink"], "discordLink")
    github = https_url(config["projectLink"], "projectLink")
    linkedin = https_url(config["linkedInLink"], "linkedInLink")
    site_url = https_url(config["siteUrl"], "siteUrl").rstrip("/") + "/"
    canonical = site_url + ("" if filename == "index.html" else filename)
    navigation = "\n".join(
        f'                    <a href="{path}"'
        + (' aria-current="page"' if label == current_page else "")
        + f">{label}</a>"
        for path, label in PAGES
    )
    header = f'''    <header class="site-header">
        <div class="container header-inner">
            <a class="brand" href="index.html" aria-label="Wisconsin Software Development Club home">
                <img src="images/sdc-icon.png" width="48" height="48" alt="">
                <span class="brand-name">SDC<span class="brand-place">Wisconsin</span></span>
            </a>
            <nav aria-label="Main navigation">
                <div class="nav-links">
{navigation}
                </div>
                <a class="button button-small" href="{discord}">Join Discord <span aria-hidden="true">↗</span></a>
            </nav>
        </div>
    </header>'''
    footer = f'''    <footer class="site-footer">
        <div class="container footer-main">
            <div>
                <a class="footer-brand" href="index.html">Wisconsin SDC<span aria-hidden="true">.</span></a>
                <p>A community for building software.<br>A place to find your people.</p>
            </div>
            <nav class="footer-links" aria-label="Community links">
                <a href="{discord}">Discord <span aria-hidden="true">↗</span></a>
                <a href="{github}">GitHub <span aria-hidden="true">↗</span></a>
                <a href="{linkedin}">LinkedIn <span aria-hidden="true">↗</span></a>
            </nav>
        </div>
        <div class="container footer-bottom">
            <span>Software Development Club · UW–Madison</span>
            <span>Built together. Maintained by the club.</span>
        </div>
    </footer>'''
    announcement = config.get("announcement")
    notice = ""
    if announcement:
        notice = f'    <aside class="announcement" aria-label="Club announcement"><div class="container">{text(announcement)}</div></aside>'
    meeting = config.get("meeting")
    meeting_content = (
        f'<p>{text(meeting)}</p>'
        if meeting
        else '<p>Find current meeting times, locations, and announcements in Discord.</p>'
    )
    board = config.get("board", [])
    board_content = ""
    if board:
        bios = []
        for member in board:
            if not isinstance(member, dict):
                raise ValueError("Each board entry must be an object with name and title")
            name = text(member["name"])
            title = text(member["title"])
            image = ""
            if member.get("imgURL"):
                image_path = member["imgURL"]
                if not isinstance(image_path, str) or not image_path.startswith("images/") or ".." in Path(image_path).parts:
                    raise ValueError("Board imgURL must be a local path inside images/")
                if not (ROOT / image_path).is_file():
                    raise ValueError(f"Board image does not exist: {image_path}")
                image = f'<img src="{text(image_path)}" alt="Portrait of {name}" width="320" height="320" loading="lazy">'
            contact = ""
            email = member.get("email", "")
            if member.get("isContact") and email:
                if not re.fullmatch(r"[^\s<>\"@]+@[^\s<>\"@]+\.[^\s<>\"@]+", email):
                    raise ValueError(f"Invalid public contact email for {member['name']}")
                contact = f'<a href="mailto:{text(email)}">Email {name}</a>'
            bios.append(f'                <article class="board-card">{image}<h3>{name}</h3><p>{title}</p>{contact}</article>')
        board_content = '''        <section class="section section-tinted" aria-labelledby="board-title">
            <div class="container">
                <p class="eyebrow">The people behind the club</p>
                <h2 id="board-title">Meet the board.</h2>
                <p class="section-intro">''' + text(config["semester"]) + ''' leadership</p>
                <div class="board-grid">
''' + "\n".join(bios) + '''
                </div>
            </div>
        </section>'''
    return {
        "metadata": f'''    <link rel="canonical" href="{canonical}">
    <meta property="og:url" content="{canonical}">
    <meta property="og:image" content="{site_url}images/sdc-icon.png">
    <meta property="og:image:alt" content="Wisconsin Software Development Club logo">''',
        "header": header,
        "announcement": notice,
        "footer": footer,
        "semester": f'                <span class="semester-label">{text(config["semester"])}</span>',
        "meeting": '                    ' + meeting_content,
        "board": board_content,
        "join": f'                <a class="button" href="{discord}">Join our Discord <span aria-hidden="true">↗</span></a>',
        "join-dark": f'                <a class="button button-light" href="{discord}">Join our Discord <span aria-hidden="true">↗</span></a>',
        "github": f'                <a class="button" href="{github}">Explore the project GitHub <span aria-hidden="true">↗</span></a>',
    }


def sync_page(source, regions):
    pattern = r"<!-- config:([\w-]+) -->.*?<!-- /config:\1 -->"
    for name in ("metadata", "header", "announcement", "footer"):
        if len(re.findall(rf"<!-- config:{name} -->.*?<!-- /config:{name} -->", source, flags=re.DOTALL)) != 1:
            raise ValueError(f"Expected exactly one complete {name} config region")
    openings = re.findall(r"<!-- config:([\w-]+) -->", source)
    complete = re.findall(pattern, source, flags=re.DOTALL)
    if openings != complete:
        raise ValueError("A config region is missing its matching closing marker")

    def replace(match):
        name = match.group(1)
        if name not in regions:
            raise ValueError(f"Unknown config region: {name}")
        return f"<!-- config:{name} -->\n{regions[name]}\n<!-- /config:{name} -->"

    return re.sub(pattern, replace, source, flags=re.DOTALL)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Report stale HTML without changing files")
    args = parser.parse_args()
    try:
        config = json.loads((ROOT / "config.json").read_text())
        # Validate every page before writing any of them.
        pages = []
        for filename, label in PAGES:
            path = ROOT / filename
            source = path.read_text()
            updated = sync_page(source, render_regions(config, filename, label))
            pages.append((path, source, updated))
    except (ValueError, KeyError, TypeError, OSError) as error:
        print(f"Cannot sync site: {error}", file=sys.stderr)
        return 1
    stale = []
    for path, source, updated in pages:
        if source != updated:
            stale.append(path.name)
            if not args.check:
                path.write_text(updated)
                print(f"Updated {path.name}")
    if args.check and stale:
        print("Run python3 scripts/update_site.py to update: " + ", ".join(stale), file=sys.stderr)
        return 1
    print("Site content is in sync with config.json.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
