# ralibakhshi.com

Personal academic website of Reza Alibakhshi, served by GitHub Pages from the `docs/` folder of the `main` branch.

## How the site is made

- `data/` holds all the content as plain YAML files.
  - `profile.yml`: name, position, links, the home page texts, education.
  - `research.yml`: journal articles and their ranking badges, papers in progress (described without titles), proceedings, coauthors, talks.
  - `teaching_service.yml`: courses, awards, editorial roles, reviewing.
- `templates/` holds the page layouts (Jinja2).
- `static/` holds the stylesheet, the small script for the coauthor map, fonts, images, favicons and the CV.
- `build.py` reads the data, fills the templates and writes the finished site into `docs/`.
- `tools/make_images.py` redraws the favicons and the social sharing card. It only needs to run again if the name, photo or colours change.

## Updating the site

1. Edit the relevant file in `data/` (for example, add a new article to `journal_articles` in `research.yml`).
2. Run `python3 build.py --domain ralibakhshi.com` (requires `pip install jinja2 pyyaml`).
3. Commit both the data change and the rebuilt `docs/` folder, and push to `main`. GitHub Pages publishes within a few minutes.

To replace the CV, overwrite `static/files/Reza-Alibakhshi-CV.pdf` and rebuild.

## Design notes

- Colours: white page `#FFFFFF`; pale United Nations blue bands `#E7F1FF` with gently curved top and bottom edges (drawn as `::before` layers behind each section; curve depth set by `--arc`); navy `#083279` for the name, headings, years and paper titles (the hue of UN blue, darkened for contrast); black `#000000` body text and links; secondary text `#555555`; United Nations blue `#6491DE` as the accent for link underlines and rules. Coauthor map: ocean `#CFE0F7`, land white, coauthor countries amber `#F6CC94` / `#EEB154` / `#B37900` from one coauthor to four or more. Ranking badges keep the hues Reza specified, made more vivid in OKLCH (same hue, higher chroma): FT50 `#F9B050` (originally `#F4CC9E`), ABDC `#0A4FA4` (originally `#245292`), ABS (AJG) `#2CB4C5` (originally `#7BC5D0`).
- Type: Literata for reading text and headings, Schibsted Grotesk for navigation and labels, both under the SIL Open Font License and served from this site (no requests to Google Fonts).
- The old Google Sites address `/home` redirects to the home page, and `/research` keeps its address.

## Custom domain

The domain is registered at Squarespace. GitHub's records for an apex domain are four A records pointing to `185.199.108.153`, `185.199.109.153`, `185.199.110.153` and `185.199.111.153`, and a CNAME record for `www` pointing to `rezaalib.github.io`. Check GitHub's documentation on managing a custom domain before changing DNS, since these values can change.
