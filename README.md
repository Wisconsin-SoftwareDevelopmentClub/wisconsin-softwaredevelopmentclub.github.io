# Wisconsin Software Development Club website

The club’s public website is plain HTML and CSS, hosted on GitHub Pages. Visitors can learn about the club, explore the project GitHub, and join Discord. All essential content works without JavaScript, a configuration fetch, or a third-party widget.

## Preview locally

Use Python 3.10 or newer. There are no packages to install.

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Open <http://127.0.0.1:8000>. Stop the server with `Ctrl+C`.

## Update club information

1. Edit `config.json` with information confirmed by the current club leadership.
2. Run the content updater and checks:

   ```sh
   python3 scripts/update_site.py
   python3 scripts/check_site.py
   python3 -m unittest discover -s tests -v
   ```

3. Preview the affected pages on a phone-sized and desktop-sized viewport.
4. Commit `config.json` **and the updated HTML** together. The hosting service serves those HTML files directly; it does not run the updater.

The updater rewrites only regions between `<!-- config:NAME -->` and `<!-- /config:NAME -->`. Edit shared content in `scripts/update_site.py` and club details in `config.json`, rather than hand-editing generated regions. Edit other page copy directly in HTML.

| Config field | Purpose |
| --- | --- |
| `siteUrl` | Full public site URL, including any project path. Generates canonical and social image URLs. |
| `semester` | Manually maintained semester label on Home and the optional board section. |
| `discordLink` | Official joining destination, used in all calls to action and the footer. |
| `projectLink` | Official project GitHub organization or repository. |
| `linkedInLink` | Official LinkedIn destination. Keep the lowercase spelling. |
| `meeting` | Confirmed meeting schedule and location as plain text, or `null` to direct people to Discord. |
| `announcement` | Short plain-text notice shown across the site, or `null` to hide it. Remove expired announcements manually. |
| `board` | Current board entries. An empty array hides the whole board section. |

All community links and `siteUrl` must use HTTPS. Text values are escaped when rendered; HTML in config is displayed as text. The updater validates pages before writing, and a failed update leaves the last generated site available.

### Replace the board

Add only confirmed current members. The optional board section appears automatically on About. A member needs `name` and `title`; a photo and public email are optional. Example structure:

```json
{
    "name": "Current member name",
    "title": "Current role",
    "imgURL": "images/current-member.jpg",
    "email": "public-contact@example.com",
    "isContact": true
}
```

Put photos inside `images/`. Omit `imgURL` when no approved photo is available. An email appears only when `isContact` is `true` and `email` is present. Confirm that the member wants that address published. Set `isContact` to `false` or omit it to keep the email out of the generated page.

### Each semester

- Update the semester, project destination, and board together.
- Confirm that the Discord invite and LinkedIn page still work.
- Publish meeting details only when confirmed; otherwise keep `meeting` as `null`.
- Clear expired announcements and remove former officers’ public contact details.
- Add project showcases only when teams have supplied actual descriptions and links.

The refreshed site starts with an empty board and no specific meeting schedule. Discord is the current source for onboarding, meeting details, and announcements. Historical announcements are preserved in Git history. Legacy image files are retained for reference but are not displayed as a current roster.

## Structure and design

| Location | Responsibility |
| --- | --- |
| `index.html` | Club introduction, activities, and joining steps. |
| `project.html` | Project orientation and GitHub links. |
| `info.html` | Club purpose, optional current board, and contact. |
| `css/style.css` | Shared colors, typography, navigation, controls, sections, and footer. |
| `css/index.css`, `css/project.css`, `css/info.css` | Page-specific layouts. |
| `scripts/update_site.py` | Generates shared navigation, footer, metadata, and config-driven content. |
| `scripts/check_site.py`, `tests/` | Static checks and content updater regression tests. |

Change the shared design tokens at the top of `css/style.css` to update colors or typography. Preserve visible keyboard focus, readable contrast, reduced-motion preferences, and the existing three page URLs. Navigation stays visible on mobile without a menu script.

Use meaningful headings, image descriptions, and link text when adding content. The numbered lists intentionally include `role="list"` so assistive technology retains list semantics when CSS hides the default markers.

## Checks and publishing

`check_site.py` checks config synchronization, local page and image links, fragment targets, document language, viewport metadata, one main heading and landmark per page, heading order, image alternatives, the skip link, and active navigation. It does not contact external services or perform a full accessibility audit.

The tests cover configuration changes, optional board contacts, safe text rendering, absent meeting details, and broken generation markers. GitHub Actions runs both checks on pushes and pull requests. The workflow uses the versions shown in the official [checkout](https://github.com/actions/checkout) and [setup-python](https://github.com/actions/setup-python) usage examples.

Before publishing, preview Home, Projects, and About at approximately 320px, 390px, 768px, 1024px, and 1440px wide. Check keyboard navigation, the skip link, community destinations, and image loading. There should be no horizontal page scrolling.

Keep the existing GitHub Pages configuration serving the repository’s root. There is no build or runtime script to deploy. `siteUrl` currently targets `https://wisconsin-softwaredevelopmentclub.github.io/`; if this checkout is published from a personal fork, project path, or custom domain, set it to that actual address and regenerate the HTML first. The checks workflow validates changes; it does not configure Pages or publish the site.

## Commit categories

Use `type(area): concise description`, grouping related changes into small commits:

| Category | Use for |
| --- | --- |
| `content(club)` | Roster, semester, links, meeting details, or page copy. |
| `feat(design)` | New or substantially changed layouts and visual features. |
| `fix(a11y)` | Keyboard, assistive technology, contrast, or motion fixes. |
| `fix(site)` | Broken links, layout defects, or generated content bugs. |
| `refactor(content)` | Content generation or organization changes. |
| `test(site)` | Checks and regression coverage. |
| `chore(ci)` | Automated workflow maintenance. |
| `docs(maintenance)` | Instructions for future maintainers. |

Include why the change was needed and how it was checked in the commit body when that context would help the next maintainer. Keep generated HTML in the same commit as its configuration or generator change.
