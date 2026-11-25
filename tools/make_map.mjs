// One-off: project the world map into SVG paths for the coauthor map.
// Run from a folder where world-atlas@2, d3-geo@3 and topojson-client@3 are installed:
//   node tools/make_map.mjs /path/to/node_modules > data/world.json
// Map data: Natural Earth via world-atlas (public domain), 1:110m scale.
import { readFileSync } from "node:fs";
import { createRequire } from "node:module";
import path from "node:path";

const modules = process.argv[2];
const require = createRequire(path.join(modules, "noop.js"));
const { geoEqualEarth, geoPath, geoCentroid, geoArea } = require("d3-geo");
const { feature } = require("topojson-client");
const world = JSON.parse(readFileSync(path.join(modules, "world-atlas/countries-110m.json"), "utf8"));

const W = 960, H = 470;
let countries = feature(world, world.objects.countries).features
  .filter(f => f.id !== "010"); // drop Antarctica

// Keep France's map shape to metropolitan France and Corsica (drop French Guiana).
for (const f of countries) {
  if (f.id === "250" && f.geometry.type === "MultiPolygon") {
    f.geometry.coordinates = f.geometry.coordinates.filter(poly => {
      const lon = poly[0].reduce((s, p) => s + p[0], 0) / poly[0].length;
      return lon > -10;
    });
  }
}

const fc = { type: "FeatureCollection", features: countries };
const projection = geoEqualEarth().rotate([-10, 0]).fitExtent([[4, 4], [W - 4, H - 4]], fc);
const p = geoPath(projection).digits(1);

// Bounds of a country's main landmasses, ignoring small islands, for framing the map.
function mainBounds(f) {
  const polys = f.geometry.type === "Polygon" ? [f.geometry.coordinates] : f.geometry.coordinates;
  const parts = polys.map(c => ({ type: "Polygon", coordinates: c }));
  const areas = parts.map(g => geoArea(g));
  const max = Math.max(...areas);
  let b = [[Infinity, Infinity], [-Infinity, -Infinity]];
  parts.forEach((g, i) => {
    if (areas[i] < 0.05 * max) return;
    const [[x0, y0], [x1, y1]] = p.bounds(g);
    b = [[Math.min(b[0][0], x0), Math.min(b[0][1], y0)], [Math.max(b[1][0], x1), Math.max(b[1][1], y1)]];
  });
  return b.flat().map(v => Math.round(v * 10) / 10);
}

function mainCentroid(f) {
  const polys = f.geometry.type === "Polygon" ? [f.geometry.coordinates] : f.geometry.coordinates;
  const parts = polys.map(c => ({ type: "Polygon", coordinates: c }));
  const areas = parts.map(g => geoArea(g));
  return projection(geoCentroid(parts[areas.indexOf(Math.max(...areas))]));
}

const out = countries.map(f => {
  const c = mainCentroid(f);
  return { id: f.id, name: f.properties.name, d: p(f), cx: Math.round(c[0]), cy: Math.round(c[1]),
           bounds: mainBounds(f) };
}).filter(f => f.d);

process.stdout.write(JSON.stringify({ width: W, height: H, countries: out }));
