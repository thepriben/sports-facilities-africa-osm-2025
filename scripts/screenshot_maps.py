#!/usr/bin/env python3
"""Render the Folium/Leaflet maps to clean PNG figures (no Leaflet UI controls).

Loads each map HTML in headless Chrome after injecting CSS that hides the
Leaflet control container (zoom, attribution, layer switcher), then captures
a screenshot suitable for the preprint figures.
"""
from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAPS = ROOT / "docs" / "maps"
OUT = ROOT / "preprint"

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# (source map, output figure, viewport WxH)
JOBS = [
    ("africa_heatmap.html", "fig1_density.png", (1500, 1500)),
    ("netball.html", "fig2_netball.png", (1500, 1500)),
    ("british_sports.html", "fig3_british_sports.png", (1500, 1500)),
]

# Continental Africa bounding box: [[south, west], [north, east]]
AFRICA_BOUNDS = "[[-35.0, -18.5], [38.0, 52.0]]"

HIDE_CSS = """
<style>
  .leaflet-control-container { display: none !important; }
  .leaflet-control-attribution { display: none !important; }
  html, body { margin: 0; padding: 0; background: #fff; }
</style>
"""

# Folium exposes each map as a global `map_<id>`; fit it tightly to Africa.
FIT_JS = """
<script>
  window.addEventListener('load', function () {
    setTimeout(function () {
      for (var k in window) {
        try {
          if (k.indexOf('map_') === 0 && window[k] && window[k].fitBounds) {
            window[k].fitBounds(%s);
            break;
          }
        } catch (e) {}
      }
    }, 1200);
  });
</script>
""" % AFRICA_BOUNDS


def inject(html: str) -> str:
    extra = HIDE_CSS + FIT_JS
    if "</head>" in html:
        return html.replace("</head>", extra + "</head>", 1)
    return extra + html


def main() -> None:
    OUT.mkdir(exist_ok=True)
    for src, out, (w, h) in JOBS:
        src_path = MAPS / src
        html = src_path.read_text(encoding="utf-8")
        with tempfile.NamedTemporaryFile(
            "w", suffix=".html", dir=MAPS, delete=False, encoding="utf-8"
        ) as tmp:
            tmp.write(inject(html))
            tmp_path = Path(tmp.name)
        out_path = OUT / out
        try:
            subprocess.run(
                [
                    CHROME,
                    "--headless=new",
                    "--hide-scrollbars",
                    "--no-sandbox",
                    "--force-device-scale-factor=2",
                    f"--window-size={w},{h}",
                    "--virtual-time-budget=20000",
                    f"--screenshot={out_path}",
                    tmp_path.as_uri(),
                ],
                check=True,
                capture_output=True,
                timeout=90,
            )
            print(f"[ok] {out_path.relative_to(ROOT)}")
        finally:
            tmp_path.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
