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
2. Run `python3 build.py --domain www.ralibakhshi.com` (requires `pip install jinja2 pyyaml`).
3. Commit both the data change and the rebuilt `docs/` folder, and push to `main`. GitHub Pages publishes within a few minutes.

To replace the CV, overwrite `static/files/Reza-Alibakhshi-CV.pdf` and rebuild.

## Design notes

- Colours: IE University navy `#00338D` for text accents and links; IE Business School blue `#0097DC` only for non-text accents (it is too light for text on white). Ranking badges use the colours Reza specified: FT50 `#F4CC9E`, ABDC `#245292`, ABS (AJG) `#7BC5D0`.
- Type: Piazzolla for reading text and Schibsted Grotesk for navigation and labels, both under the SIL Open Font License and served from this site (no requests to Google Fonts).
- The old Google Sites address `/home` redirects to the home page, and `/research` keeps its address.

## Custom domain

The domain is registered at Squarespace. GitHub's records for an apex domain are four A records pointing to `185.199.108.153`, `185.199.109.153`, `185.199.110.153` and `185.199.111.153`, and a CNAME record for `www` pointing to `rezaalib.github.io`. Check GitHub's documentation on managing a custom domain before changing DNS, since these values can change.
