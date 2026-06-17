"""Reconstruit data/sports_facilities.csv depuis l'extrait Afrique de Geofabrik.

Approche « pbf unique » (conforme à la méthodo de l'article) :
  1. téléchargement de africa-latest.osm.pbf (Geofabrik) ;
  2. filtrage osmium (leisure=pitch / leisure=stadium / building=stadium) ;
  3. export GeoJSONSeq, puis extraction (géométrie WKT, sport) → CSV.

Le `.pbf` (~8 Go) est supprimé en fin de traitement, sauf --keep-pbf.
Relancer ce script sur un autre extrait (ou un dump daté) produit une mesure
comparable : c'est le socle de l'observatoire « rejouable ».

Usage :
    python scripts/refresh_from_geofabrik.py
    python scripts/refresh_from_geofabrik.py --keep-pbf

Le téléchargement est parallélisé (plages d'octets) pour contourner le bridage
par connexion de Geofabrik.

Prérequis : `osmium` (osmium-tool) et les paquets de requirements.txt.
"""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import threading
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from shapely.geometry import shape

from common import FACILITIES_CSV

PBF_URL = "https://download.geofabrik.de/africa-latest.osm.pbf"
FILTERS = [
    "nwr/leisure=pitch",
    "nwr/leisure=stadium",
    "nwr/building=stadium",
]
TMP = FACILITIES_CSV.parent / "_tmp"


def run(cmd: list[str]) -> None:
    print("  $", " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True)


def _resolve(url: str) -> tuple[str, int]:
    """Suit les redirections et renvoie (url finale, taille en octets)."""
    req = urllib.request.Request(url, headers={"Range": "bytes=0-0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        final = r.geturl()
        cr = r.headers.get("Content-Range")  # "bytes 0-0/TOTAL"
        if cr and "/" in cr:
            return final, int(cr.rsplit("/", 1)[1])
        return final, int(r.headers["Content-Length"])


def _download_chunk(url: str, start: int, end: int, path: Path, attempts: int = 4) -> None:
    """Télécharge l'intervalle [start, end] et l'écrit à son offset (reprise incluse)."""
    for attempt in range(1, attempts + 1):
        pos = start
        try:
            req = urllib.request.Request(url, headers={"Range": f"bytes={pos}-{end}"})
            with urllib.request.urlopen(req, timeout=120) as r, open(path, "r+b") as f:
                f.seek(pos)
                while True:
                    buf = r.read(1 << 18)
                    if not buf:
                        break
                    f.write(buf)
                    pos += len(buf)
            if pos > end:
                return
            start = pos  # reprise partielle
        except Exception as e:
            if attempt == attempts:
                raise
            print(f"    chunk {start}-{end} retry {attempt} ({e})", flush=True)


def _progress(path: Path, length: int, stop: threading.Event) -> None:
    """Affiche périodiquement la progression (garde le job 'actif')."""
    start = time.time()
    while not stop.wait(8):
        try:
            done = path.stat().st_blocks * 512
        except OSError:
            done = 0
        elapsed = max(time.time() - start, 1)
        rate = done / elapsed / 1e6
        pct = 100 * done / length if length else 0
        eta = (length - done) / (done / elapsed) / 60 if done else 0
        print(f"  … {done/1e6:6.0f}/{length/1e6:.0f} Mo ({pct:4.1f}%) "
              f"{rate:.1f} Mo/s ETA {eta:4.1f} min", flush=True)


def parallel_download(url: str, path: Path, workers: int = 8) -> None:
    final, length = _resolve(url)
    print(f"  {length/1e9:.2f} Go via {workers} connexions parallèles", flush=True)
    with open(path, "wb") as f:
        f.truncate(length)  # pré-allocation (sparse)
    step = length // workers
    ranges = [
        (i * step, (length - 1) if i == workers - 1 else (i * step + step - 1))
        for i in range(workers)
    ]
    stop = threading.Event()
    reporter = threading.Thread(target=_progress, args=(path, length, stop), daemon=True)
    reporter.start()
    try:
        with ThreadPoolExecutor(max_workers=workers) as ex:
            futs = [ex.submit(_download_chunk, final, s, e, path) for s, e in ranges]
            for fu in as_completed(futs):
                fu.result()
    finally:
        stop.set()
    size = path.stat().st_size
    if size != length:
        raise RuntimeError(f"taille inattendue : {size} != {length}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--keep-pbf", action="store_true", help="ne pas supprimer le .pbf")
    parser.add_argument("--url", default=PBF_URL, help="URL de l'extrait .osm.pbf")
    parser.add_argument("--workers", type=int, default=8, help="connexions parallèles")
    args = parser.parse_args()

    TMP.mkdir(parents=True, exist_ok=True)
    pbf = TMP / "africa-latest.osm.pbf"
    filtered = TMP / "filtered.osm.pbf"
    geojson = TMP / "africa.geojsonseq"

    try:
        print("1/4 Téléchargement de l'extrait Afrique…", flush=True)
        parallel_download(args.url, pbf, workers=args.workers)

        print("2/4 Filtrage osmium…", flush=True)
        run(["osmium", "tags-filter", str(pbf), *FILTERS, "--overwrite", "-o", str(filtered)])

        print("3/4 Export GeoJSONSeq…", flush=True)
        run(["osmium", "export", str(filtered), "-f", "geojsonseq",
             "--overwrite", "-o", str(geojson)])

        print("4/4 Extraction (géométrie, sport) → CSV…", flush=True)
        kept = 0
        with open(geojson, "r", encoding="utf-8") as fh, \
                open(FACILITIES_CSV, "w", newline="", encoding="utf-8") as out:
            writer = csv.writer(out)
            writer.writerow(["geometry", "sport"])
            for line in fh:
                line = line.strip().lstrip("\x1e").strip()
                if not line:
                    continue
                feat = json.loads(line)
                sport = (feat.get("properties") or {}).get("sport")
                geom = feat.get("geometry")
                if not sport or not geom:
                    continue
                try:
                    wkt = shape(geom).wkt
                except Exception:
                    continue
                writer.writerow([wkt, sport])
                kept += 1
        print(f"\n✅ {FACILITIES_CSV} reconstruit : {kept} enregistrements sport", flush=True)
    finally:
        filtered.unlink(missing_ok=True)
        geojson.unlink(missing_ok=True)
        if not args.keep_pbf:
            pbf.unlink(missing_ok=True)
        try:
            TMP.rmdir()
        except OSError:
            pass


if __name__ == "__main__":
    main()
