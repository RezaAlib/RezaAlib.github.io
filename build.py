#!/usr/bin/env python3
"""Build the static site into ./docs from ./data, ./templates and ./static.

Usage:
    python3 build.py                # build for preview and for GitHub Pages
    python3 build.py --domain www.ralibakhshi.com   # also write the CNAME file

Requires: jinja2, pyyaml.
"""
import argparse
import datetime as dt
import hashlib
import json
import shutil
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "docs"


def load(name):
    with open(ROOT / "data" / name, encoding="utf-8") as f:
        return yaml.safe_load(f)


def version_hash():
    h = hashlib.sha1()
    for p in sorted((ROOT / "static").rglob("*")):
        if p.is_file() and p.suffix in {".css", ".js"}:
            h.update(p.read_bytes())
    return h.hexdigest()[:8]


def coauthor_map(r):
    """Shade countries by the number of coauthors affiliated there."""
    world = json.loads((ROOT / "data" / "world.json").read_text(encoding="utf-8"))
    projects = [a["authors"] for a in r["journal_articles"]] + [w["authors"] for w in r["in_progress"]]
    by_country = {}
    for c in r["coauthors"]:
        joint = sum(1 for authors in projects if c["name"] in authors)
        entry = by_country.setdefault(c["country"], {"name": c["country_name"], "people": []})
        entry["people"].append({"name": c["name"], "affiliation": c["affiliation"], "joint": joint})
    for entry in by_country.values():
        entry["people"].sort(key=lambda x: (-x["joint"], x["name"].split()[-1]))
        entry["count"] = len(entry["people"])
        entry["bin"] = 1 if entry["count"] == 1 else (2 if entry["count"] <= 3 else 3)

    shapes = []
    for c in world["countries"]:
        cid = c.get("id")
        info = by_country.get(cid)
        shapes.append({"d": c["d"], "id": cid, "name": c["name"], "info": info,
                       "cx": c["cx"], "cy": c["cy"]})
    # draw shaded countries last so their outlines sit on top
    shapes.sort(key=lambda x: x["info"] is not None)
    countries = sorted(by_country.items(), key=lambda kv: (-kv[1]["count"], kv[1]["name"]))
    return {"width": world["width"], "height": world["height"], "shapes": shapes,
            "countries": [dict(id=k, **v) for k, v in countries]}


def person_jsonld(p):
    data = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": p["name"],
        "givenName": p["given_name"],
        "familyName": p["family_name"],
        "jobTitle": p["position"],
        "worksFor": {"@type": "CollegeOrUniversity", "name": p["institution"],
                     "department": p["department"]},
        "alumniOf": [{"@type": "CollegeOrUniversity", "name": e["school"]} for e in p["education"]],
        "email": "mailto:" + p["email"],
        "url": p["site_url"] + "/",
        "image": p["site_url"] + "/img/reza-alibakhshi-800.jpg",
        "sameAs": [x["url"] for x in p["profiles"]],
        "knowsAbout": ["Information systems", "User-generated content", "Social media platforms",
                       "Platform economics", "Econometrics", "Causal inference"],
    }
    return json.dumps(data, ensure_ascii=False, indent=1).replace("</", "<\\/")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--domain", help="custom domain to write into docs/CNAME")
    args = ap.parse_args()

    p = load("profile.yml")
    r = load("research.yml")
    t = load("teaching_service.yml")

    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(ROOT / "static", OUT)

    env = Environment(loader=FileSystemLoader(ROOT / "templates"),
                      autoescape=select_autoescape(["html"]),
                      trim_blocks=True, lstrip_blocks=True)
    env.globals.update(me=p["name"])

    nav = [
        {"label": "Research", "href": "/research/"},
        {"label": "Teaching", "href": "/teaching/"},
        {"label": "Service", "href": "/service/"},
        {"label": "CV", "href": p["cv"]},
    ]
    common = {
        "p": p, "r": r, "t": t, "nav": nav, "version": version_hash(),
        "updated": dt.date.today().strftime("%B %Y"),
    }
    short_desc = (f'{p["name"]} is an {p["position"]} at {p["institution"]} in {p["city"]}. '
                  f'He studies user-generated content, emotion dynamics and the economics of '
                  f'social media platforms.')
    pages = [
        ("index.html", "/", "index.html",
         f'{p["name"]}, {p["position"]}, {p["institution"]}', short_desc),
        ("research.html", "/research/", "research/index.html", f'Research | {p["name"]}',
         f'Journal articles, papers in progress, coauthors, proceedings and talks by {p["name"]}.'),
        ("teaching.html", "/teaching/", "teaching/index.html", f'Teaching | {p["name"]}',
         f'Courses taught by {p["name"]} at IE Business School and HEC Paris, with teaching awards.'),
        ("service.html", "/service/", "service/index.html", f'Service | {p["name"]}',
         f'Editorial roles, reviewing and program committee service of {p["name"]}.'),
        ("404.html", "/404.html", "404.html", f'Page not found | {p["name"]}', short_desc),
    ]
    extra = {"jsonld": person_jsonld(p), "wmap": coauthor_map(r)}
    for tpl, path, out, title, desc in pages:
        html = env.get_template(tpl).render(**common, **extra, path=path, page_title=title,
                                            description=desc)
        dest = OUT / out
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html, encoding="utf-8")

    # The old Google Sites home page lived at /home; send visitors to the new one.
    (OUT / "home").mkdir(exist_ok=True)
    (OUT / "home" / "index.html").write_text(
        '<!doctype html><meta charset="utf-8"><title>Redirecting</title>'
        '<link rel="canonical" href="/"><meta http-equiv="refresh" content="0; url=/">'
        '<p><a href="/">Continue to the home page</a></p>', encoding="utf-8")

    urls = ["/", "/research/", "/teaching/", "/service/"]
    today = dt.date.today().isoformat()
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>',
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sitemap += [f"  <url><loc>{p['site_url']}{u}</loc><lastmod>{today}</lastmod></url>" for u in urls]
    sitemap.append("</urlset>")
    (OUT / "sitemap.xml").write_text("\n".join(sitemap) + "\n", encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {p['site_url']}/sitemap.xml\n",
                                    encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    if args.domain:
        (OUT / "CNAME").write_text(args.domain + "\n", encoding="utf-8")
    print(f"Built {len(pages)} pages into {OUT}")


if __name__ == "__main__":
    main()
