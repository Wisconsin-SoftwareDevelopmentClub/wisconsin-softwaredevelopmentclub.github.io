# Wisconsin Software Development Club website

Static HTML and CSS hosted on GitHub Pages. Maintenance scripts require Python 3.10 or newer, with no additional packages.

## Preview locally

From the repository root:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Open <http://127.0.0.1:8000>. Stop the server with `Ctrl+C`.

## Update content

Edit `config.json` for the semester, community links, meeting details, announcements, and board roster.

- Use HTTPS for community links and `siteUrl`. Set `siteUrl` to the full published URL, including any project path.
- Set `meeting` to `null` to direct visitors to Discord, and `announcement` to `null` to hide the notice. Remove expired announcements manually.
- Each board member needs `name` and `title`. Optional photos go in `images/` and use `imgURL`; use `imgAlt` to override the default description. An empty `board` array hides the section.
- Publish a board member's `email` only with their permission; it appears when `isContact` is `true`.

Edit page copy in `index.html` (Home), `project.html` (Projects), and `info.html` (About). Regions between `<!-- config:NAME -->` and `<!-- /config:NAME -->` are generated; change their content in `config.json` or their templates in `scripts/update_site.py`.

Shared styles are in `css/style.css`; page styles are in the matching CSS files. Board photos use centered square crops; check their framing in `css/info.css` when replacing them.

After changing configuration or templates, regenerate the HTML and run the checks:

```sh
python3 scripts/update_site.py
python3 scripts/check_site.py
python3 -m unittest discover -s tests -v
```

Commit the configuration or template changes **and the updated HTML together**. GitHub Pages serves the HTML directly and does not run the updater.

Before publishing, preview all three pages at mobile and desktop widths. Check keyboard navigation, image loading, and external links. GitHub Actions runs the static checks and tests on pushes and pull requests; external links require manual checking.

## Club naming

Use **Wisconsin Software Development Club**, **Wisconsin SDC**, or **Software Development Club**. Do not put **UW**, **UW-Madison**, or **University of Wisconsin–Madison** before the club name or abbreviation in page titles, headings, branding, descriptions, or accessibility text.

University references can follow the club name, as in “Software Development Club at UW–Madison.” The site checks enforce the prefix rule in page text, metadata, image descriptions, and accessible labels, including names split across inline HTML tags.

## Publishing

Keep GitHub Pages configured to serve the repository root. If the public URL changes, update `siteUrl` and regenerate the HTML before publishing. The checks workflow validates changes; it does not deploy the site.
