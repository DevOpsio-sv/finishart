# -*- coding: utf-8 -*-
"""Build a decorative Bulgaria SVG from Natural Earth public-domain data.

Source:
  Natural Earth 1:50m cultural admin-0 countries (Bulgaria, ISO_A3 BGR)
  Natural Earth 1:10m physical rivers and lake centerlines
  https://www.naturalearthdata.com/about/terms-of-use/
  License: public domain. No permission, attribution, or registration required.

Distribution copies fetched at build time:
  https://github.com/martynafford/natural-earth-geojson

The country outline and rivers are geographic. The 1-degree graticule is the
real geographic grid, clipped to the country. Inset parallels are decorative
engraving lines scaled from that outline. They are not roads, oblasts, or
other administrative boundaries.
"""
import json
import math
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public" / "assets" / "bulgaria-map.svg"

COUNTRY_URLS = [
    "https://cdn.jsdelivr.net/gh/martynafford/natural-earth-geojson@master/50m/cultural/ne_50m_admin_0_countries.json",
    "https://raw.githubusercontent.com/martynafford/natural-earth-geojson/master/50m/cultural/ne_50m_admin_0_countries.json",
]
RIVER_URLS = [
    "https://cdn.jsdelivr.net/gh/martynafford/natural-earth-geojson@master/10m/physical/ne_10m_rivers_lake_centerlines.json",
    "https://raw.githubusercontent.com/martynafford/natural-earth-geojson/master/10m/physical/ne_10m_rivers_lake_centerlines.json",
    "https://cdn.jsdelivr.net/gh/martynafford/natural-earth-geojson@master/50m/physical/ne_50m_rivers_lake_centerlines.json",
]

# Names as published by Natural Earth. Evros is the Maritsa; Strymnas is the Struma.
# Romanian rivers that only touch the bounding box (Olt, Borcea) are omitted.
RIVER_NAMES = {"danube", "evros", "strymnas"}

LON0 = 25.4
LAT0 = 42.75
COS = math.cos(math.radians(LAT0))
TARGET_W = 640.0
PAD = 18.0


def fetch(urls):
    last = None
    for url in urls:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "FinishArt-map-build/1.0"})
            with urllib.request.urlopen(req, timeout=90) as response:
                return json.load(response), url
        except Exception as exc:  # noqa: BLE001 - try the next mirror
            last = exc
    raise SystemExit(f"could not download Natural Earth data: {last}")


def is_bulgaria(props):
    for key in ("ISO_A3", "ADM0_A3", "ISO_A3_EH", "iso_a3", "SOV_A3", "ADM0_ISO"):
        if str(props.get(key, "")).upper() == "BGR":
            return True
    name = str(props.get("NAME") or props.get("ADMIN") or props.get("name") or "")
    return name.lower() == "bulgaria"


def as_polygons(geometry):
    gtype = geometry["type"]
    coords = geometry["coordinates"]
    if gtype == "Polygon":
        return [coords]
    if gtype == "MultiPolygon":
        return coords
    raise SystemExit(f"unexpected geometry {gtype}")


def as_lines(geometry):
    gtype = geometry["type"]
    coords = geometry["coordinates"]
    if gtype == "LineString":
        return [coords]
    if gtype == "MultiLineString":
        return coords
    return []


def dist_point_seg(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    if dx == 0 and dy == 0:
        return math.hypot(px - ax, py - ay)
    t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))


def point_in_ring(x, y, ring):
    inside = False
    x1, y1 = ring[-1]
    for x2, y2 in ring:
        if ((y2 > y) != (y1 > y)) and (x < (x1 - x2) * (y - y2) / (y1 - y2) + x2):
            inside = not inside
        x1, y1 = x2, y2
    return inside


def point_in_country(lon, lat, polygons):
    for rings in polygons:
        if not rings:
            continue
        if not point_in_ring(lon, lat, rings[0]):
            continue
        if any(point_in_ring(lon, lat, hole) for hole in rings[1:]):
            continue
        return True
    return False


def near_country(lon, lat, polygons, eps):
    if point_in_country(lon, lat, polygons):
        return True
    for rings in polygons:
        ring = rings[0]
        for i in range(len(ring) - 1):
            ax, ay = ring[i]
            bx, by = ring[i + 1]
            if dist_point_seg(lon, lat, ax, ay, bx, by) <= eps:
                return True
    return False


def perp_dist(p, a, b):
    return dist_point_seg(p[0], p[1], a[0], a[1], b[0], b[1])


def simplify(points, eps):
    if len(points) < 3:
        return points
    closed = points[0] == points[-1]
    work = points[:-1] if closed else points
    if len(work) < 3:
        return points

    def rec(seq):
        if len(seq) < 3:
            return seq
        end = len(seq) - 1
        index, best = 0, 0.0
        for i in range(1, end):
            d = perp_dist(seq[i], seq[0], seq[end])
            if d > best:
                index, best = i, d
        if best <= eps:
            return [seq[0], seq[end]]
        left = rec(seq[: index + 1])
        right = rec(seq[index:])
        return left[:-1] + right

    simplified = rec(work)
    if closed:
        simplified.append(simplified[0])
    return simplified


def project(lon, lat):
    # North is larger y here; to_svg flips it into SVG coordinates.
    return (lon - LON0) * COS, lat


def fmt(n):
    return f"{n:.2f}".rstrip("0").rstrip(".")


def ring_path(ring):
    if len(ring) < 2:
        return ""
    cmds = [f"M{fmt(ring[0][0])} {fmt(ring[0][1])}"]
    cmds.extend(f"L{fmt(x)} {fmt(y)}" for x, y in ring[1:])
    if ring[0] == ring[-1]:
        cmds[-1] = "Z" if len(ring) > 2 else cmds[-1]
        if cmds[-1] != "Z":
            cmds.append("Z")
    return "".join(cmds)


def main():
    countries, country_url = fetch(COUNTRY_URLS)
    feature = next(feat for feat in countries["features"] if is_bulgaria(feat.get("properties") or {}))
    polygons = as_polygons(feature["geometry"])
    for name, lon, lat, expected in (
        ("Sofia", 23.32, 42.70, True),
        ("Lovech", 24.72, 43.14, True),
        ("Pleven", 24.62, 43.42, True),
        ("Romania", 26.1, 44.7, False),
        ("Black Sea", 28.8, 42.6, False),
    ):
        found = point_in_country(lon, lat, polygons)
        if found != expected:
            raise SystemExit(f"geography check failed for {name}: inside={found}")

    rivers_fc, river_url = fetch(RIVER_URLS)
    kept = []
    for feat in rivers_fc["features"]:
        props = feat.get("properties") or {}
        label = str(props.get("name") or props.get("NAME") or props.get("name_en") or "").strip().lower()
        if label not in RIVER_NAMES:
            continue
        for line in as_lines(feat["geometry"]):
            clipped = [pt for pt in line if 22.15 <= pt[0] <= 28.75 and 41.15 <= pt[1] <= 44.35]
            run = []
            for pt in clipped:
                if near_country(pt[0], pt[1], polygons, 0.09):
                    run.append(pt)
                elif len(run) >= 2:
                    kept.append((label, run))
                    run = []
                else:
                    run = []
            if len(run) >= 2:
                kept.append((label, run))

    all_xy = []
    for rings in polygons:
        for ring in rings:
            all_xy.extend(project(lon, lat) for lon, lat in ring)
    min_x = min(p[0] for p in all_xy)
    max_x = max(p[0] for p in all_xy)
    min_y = min(p[1] for p in all_xy)
    max_y = max(p[1] for p in all_xy)
    scale = TARGET_W / (max_x - min_x)

    def to_svg(lon, lat):
        x, y = project(lon, lat)
        return (x - min_x) * scale + PAD, (max_y - y) * scale + PAD

    if to_svg(25.5, 44.0)[1] >= to_svg(25.5, 41.5)[1]:
        raise SystemExit("map is upside down")
    if to_svg(28.3, 43.0)[0] <= to_svg(22.7, 43.0)[0]:
        raise SystemExit("map is mirrored")

    def map_ring(ring, eps):
        mapped = [to_svg(lon, lat) for lon, lat in ring]
        simplified = simplify(mapped, eps)
        if simplified[0] != simplified[-1]:
            simplified.append(simplified[0])
        return simplified

    country_rings = []
    for rings in polygons:
        mapped = [map_ring(ring, 1.15) for ring in rings if len(ring) > 3]
        if mapped:
            country_rings.append(mapped)

    width = (max_x - min_x) * scale + PAD * 2
    height = (max_y - min_y) * scale + PAD * 2

    def centroid(ring):
        sx = sum(p[0] for p in ring[:-1])
        sy = sum(p[1] for p in ring[:-1])
        n = max(1, len(ring) - 1)
        return sx / n, sy / n

    def scaled(ring, factor):
        cx, cy = centroid(ring)
        inner = [((x - cx) * factor + cx, (y - cy) * factor + cy) for x, y in ring[:-1]]
        inner.append(inner[0])
        return inner

    outline = "".join(ring_path(ring) for rings in country_rings for ring in rings)
    inset = "".join(
        ring_path(scaled(rings[0], factor))
        for rings in country_rings
        for factor in (0.972, 0.935)
    )

    graticule = []
    for lon in range(23, 29):
        run = []
        lat = 41.2
        while lat <= 44.3:
            if point_in_country(lon, lat, polygons):
                run.append(to_svg(lon, lat))
            elif run:
                if len(run) > 2:
                    graticule.append(run)
                run = []
            lat += 0.04
        if len(run) > 2:
            graticule.append(run)
    for lat in (42, 43, 44):
        run = []
        lon = 22.2
        while lon <= 28.7:
            if point_in_country(lon, lat, polygons):
                run.append(to_svg(lon, lat))
            elif run:
                if len(run) > 2:
                    graticule.append(run)
                run = []
            lon += 0.04
        if len(run) > 2:
            graticule.append(run)
    graticule_d = "".join(ring_path(simplify(run, 0.8)) for run in graticule)

    river_d = []
    used = []
    for label, line in kept:
        mapped = [to_svg(lon, lat) for lon, lat in line]
        mapped = simplify(mapped, 0.9)
        if len(mapped) >= 2:
            river_d.append(ring_path(mapped).replace("Z", ""))
            used.append(label)

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<!--
  Bulgaria outline: Natural Earth 1:50m Admin 0 — Countries, feature Bulgaria (BGR).
  Rivers: Natural Earth 1:10m rivers and lake centerlines, clipped to Bulgaria.
  Drawn rivers use Natural Earth's published names: Danube, Evros (Maritsa), Strymnas (Struma).
  License: public domain, https://www.naturalearthdata.com/about/terms-of-use/
  Files: {country_url}
         {river_url}
  Rivers drawn: {", ".join(sorted(set(used))) or "none"}.
  Graticule: 1-degree meridians and parallels clipped to the country.
  Inset lines: decorative engraving parallels of the national outline, not boundaries or roads.
-->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {fmt(width)} {fmt(height)}" fill="none">
  <path fill="#C4A08C" fill-opacity="0.55" d="{outline}"/>
  <path stroke="#7A4638" stroke-width="0.7" stroke-opacity="0.45" d="{graticule_d}"/>
  <path stroke="#7A4638" stroke-width="0.85" stroke-opacity="0.55" stroke-linecap="round" stroke-linejoin="round" d="{inset}"/>
  <path stroke="#6C3427" stroke-width="1.35" stroke-linecap="round" stroke-linejoin="round" d="{''.join(river_d)}"/>
  <path stroke="#6C3427" stroke-width="2.15" stroke-linejoin="round" d="{outline}"/>
</svg>
"""
    OUT.write_text(svg, encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"viewBox 0 0 {width:.1f} {height:.1f}")
    print(f"rivers: {sorted(set(used))}")
    print(f"bytes: {OUT.stat().st_size}")


if __name__ == "__main__":
    main()
