# -*- coding: utf-8 -*-
"""Check that local images exist, have real pixels, and keep the restored crops."""
import re
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
ASSETS = PUBLIC / "assets"

failures = []


def fail(message):
    failures.append(message)


html_files = list(PUBLIC.rglob("*.html"))
if not html_files:
    fail("no html pages")

srcs = []
for page in html_files:
    text = page.read_text(encoding="utf-8")
    for src in re.findall(r'<img\b[^>]*\ssrc="([^"]+)"', text):
        if src.startswith("/assets/"):
            srcs.append((page.relative_to(PUBLIC).as_posix(), src))

if not srcs:
    fail("no local images referenced")

seen = {}
for page, src in srcs:
    path = PUBLIC / src.lstrip("/")
    if not path.is_file():
        fail(f"missing file {src} referenced by {page}")
        continue
    if src not in seen:
        with Image.open(path) as im:
            w, h = im.size
        if w < 2 or h < 2:
            fail(f"{src} has empty dimensions {w}x{h}")
        if path.stat().st_size < 500:
            fail(f"{src} is unexpectedly tiny ({path.stat().st_size} bytes)")
        seen[src] = (w, h)

home = (PUBLIC / "bg" / "index.html").read_text(encoding="utf-8")
en_home = (PUBLIC / "en" / "index.html").read_text(encoding="utf-8")
if 'src="/assets/painted-interior-tall-windows.jpg"' not in home or "fetchpriority=\"high\"" not in home:
    fail("hero is missing or not prioritized")
if 'lang="en"' not in en_home or 'hreflang="bg"' not in en_home:
    fail("english home is missing language metadata")
if "tel:+359882820025" not in home:
    fail("bulgarian home is missing the phone link")
if "viber://" in home or "viber://" in en_home:
    fail("an unverified Viber link was published")
if "object-position:72%" in home or "object-position:center 42%" in home or "object-position:center 20%" in home:
    fail("homepage still uses the old focal-point overrides")

css = (PUBLIC / "css" / "styles.css").read_text(encoding="utf-8")
if "aspect-ratio: 276 / 325" not in css:
    fail("service cards are not using the Wix 276/325 frame")
if "../assets/beige-plaster-texture.jpg" not in css:
    fail("why-section texture is not the local file")

with Image.open(ASSETS / "beige-plaster-texture.jpg") as im:
    texture = im.size
if texture[0] <= texture[1]:
    fail(f"texture should be landscape after EXIF orientation, got {texture}")

bath = (PUBLIC / "bg" / "portfolio" / "bathrooms" / "sofia-bathroom-renovation" / "index.html").read_text(encoding="utf-8")
after = bath.find("/assets/sofia-bathroom-after-renovation.jpg")
before = bath.find("/assets/sofia-bathroom-before-renovation.jpg")
if after < 0 or before < 0 or after > before:
    fail("Sofia bathroom gallery is not ordered after, then before")

house = (PUBLIC / "bg" / "portfolio" / "bathrooms" / "house-bathroom-renovation" / "index.html").read_text(encoding="utf-8")
first = house.find('class="gallery"')
chunk = house[first:]
if not chunk.startswith('class="gallery"') and 'class="gallery"' not in house:
    fail("house gallery missing")
order = re.findall(r'src="(/assets/house-bathroom[^"]*)"', chunk)
expected = [
    "/assets/house-bathroom-towel-rail.jpg",
    "/assets/house-bathroom-before-damaged-shower.jpg",
    "/assets/house-bathroom-shower-wood-slat-wall.jpg",
    "/assets/house-bathroom-vanity-leaf-wallpaper.jpg",
]
if order != expected:
    fail(f"house gallery order {order}")

office = PUBLIC / "bg" / "portfolio" / "other-projects" / "office-plaster-and-paint" / "index.html"
stairs = PUBLIC / "bg" / "portfolio" / "other-projects" / "staircase-renovation" / "index.html"
if not office.is_file() or not stairs.is_file():
    fail("missing portfolio project pages for other objects")
else:
    office_html = office.read_text(encoding="utf-8")
    stairs_html = stairs.read_text(encoding="utf-8")
    for src in [
        "/assets/office-before-concrete-shell.jpg",
        "/assets/office-after-painted-columns.jpg",
        "/assets/office-before-plasterboard-walls.jpg",
        "/assets/office-after-painted-walls.jpg",
    ]:
        if src not in office_html:
            fail(f"office gallery missing {src}")
    for src in [
        "/assets/spiral-stair-wood-handrail.jpg",
        "/assets/stair-details-before-renovation.jpg",
        "/assets/stair-details-after-renovation.jpg",
    ]:
        if src not in stairs_html:
            fail(f"stairs gallery missing {src}")

if home.count('width="276" height="325"') != 3:
    fail("service cards should reserve the Wix 276 by 325 frame")
if "height: auto" not in css.split(".service-card img")[1][:180]:
    fail("service images need height: auto so the HTML height does not stretch the frame")

print(f"checked {len(seen)} images across {len(html_files)} pages")
if failures:
    print("FAILED")
    for item in failures:
        print("-", item)
    sys.exit(1)
print("ok")
